#!/usr/bin/env python3
"""FWC case-authority verification prototype v0.3.

One-authority controlled retrieval server for the low-fidelity prototype.
It accepts only the frozen prototype citation/pinpoint, fetches the pinned
Fair Work Commission signed-decision PDF at request time, validates source
identity, extracts the requested paragraph, and returns the existing Minimum
Evidence Contract. It does not make a practitioner verification decision.
"""

from __future__ import annotations

import io
import json
import re
import ssl
from datetime import datetime
from http import HTTPStatus
from http.client import HTTPSConnection
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import Any

from pypdf import PdfReader

HOST = "127.0.0.1"
PORT = 8765
HERE = Path(__file__).resolve().parent
HTML_FILE = HERE / "FWC_case_authority_verification_prototype_v0_3.html"

CASE = {
    "citation": "Prateek Patial v Kailash Lawyers Pty Ltd [2025] FWCFB 41",
    "pinpoint": "[13]",
    "source_authority": "Fair Work Commission",
    "source_type": "signed decision PDF",
    "source_title": "Prateek Patial v Kailash Lawyers Pty Ltd [2025] FWCFB 41",
    "neutral_citation": "[2025] FWCFB 41",
    "source_host": "www.fwc.gov.au",
    "source_path": "/documents/decisionssigned/pdf/2025fwcfb41.pdf",
    "source_url": "https://www.fwc.gov.au/documents/decisionssigned/pdf/2025fwcfb41.pdf",
    "matter_number": "C2024/9258",
    "decision_date": "20 February 2025",
}

MAX_REQUEST_BYTES = 4096
MAX_PDF_BYTES = 10 * 1024 * 1024
TIMEOUT_SECONDS = 20


def timestamp() -> str:
    return datetime.now().astimezone().isoformat(timespec="seconds")


def base_contract(status: str, failure_message: str | None = None) -> dict[str, Any]:
    payload: dict[str, Any] = {
        "input_citation": CASE["citation"],
        "source_authority": CASE["source_authority"],
        "source_type": CASE["source_type"],
        "source_title": CASE["source_title"],
        "neutral_citation": CASE["neutral_citation"],
        "source_url": CASE["source_url"],
        "retrieval_timestamp": timestamp(),
        "retrieval_status": status,
        "verification_status": "PRACTITIONER_VERIFICATION_REQUIRED",
    }
    if failure_message:
        payload["failure_message"] = failure_message
    return payload


def normalise(text: str) -> str:
    return re.sub(r"\s+", " ", text or "").strip()


def fetch_pinned_pdf() -> bytes:
    """Fetch only the hard-pinned official FWC PDF. Caller cannot choose URL."""
    context = ssl.create_default_context()
    conn = HTTPSConnection(CASE["source_host"], timeout=TIMEOUT_SECONDS, context=context)
    try:
        conn.request(
            "GET",
            CASE["source_path"],
            headers={
                "User-Agent": "FWC-evidence-retrieval-prototype-v0.3/1.0",
                "Accept": "application/pdf",
                "Connection": "close",
            },
        )
        response = conn.getresponse()

        if response.status == HTTPStatus.NOT_FOUND:
            raise FileNotFoundError("The pinned FWC decision PDF returned HTTP 404.")
        if response.status != HTTPStatus.OK:
            raise ConnectionError(f"The pinned FWC decision PDF returned HTTP {response.status}.")

        content_type = (response.getheader("Content-Type") or "").lower()
        if "pdf" not in content_type:
            raise ValueError(f"Pinned FWC source returned unexpected Content-Type: {content_type or 'missing'}.")

        content_length = response.getheader("Content-Length")
        if content_length and int(content_length) > MAX_PDF_BYTES:
            raise ValueError("Pinned FWC PDF exceeds the prototype size limit.")

        body = bytearray()
        while True:
            chunk = response.read(64 * 1024)
            if not chunk:
                break
            body.extend(chunk)
            if len(body) > MAX_PDF_BYTES:
                raise ValueError("Pinned FWC PDF exceeded the prototype size limit while downloading.")

        if not body.startswith(b"%PDF-"):
            raise ValueError("Pinned FWC source did not contain a PDF signature.")
        return bytes(body)
    finally:
        conn.close()


def extract_pdf_text(pdf_bytes: bytes) -> str:
    reader = PdfReader(io.BytesIO(pdf_bytes), strict=False)
    chunks: list[str] = []
    for page in reader.pages:
        chunks.append(page.extract_text() or "")
    text = "\n".join(chunks)
    if not text.strip():
        raise ValueError("No extractable text was found in the FWC PDF.")
    return text


def validate_source_identity(text: str) -> None:
    n = normalise(text).casefold()
    checks = {
        "neutral citation": CASE["neutral_citation"],
        "applicant name": "Prateek Patial",
        "respondent name": "Kailash Lawyers Pty Ltd",
        "matter number": CASE["matter_number"],
        "decision date": CASE["decision_date"],
    }
    missing = [label for label, value in checks.items() if normalise(value).casefold() not in n]
    if missing:
        raise ValueError("FWC source identity validation failed: missing " + ", ".join(missing) + ".")


def extract_pinpoint(text: str, pinpoint: str) -> str:
    """Extract paragraph text from [N] up to the next numbered paragraph."""
    match = re.fullmatch(r"\[(\d+)\]", pinpoint.strip())
    if not match:
        raise ValueError("Pinpoint is not in the frozen [N] form.")

    number = int(match.group(1))
    start_marker = f"[{number}]"
    next_marker = f"[{number + 1}]"

    start = text.find(start_marker)
    if start < 0:
        raise LookupError(f"Requested pinpoint {start_marker} was not found in the retrieved PDF.")

    end = text.find(next_marker, start + len(start_marker))
    if end < 0:
        end = len(text)

    passage = text[start + len(start_marker):end]
    passage = normalise(passage)
    if not passage:
        raise LookupError(f"Requested pinpoint {start_marker} contained no extractable text.")
    return passage


def retrieve(citation: str, pinpoint: str) -> tuple[int, dict[str, Any]]:
    # Authority boundary: caller cannot turn this prototype into a general URL fetcher.
    if citation != CASE["citation"] or pinpoint != CASE["pinpoint"]:
        return HTTPStatus.BAD_REQUEST, base_contract(
            "RETRIEVAL_ERROR",
            "This v0.3 controlled retrieval path only accepts the frozen prototype citation and pinpoint.",
        )

    try:
        pdf_bytes = fetch_pinned_pdf()
    except FileNotFoundError as exc:
        return HTTPStatus.OK, base_contract("SOURCE_NOT_FOUND", str(exc))
    except (ConnectionError, TimeoutError, OSError) as exc:
        return HTTPStatus.OK, base_contract("SOURCE_UNAVAILABLE", f"Authoritative FWC source could not be obtained: {exc}")
    except ValueError as exc:
        return HTTPStatus.OK, base_contract("SOURCE_UNAVAILABLE", str(exc))

    try:
        text = extract_pdf_text(pdf_bytes)
        validate_source_identity(text)
    except Exception as exc:
        return HTTPStatus.OK, base_contract("RETRIEVAL_ERROR", f"Retrieved source could not be validated: {exc}")

    try:
        retrieved_text = extract_pinpoint(text, pinpoint)
    except LookupError as exc:
        return HTTPStatus.OK, base_contract("PINPOINT_NOT_FOUND", str(exc))
    except Exception as exc:
        return HTTPStatus.OK, base_contract("RETRIEVAL_ERROR", f"Pinpoint extraction failed: {exc}")

    payload = base_contract("SOURCE_RETRIEVED")
    payload.update(
        {
            "matter_number": CASE["matter_number"],
            "decision_date": CASE["decision_date"],
            "retrieved_pinpoint": pinpoint,
            "retrieved_text": retrieved_text,
        }
    )
    return HTTPStatus.OK, payload


class Handler(BaseHTTPRequestHandler):
    server_version = "FWCRetrievalPrototype/0.3"

    def log_message(self, fmt: str, *args: Any) -> None:
        print(f"[{self.log_date_time_string()}] {fmt % args}")

    def _send_json(self, status: int, payload: dict[str, Any]) -> None:
        body = json.dumps(payload, ensure_ascii=False, separators=(",", ":")).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.send_header("X-Content-Type-Options", "nosniff")
        self.end_headers()
        self.wfile.write(body)

    def _send_html(self) -> None:
        try:
            body = HTML_FILE.read_bytes()
        except OSError as exc:
            self.send_error(HTTPStatus.INTERNAL_SERVER_ERROR, explain=str(exc))
            return
        self.send_response(HTTPStatus.OK)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.send_header("X-Content-Type-Options", "nosniff")
        self.send_header("Content-Security-Policy", "default-src 'self'; script-src 'self' 'unsafe-inline'; style-src 'self' 'unsafe-inline'; connect-src 'self'; img-src 'self' data:; frame-ancestors 'none'; base-uri 'none'")
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self) -> None:
        if self.path in ("/", "/index.html", "/FWC_case_authority_verification_prototype_v0_3.html"):
            self._send_html()
            return
        if self.path == "/health":
            self._send_json(HTTPStatus.OK, {"status": "ok", "version": "0.3"})
            return
        self.send_error(HTTPStatus.NOT_FOUND)

    def do_POST(self) -> None:
        if self.path != "/api/retrieve":
            self.send_error(HTTPStatus.NOT_FOUND)
            return

        content_type = (self.headers.get("Content-Type") or "").split(";", 1)[0].strip().lower()
        if content_type != "application/json":
            self._send_json(HTTPStatus.UNSUPPORTED_MEDIA_TYPE, base_contract("RETRIEVAL_ERROR", "Content-Type must be application/json."))
            return

        try:
            length = int(self.headers.get("Content-Length") or "0")
        except ValueError:
            length = 0
        if length <= 0 or length > MAX_REQUEST_BYTES:
            self._send_json(HTTPStatus.BAD_REQUEST, base_contract("RETRIEVAL_ERROR", "Invalid retrieval request size."))
            return

        try:
            data = json.loads(self.rfile.read(length).decode("utf-8"))
            citation = data.get("citation")
            pinpoint = data.get("pinpoint")
            if not isinstance(citation, str) or not isinstance(pinpoint, str):
                raise ValueError("citation and pinpoint must be strings")
        except Exception as exc:
            self._send_json(HTTPStatus.BAD_REQUEST, base_contract("RETRIEVAL_ERROR", f"Invalid retrieval request: {exc}"))
            return

        status, payload = retrieve(citation, pinpoint)
        self._send_json(status, payload)


if __name__ == "__main__":
    if not HTML_FILE.exists():
        raise SystemExit(f"Missing prototype HTML: {HTML_FILE}")
    server = ThreadingHTTPServer((HOST, PORT), Handler)
    print(f"FWC prototype v0.3: http://{HOST}:{PORT}")
    print("Press Ctrl+C to stop.")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()
