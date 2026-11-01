#!/usr/bin/env python3
"""CDPR-002: real authenticated GitHub TLS disconnect and fresh-client recovery.

This is a GitHub transport test, NOT a ChatGPT/Ecosystem MCP session test.
The GitHub Actions token has repository read-only permissions.
Only a synthetic local file is written. No GitHub write verbs are used.
"""
import base64
import hashlib
import http.client
import json
import os
from pathlib import Path
import socket
import subprocess
import sys
import tempfile
from urllib.parse import quote

HOST = "api.github.com"
REPO = "9TEVE-O/lab-openai-workspace-engineering"
BRANCH = "proof/cdpr-001-resume-pr-20261101"
PR_NUMBER = 66
CHECKPOINT_PATH = "capability-ingest/CDPR-001_STATE.json"
CONTINUATION_PATH = "capability-ingest/CDPR-001_CONTINUATION.json"
CHECKPOINT_BLOB = "bdb4e3213e53a998dbbcd2c540cbb720be59560f"
CONTINUATION_BLOB = "4d7d39bdf4e32fcc508e14bbdd1b82ab56c86e10"
DENIED = {"merge", "deploy", "production changes", "secrets", "unreviewed writes to main", "scope expansion"}


def require_token():
    token = os.getenv("GITHUB_TOKEN")
    if not token:
        raise RuntimeError("GITHUB_TOKEN missing; cannot claim authenticated connection")
    return token


def headers(token):
    return {
        "Authorization": "Bearer " + token,
        "Accept": "application/vnd.github+json",
        "User-Agent": "cdpr-002-bounded-recovery-test",
        "X-GitHub-Api-Version": "2022-11-28",
    }


def api_get(path, token):
    client = http.client.HTTPSConnection(HOST, timeout=20)
    try:
        client.request("GET", path, headers=headers(token))
        response = client.getresponse()
        body = response.read()
        if response.status != 200:
            raise RuntimeError("authenticated GitHub GET failed: HTTP " + str(response.status))
        return json.loads(body)
    finally:
        client.close()


def file_path(name):
    return "/repos/" + REPO + "/contents/" + quote(name, safe="/") + "?ref=" + quote(BRANCH, safe="")


def read_durable(token):
    checkpoint_result = api_get(file_path(CHECKPOINT_PATH), token)
    continuation_result = api_get(file_path(CONTINUATION_PATH), token)
    assert checkpoint_result["sha"] == CHECKPOINT_BLOB, "checkpoint blob drift"
    assert continuation_result["sha"] == CONTINUATION_BLOB, "continuation blob drift"
    checkpoint = json.loads(base64.b64decode(checkpoint_result["content"]))
    continuation = json.loads(base64.b64decode(continuation_result["content"]))
    assert checkpoint["proof_id"] == "CDPR-001"
    assert continuation["proof_id"] == "CDPR-001"
    assert checkpoint["revision"] == 1 and continuation["revision"] == 2
    assert continuation["source_checkpoint"]["blob_sha"] == CHECKPOINT_BLOB
    assert checkpoint["authority"] == continuation["authority"], "authority changed"
    assert checkpoint["authority"]["release_decision"] == "HUMAN_ONLY"
    assert DENIED.issubset(set(checkpoint["authority"]["denied"]))
    assert continuation["status"] == "WAITING_HUMAN_REVIEW"
    assert continuation["pr"]["number"] == PR_NUMBER
    assert continuation["pr"]["draft"] is True
    assert continuation["pr"]["merged"] is False
    pr = api_get("/repos/" + REPO + "/pulls/" + str(PR_NUMBER), token)
    assert pr["state"] == "open" and pr["draft"] is True and pr["merged"] is False, "PR release boundary changed"
    digest = hashlib.sha256(json.dumps(checkpoint["authority"], sort_keys=True, separators=(",", ":")).encode()).hexdigest()
    return {
        "authority_sha256": digest,
        "checkpoint_blob": CHECKPOINT_BLOB,
        "continuation_blob": CONTINUATION_BLOB,
        "release": "HUMAN_ONLY",
        "pr_number": PR_NUMBER,
    }


def effect_once(path, record):
    # An exclusive create is the test's durable synthetic idempotency guard.
    try:
        fd = os.open(path, os.O_CREAT | os.O_EXCL | os.O_WRONLY, 0o600)
    except FileExistsError:
        return False
    with os.fdopen(fd, "w", encoding="utf-8") as handle:
        json.dump(record, handle, sort_keys=True)
        handle.write("\n")
        handle.flush()
        os.fsync(handle.fileno())
    return True


def disconnect_authenticated_client(token):
    # A real TLS connection and authenticated GitHub request are initiated.
    # The transport is forcibly shutdown before reading the response.
    client = http.client.HTTPSConnection(HOST, timeout=20)
    try:
        client.request("GET", file_path(CHECKPOINT_PATH), headers=headers(token))
        sock = client.sock
        assert sock is not None and sock.fileno() >= 0, "no connected TLS socket"
        try:
            sock.shutdown(socket.SHUT_RDWR)
        except OSError:
            # A server close can race the local shutdown; closing still tears
            # down this actual connection, not a mocked network call.
            pass
        client.close()
        assert client.sock is None, "original connection not closed"
    finally:
        client.close()


def before_disconnect(ledger):
    token = require_token()
    record = read_durable(token)
    record.update(operation_id="CDPR-002/PR-66/local-proof", effect_kind="synthetic-local-one-time-marker")
    assert effect_once(ledger, record), "initial effect unexpectedly exists"
    disconnect_authenticated_client(token)
    print(json.dumps({"phase": "before_disconnect", "pid": os.getpid(), "authenticated_read": True,
                      "socket_closed_after_in_flight_request": True, "effect_applied": 1, "release": record["release"]}))
    return 73  # Explicitly indicates the client was interrupted.


def after_reconnect(ledger):
    token = require_token()  # New process creates new authenticated connections.
    record = read_durable(token)
    before = ledger.read_bytes()
    original = json.loads(before)
    assert original["authority_sha256"] == record["authority_sha256"]
    assert original["checkpoint_blob"] == record["checkpoint_blob"]
    assert original["continuation_blob"] == record["continuation_blob"]
    assert original["release"] == "HUMAN_ONLY"
    assert effect_once(ledger, original) is False, "duplicate operation accepted"
    assert ledger.read_bytes() == before, "recovery mutated original effect"
    assert len(list(ledger.parent.glob("effect-*.json"))) == 1, "duplicate effect files found"
    print(json.dumps({"phase": "after_reconnect", "pid": os.getpid(), "new_authenticated_reads": True,
                      "checkpoint_reconstructed": True, "authority_preserved": True,
                      "duplicate_effects": 0, "total_effects": 1, "release": record["release"]}))
    return 0


def orchestrate():
    require_token()
    with tempfile.TemporaryDirectory(prefix="cdpr-002-") as directory:
        ledger = Path(directory) / "effect-CDPR-002.json"
        command = [sys.executable, str(Path(__file__).resolve())]
        first = subprocess.run(command + ["--before", str(ledger)], capture_output=True, text=True)
        assert first.returncode == 73, ("disconnect phase failed", first.returncode, first.stderr[-700:])
        first_receipt = json.loads(first.stdout)
        assert first_receipt["socket_closed_after_in_flight_request"] is True
        second = subprocess.run(command + ["--after", str(ledger)], capture_output=True, text=True)
        assert second.returncode == 0, ("reconnect phase failed", second.returncode, second.stderr[-700:])
        second_receipt = json.loads(second.stdout)
        assert first_receipt["pid"] != second_receipt["pid"], "client process reused"
        assert second_receipt["authority_preserved"] is True
        assert second_receipt["duplicate_effects"] == 0
        assert second_receipt["total_effects"] == 1
        print(json.dumps({
            "proof": "CDPR-002", "result": "PASS", "authenticated_service": "private GitHub REST API",
            "actual_socket_shutdown": True, "new_client_process": True,
            "durable_provider_readback": True, "authority_preserved": True,
            "synthetic_local_effects": 1, "duplicate_effects": 0,
            "pr_remained_draft_unmerged": True, "github_write_operations": 0,
            "ecosystem_mcp_transport_tested": False, "token_expiry_tested": False,
            "distributed_exactly_once_proven": False
        }, indent=2))


if __name__ == "__main__":
    if len(sys.argv) == 3 and sys.argv[1] == "--before":
        sys.exit(before_disconnect(Path(sys.argv[2])))
    if len(sys.argv) == 3 and sys.argv[1] == "--after":
        sys.exit(after_reconnect(Path(sys.argv[2])))
    if len(sys.argv) == 1:
        orchestrate()
    else:
        raise SystemExit("use no args, --before PATH, or --after PATH")
