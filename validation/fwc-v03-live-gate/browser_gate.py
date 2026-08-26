#!/usr/bin/env python3
import json
from pathlib import Path

from playwright.sync_api import sync_playwright

CITATION = "Prateek Patial v Kailash Lawyers Pty Ltd [2025] FWCFB 41"
PINPOINT = "[13]"
SOURCE_URL = "https://www.fwc.gov.au/documents/decisionssigned/pdf/2025fwcfb41.pdf"
REQUIRED = [
    "input_citation",
    "source_authority",
    "source_type",
    "source_title",
    "neutral_citation",
    "source_url",
    "retrieval_timestamp",
    "retrieval_status",
    "verification_status",
]
SUCCESS_REQUIRED = ["retrieved_pinpoint", "retrieved_text"]


def fail(message: str, data=None) -> None:
    if data is not None:
        print(json.dumps(data, ensure_ascii=False, indent=2))
    raise AssertionError(message)


def main() -> None:
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page(viewport={"width": 1280, "height": 900})
        page.goto("http://127.0.0.1:8765/", wait_until="domcontentloaded")

        page.get_by_text(CITATION, exact=False).first.wait_for(timeout=10_000)

        with page.expect_response(
            lambda r: r.url.endswith("/api/retrieve") and r.request.method == "POST",
            timeout=40_000,
        ) as response_info:
            page.get_by_role("button", name="Review citation").click()

        response = response_info.value
        data = response.json()
        print("LIVE_API_RESPONSE_START")
        print(json.dumps(data, ensure_ascii=False, indent=2))
        print("LIVE_API_RESPONSE_END")

        if response.status != 200:
            fail(f"IMPLEMENTATION_BLOCKER: /api/retrieve returned HTTP {response.status}", data)
        if data.get("retrieval_status") != "SOURCE_RETRIEVED":
            fail(
                "IMPLEMENTATION_BLOCKER: live retrieval did not reach SOURCE_RETRIEVED: "
                + str(data.get("failure_message") or data.get("retrieval_status")),
                data,
            )

        missing = [key for key in REQUIRED if not data.get(key)]
        if missing:
            fail("IMPLEMENTATION_BLOCKER: frozen evidence contract missing: " + ", ".join(missing), data)
        success_missing = [key for key in SUCCESS_REQUIRED if not data.get(key)]
        if success_missing:
            fail("IMPLEMENTATION_BLOCKER: successful evidence payload missing: " + ", ".join(success_missing), data)

        expected = {
            "input_citation": CITATION,
            "source_authority": "Fair Work Commission",
            "source_type": "signed decision PDF",
            "source_title": CITATION,
            "neutral_citation": "[2025] FWCFB 41",
            "source_url": SOURCE_URL,
            "retrieved_pinpoint": PINPOINT,
            "verification_status": "PRACTITIONER_VERIFICATION_REQUIRED",
            "matter_number": "C2024/9258",
            "decision_date": "20 February 2025",
        }
        for key, value in expected.items():
            if data.get(key) != value:
                fail(f"IMPLEMENTATION_BLOCKER: {key} mismatch: {data.get(key)!r} != {value!r}", data)

        passage = data["retrieved_text"].strip()
        if len(passage) < 20:
            fail("IMPLEMENTATION_BLOCKER: paragraph [13] retrieval was empty or implausibly short", data)
        if "[14]" in passage:
            fail("IMPLEMENTATION_BLOCKER: paragraph [13] extraction leaked into paragraph [14]", data)

        page.get_by_text("AUTHORITATIVE SOURCE RETRIEVED", exact=True).wait_for(timeout=10_000)
        page.get_by_text("PRACTITIONER_VERIFICATION_REQUIRED", exact=True).wait_for(timeout=10_000)
        page.get_by_role("button", name="Open retrieved evidence").click()

        page.get_by_role("heading", name="Retrieved source evidence").wait_for(timeout=10_000)
        page.get_by_text("PRACTITIONER VERIFICATION REQUIRED", exact=False).first.wait_for(timeout=10_000)
        page.locator(f'a[href="{SOURCE_URL}"]').wait_for(timeout=10_000)

        displayed_passage = page.locator(".source-doc .quote").inner_text().strip()
        if displayed_passage != passage:
            fail("IMPLEMENTATION_BLOCKER: practitioner interface passage does not match retrieved contract passage", data)
        if page.get_by_text(PINPOINT, exact=True).count() < 1:
            fail("IMPLEMENTATION_BLOCKER: practitioner interface did not display pinpoint [13]", data)
        if page.get_by_role("button", name="Continue to decision").count() != 1:
            fail("IMPLEMENTATION_BLOCKER: existing evidence interface did not reach its decision boundary", data)
        if page.get_by_role("heading", name="RESOLVED").count() != 0:
            fail("IMPLEMENTATION_BLOCKER: system crossed practitioner decision boundary without practitioner action", data)

        result = {
            "gate": "FWC v0.3 live retrieval",
            "result": "PASS",
            "citation": CITATION,
            "source_url": SOURCE_URL,
            "retrieval_status": data["retrieval_status"],
            "retrieved_pinpoint": data["retrieved_pinpoint"],
            "retrieval_timestamp": data["retrieval_timestamp"],
            "verification_status": data["verification_status"],
            "retrieved_text": passage,
            "interface_state": "Retrieved source evidence",
            "practitioner_decision_recorded": False,
        }
        Path("live_gate_result.json").write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        print("LIVE_GATE_RESULT_START")
        print(json.dumps(result, ensure_ascii=False, indent=2))
        print("LIVE_GATE_RESULT_END")
        browser.close()


if __name__ == "__main__":
    main()
