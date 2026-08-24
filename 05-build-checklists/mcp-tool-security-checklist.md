# MCP Tool Security Checklist

## Status

Updated 25 August 2026 to align with the approved MCP `2026-07-28` handbook canon.

This checklist is a readiness/security control, not evidence that a server, client or extension is production-ready or protocol-conformant.

## Protocol and transport boundary

- [ ] The intended MCP protocol revision is explicit and tested.
- [ ] Modern `2026-07-28` requests are treated as self-describing; the implementation does not depend on hidden protocol-session state.
- [ ] Any legacy initialize/session fallback is intentional, bounded and tested rather than silently inferred.
- [ ] Application state is explicit; stateless protocol behaviour is not mistaken for stateless application behaviour.
- [ ] HTTP routing/proxy infrastructure preserves and validates required MCP protocol metadata.

## Discovery and capability negotiation

- [ ] Client/server capability discovery is explicit.
- [ ] The host does not assume an extension or capability merely because another SDK/version supports it.
- [ ] Protocol-version downgrade behaviour cannot silently remove a required security control.
- [ ] Unsupported protocol versions or required capabilities fail clearly rather than being guessed.

## Tool inventory

- [ ] Every tool is listed.
- [ ] Every tool has a clear purpose.
- [ ] Every tool has defined input and output schemas.
- [ ] Every tool has side effects classified.
- [ ] Tool names and descriptions do not conceal consequential behaviour.
- [ ] Tool arguments are structurally validated at the execution boundary, not only described in prompts.

## Authority and side-effect review

- [ ] Read-only behaviour is actually read-only.
- [ ] Write actions are explicit.
- [ ] Destructive actions are labelled and separately controlled where appropriate.
- [ ] External-world actions require clear user intent and the required approval boundary.
- [ ] Public or third-party changes are not hidden behind vague tool names.
- [ ] Worker access to MCP tools cannot alter the verifier, policy, credential store or approval mechanism that constrains the worker.
- [ ] A denied/rejected operation leaves protected authoritative state unchanged.

## Multi Round-Trip Requests / elicitation

- [ ] `input_required` or equivalent MRTR flows have an explicit reason and stopping condition.
- [ ] Elicited input is validated before it becomes an execution argument.
- [ ] Human participation is not treated as automatic authorisation for a different or broader action.
- [ ] A multi-round-trip flow cannot be used to smuggle hidden scope expansion past the original request.
- [ ] Pending interactions have timeout/cancellation behaviour appropriate to the host system.

## Authorization and identity

- [ ] OAuth/OIDC discovery and issuer metadata are validated rather than inferred.
- [ ] PKCE requirements are explicitly checked where the selected flow requires them.
- [ ] Redirect URIs and authorization state are strictly validated.
- [ ] Client/server identity used for policy decisions comes from an authenticated source.
- [ ] Tokens are scoped to the minimum required authority and are not exposed to model-visible content unless required.
- [ ] Token/cache behaviour does not allow one client, tenant or server context to reuse another's authority.

## HTTP headers, routing and observability

- [ ] `MCP-Protocol-Version` (or negotiated equivalent) is recorded in execution traces where relevant.
- [ ] `Mcp-Method` / `Mcp-Name` routing metadata is not trusted as sole proof of authorisation.
- [ ] Gateways/WAFs apply policy to the actual authenticated request context, not only a descriptive header.
- [ ] Logs capture enough request/tool identity to investigate actions without unnecessarily storing sensitive payload content.
- [ ] Cache hints and catalogue caching cannot preserve stale authority, stale tool metadata or superseded policy beyond the intended lifetime.

## Sensitive and untrusted data review

- [ ] Tool does not expose secrets.
- [ ] Tool does not log raw sensitive content unnecessarily.
- [ ] Tool does not send unapproved content to models or third parties.
- [ ] Tool respects approval gates.
- [ ] Tool descriptions, resources, logs, elicited text and tool results are treated as potentially untrusted input.
- [ ] Retrieved or returned content cannot become a new source of execution authority merely because it arrived through MCP.

## Tasks extension

Apply only when Tasks are used.

- [ ] The Tasks extension is required by the workflow rather than added by default.
- [ ] Task identity, status, result and cancellation semantics are recorded explicitly.
- [ ] Long-running execution does not expand authority after the initiating request.
- [ ] Task retries are idempotent or otherwise protected from duplicate side effects.
- [ ] Task completion is independently verified before consequential promotion where required.

## MCP Apps extension

Apply only when MCP Apps are used.

- [ ] UI rendering does not confer additional tool authority.
- [ ] User-visible controls accurately represent the action that will occur.
- [ ] UI-provided values are validated at the server/tool boundary.
- [ ] Cross-origin/content-security assumptions are explicit and tested where relevant.
- [ ] The app cannot bypass the same approval and verification controls required for non-UI tool calls.

## Extension maturity gate

- [ ] Every relied-on extension is named and version/spec status is recorded.
- [ ] Required SDK support is verified against the current official SDK/tier evidence.
- [ ] Experimental or recently changed extension behaviour is isolated behind a replaceable adapter where practical.
- [ ] Core-protocol conformance is not used as evidence that an extension is mature or safe for this host.

## Final questions

1. Could this MCP tool surprise a user by doing more than its name, description or UI suggests?
2. Could untrusted MCP content influence a component that has more authority than the content should possess?
3. If the MCP layer were compromised or misconfigured, which protected effects could still occur?
4. Does MCP add concrete interoperability/control value here, or would a smaller direct interface be safer and easier to verify?

If any answer is unclear, the MCP integration has not passed this checklist.

## Canonical source

See `research/technology-extractions/mcp-2026-07-28-canonical-integration.md` for the approved cross-project protocol interpretation and evidence boundary.
