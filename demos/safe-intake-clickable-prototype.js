const states = [
  "received",
  "extracted",
  "classified",
  "classified_with_findings",
  "redacted",
  "needs_review",
  "approval_state_missing",
  "approved_for_ai",
  "blocked",
  "used_or_exported",
];

const rawFixture = `ARTIST ONBOARDING FORM — SYNTHETIC DEMO ONLY

Artist / Project Name:
River Echo Demo Project

Primary Contact:
Avery Placeholder

Representative / Manager:
Morgan Example

Email:
avery.placeholder@example.test

Phone:
+61 400 000 000

Postal Address:
100 Example Street, Demo Suburb, NT 0800, Australia

ABN / Business Reference:
00 000 000 000

Payment Term:
Invoice payable within 14 days of approved milestone delivery.

Banking Note:
Payment details to be confirmed through secure approved channel. Do not process from this form.

Private Note:
Artist has requested that unreleased project details are not shared outside the review team.

Signature Placeholder:
/s/ Avery Placeholder

Date:
01 January 2026`;

const redactedFixture = `ARTIST ONBOARDING FORM — SYNTHETIC DEMO ONLY

Artist / Project Name:
[PROJECT_NAME]

Primary Contact:
[PERSON_NAME]

Representative / Manager:
[PERSON_NAME]

Email:
[EMAIL]

Phone:
[PHONE]

Postal Address:
[ADDRESS]

ABN / Business Reference:
[BUSINESS_REFERENCE]

Payment Term:
[PAYMENT_TERM]

Banking Note:
[PAYMENT_NOTE]

Private Note:
[PRIVATE_NOTE]

Signature Placeholder:
[SIGNATURE]

Date:
[DATE]`;

const findings = [
  "[PROJECT_NAME]",
  "[PERSON_NAME]",
  "[EMAIL]",
  "[PHONE]",
  "[ADDRESS]",
  "[BUSINESS_REFERENCE]",
  "[PAYMENT_TERM]",
  "[PAYMENT_NOTE]",
  "[PRIVATE_NOTE]",
  "[SIGNATURE]",
  "[DATE]",
];

const model = {
  state: "received",
  approvalReason:
    "Synthetic fixture reviewed. Redacted working copy may be used for demo summary.",
  documentId: "doc_synth_artist_onboarding_001",
  redactedCopyId: null,
  safeSummary: null,
  audit: [],
};

function esc(value) {
  return String(value)
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;")
    .replaceAll("'", "&#039;");
}

function button(label, action, className = "") {
  return `<button ${className ? `class="${className}"` : ""} data-action="${action}">${label}</button>`;
}

function addAudit(action, previousState, newState, reason, evidenceRef) {
  model.audit.unshift({
    event_id: `evt_${String(model.audit.length + 1).padStart(3, "0")}`,
    timestamp: new Date().toISOString(),
    actor: "prototype_user_or_system",
    item_id: model.redactedCopyId || model.documentId,
    action,
    previous_state: previousState,
    new_state: newState,
    reason,
    evidence_ref: evidenceRef,
  });
}

function transition(newState, action, reason, evidenceRef) {
  const oldState = model.state;
  model.state = newState;
  addAudit(action, oldState, newState, reason, evidenceRef);
  render();
}

function block(action, reason) {
  addAudit(action, model.state, model.state, reason, "blocked_action_log");
  render(`Blocked: ${reason}`);
}

const actions = {
  extractText() {
    transition("extracted", "text_extracted", "Synthetic fixture text parsed locally.", "raw_fixture_preview");
  },
  classifySensitivity() {
    transition("classified", "sensitivity_classified", "Contains personal, business-reference, payment-process, and private project information.", "classification_panel");
  },
  detectCategories() {
    transition("classified_with_findings", "categories_detected", "Expected synthetic fixture categories detected.", "findings_panel");
  },
  createRedactedCopy() {
    model.redactedCopyId = "redacted_copy_001";
    transition("redacted", "redacted_copy_created", "Raw values replaced with category labels.", "redacted_copy_preview");
  },
  sendToReview() {
    transition("needs_review", "human_review_requested", "Reviewer decision required before AI use.", "review_panel");
  },
  approveForAI() {
    if (!model.approvalReason.trim()) {
      block("approval_attempt_without_reason", "Reviewer decision reason required.");
      return;
    }
    transition("approved_for_ai", "approval_granted", model.approvalReason.trim(), "approval_record");
  },
  requestChanges() {
    transition("redacted", "changes_requested", "Reviewer requested redaction changes before approval.", "review_record");
  },
  blockUse() {
    transition("blocked", "content_blocked", "Reviewer blocked downstream AI use for this item.", "review_record");
  },
  safeSummary() {
    if (model.state !== "approved_for_ai") {
      block("safe_summary_attempt", "only approved redacted content can enter the AI workflow.");
      return;
    }
    model.safeSummary =
      "This synthetic artist onboarding form contains contact, address, business-reference, payment-process, and private project fields. Sensitive values were replaced with category labels before approval.";
    transition("used_or_exported", "safe_summary_generated", "Summary generated from approved redacted copy only.", "safe_summary_panel");
  },
  exportAudit() {
    if (!["approved_for_ai", "used_or_exported", "blocked"].includes(model.state)) {
      block("audit_export_attempt", "only reviewed items can export an audit summary in this demo.");
      return;
    }
    transition("used_or_exported", "audit_summary_exported", "Audit summary made visible in prototype.", "audit_summary_panel");
  },
  tryRawSummary() {
    block(
      model.state === "approved_for_ai"
        ? "raw_summary_attempt_after_approval"
        : "raw_summary_attempt_before_approval",
      "raw source is not the approved boundary; only approved redacted content can enter the AI workflow."
    );
  },
  queryBeforeApproval() {
    block("query_before_approval_attempt", "only approved redacted content can enter the AI workflow.");
  },
  exportBeforeApproval() {
    block("export_before_approval_attempt", "only approved redacted content can enter the AI workflow.");
  },
  tryRawExport() {
    block(
      "raw_source_export_attempt",
      "Raw source document cannot be exported from this demo path before approval or after approval. Export the audit summary or approved redacted copy boundary only."
    );
  },
  simulateMissingApprovalState() {
    const oldState = model.state;
    model.state = "approval_state_missing";
    addAudit(
      "missing_approval_state_test",
      oldState,
      model.state,
      "Missing approval state. Workflow fails closed.",
      "demo_only_missing_approval_state_control"
    );
    render("Missing approval state. Workflow fails closed.");
  },
  resetDemo() {
    resetDemo();
  },
};

function resetDemo() {
  model.state = "received";
  model.redactedCopyId = null;
  model.safeSummary = null;
  model.audit = [];
  model.approvalReason =
    "Synthetic fixture reviewed. Redacted working copy may be used for demo summary.";
  addAudit(
    "document_received",
    "none",
    "received",
    "Synthetic artist onboarding fixture loaded locally.",
    "synthetic_fixture"
  );
  render();
}

function negativeControls() {
  return `${button("Try summarise raw document", "tryRawSummary", "danger")}${button(
    "Try export raw source",
    "tryRawExport",
    "danger"
  )}${button("Simulate missing approval state", "simulateMissingApprovalState", "ghost")}`;
}

function renderStatebar() {
  const current = states.indexOf(model.state);
  document.getElementById("statebar").innerHTML = states
    .map((state, index) => {
      const stateClass =
        state === model.state ? "active" : index < current && model.state !== "blocked" ? "done" : "";
      return `<span class="pill ${stateClass}">${state}</span>`;
    })
    .join("");
}

function renderStage(message = "") {
  const statusClass =
    model.state === "approved_for_ai"
      ? "good"
      : model.state === "blocked" || model.state === "approval_state_missing"
        ? "bad"
        : model.state === "needs_review"
          ? "warn"
          : "";

  let html = `<span class="status ${statusClass}">${model.state}</span>${
    message ? `<div class="notice bad"><strong>${esc(message)}</strong></div>` : ""
  }`;

  if (model.state === "received") {
    html += `<h2>1. Document received</h2><p>A synthetic artist onboarding form has entered the local demo workflow. This raw source is not approved for AI use.</p><div class="buttons">${button("Extract text", "extractText")}${negativeControls()}</div>`;
  }
  if (model.state === "extracted") {
    html += `<h2>2. Text extracted</h2><p>Visible text and simple metadata were extracted from the synthetic fixture.</p><div class="notice"><strong>Metadata:</strong> method=fixture text parse; length=${rawFixture.length} characters; source=synthetic fixture.</div><div class="buttons">${button("Classify sensitivity", "classifySensitivity")}${negativeControls()}</div>`;
  }
  if (model.state === "classified") {
    html += `<h2>3. Sensitivity classified</h2><p>The fixture is classified as containing personal, business-reference, payment-process, and private project information.</p><div class="notice"><strong>Recommended state:</strong> needs_review before downstream AI use.</div><div class="buttons">${button("Detect sensitive categories", "detectCategories")}${negativeControls()}</div>`;
  }
  if (model.state === "classified_with_findings") {
    html += `<h2>4. Sensitive categories detected</h2><p>Detected categories are shown as labels. The audit view should not repeat unnecessary raw values.</p><div>${findings.map((finding) => `<span class="finding">${finding}</span>`).join("")}</div><div class="buttons">${button("Create redacted copy", "createRedactedCopy")}${negativeControls()}</div>`;
  }
  if (model.state === "redacted") {
    html += `<h2>5. Redacted working copy</h2><p>A separate redacted copy has been created. It is not approved yet.</p><div class="notice"><strong>Redacted copy ID:</strong> ${model.redactedCopyId}</div><div class="buttons">${button("Send to review", "sendToReview")}${negativeControls()}</div>`;
  }
  if (model.state === "needs_review") {
    html += `<h2>6. Human review required</h2><p>The reviewer must approve, request changes, or block. Downstream AI use remains blocked until approval.</p><label for="reason">Reviewer decision reason</label><textarea id="reason">${esc(model.approvalReason)}</textarea><div class="buttons">${button("Approve for AI", "approveForAI")}${button("Request changes", "requestChanges", "secondary")}${button("Block", "blockUse", "danger")}${button("Query before approval", "queryBeforeApproval", "ghost")}${button("Export before approval", "exportBeforeApproval", "ghost")}${negativeControls()}</div>`;
  }
  if (model.state === "approval_state_missing") {
    html += `<h2>6B. Missing approval-state simulation</h2><p>This demo-only negative test simulates a missing or invalid approval state. The workflow fails closed and records a blocked audit event.</p><div class="buttons">${button("Try safe summary with missing state", "safeSummary", "danger")}${button("Reset demo", "resetDemo", "ghost")}</div>`;
  }
  if (model.state === "approved_for_ai") {
    html += `<h2>7A. Approved for AI</h2><p>Only the approved redacted copy may be used. The raw source remains outside the approved boundary.</p><div class="notice good"><strong>Approved boundary:</strong> ${model.redactedCopyId}</div><div class="buttons">${button("Generate safe summary", "safeSummary")}${button("Export audit summary", "exportAudit", "secondary")}${button("Try raw source anyway", "tryRawSummary", "danger")}${button("Try export raw source", "tryRawExport", "danger")}</div>`;
  }
  if (model.state === "blocked") {
    html += `<h2>7B. Blocked</h2><p>The reviewer blocked downstream AI use. The next action is to revise redaction or keep the item out of AI workflows.</p><div class="buttons">${button("View audit summary", "exportAudit", "secondary")}${button("Reset demo", "resetDemo", "ghost")}</div>`;
  }
  if (model.state === "used_or_exported") {
    html += `<h2>8. Audit summary / approved use</h2><p>The demo has produced either a safe summary, an audit summary, or both.</p>${
      model.safeSummary
        ? `<div class="notice good"><strong>Safe summary:</strong> ${esc(model.safeSummary)}</div>`
        : ""
    }<div class="buttons">${button("Reset demo", "resetDemo", "ghost")}${button("Try export raw source", "tryRawExport", "danger")}</div>`;
  }

  document.getElementById("stageCard").innerHTML = html;
}

function renderDecisionPanel() {
  const approved =
    model.state === "approved_for_ai" || model.state === "used_or_exported"
      ? model.redactedCopyId
      : "none";
  document.getElementById("decisionPanel").innerHTML = `<p><strong>Current state:</strong> <code>${model.state}</code></p><p><strong>Document ID:</strong> <code>${model.documentId}</code></p><p><strong>Redacted copy ID:</strong> <code>${model.redactedCopyId || "not created"}</code></p><p><strong>Approved boundary:</strong> <code>${approved}</code></p><div class="notice ${approved === "none" ? "bad" : "good"}">${approved === "none" ? "Downstream AI use is blocked." : "Approved redacted content may be used for the safe summary path."}</div><div class="buttons">${button("Reset demo", "resetDemo", "ghost")}</div>`;
}

function renderDocuments() {
  document.getElementById("rawDoc").textContent = rawFixture;
  const workingDoc = document.getElementById("workingDoc");
  if (model.redactedCopyId) {
    workingDoc.textContent = redactedFixture;
    workingDoc.classList.remove("muted");
  } else {
    workingDoc.textContent = "No redacted working copy has been approved yet.";
    workingDoc.classList.add("muted");
  }
}

function renderAudit() {
  const list = document.getElementById("auditList");
  if (!model.audit.length) {
    list.innerHTML = `<p class="muted small">No audit events yet.</p>`;
    return;
  }
  list.innerHTML = model.audit
    .map(
      (event) =>
        `<div class="audit"><strong>${event.event_id}</strong> · ${esc(event.action)}<br><span class="muted">${esc(event.previous_state)} → ${esc(event.new_state)}</span><br>reason: ${esc(event.reason)}<br>evidence: <code>${esc(event.evidence_ref)}</code><br><span class="muted">${esc(event.timestamp)}</span></div>`
    )
    .join("");
}

function render(message = "") {
  renderStatebar();
  renderStage(message);
  renderDecisionPanel();
  renderDocuments();
  renderAudit();
}

document.addEventListener("click", (event) => {
  const target = event.target.closest("[data-action]");
  if (!target) return;
  const action = target.dataset.action;
  if (typeof actions[action] === "function") {
    actions[action]();
  }
});

document.addEventListener("input", (event) => {
  if (event.target.id === "reason") {
    model.approvalReason = event.target.value;
  }
});

resetDemo();
