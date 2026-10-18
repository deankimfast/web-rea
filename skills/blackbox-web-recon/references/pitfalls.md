# Pitfalls that change the result

| Pitfall | Required response |
|---|---|
| Feedback reveals the answer | Even “look for limits that reset over time” narrows the mechanism. Send counts only within fixed areas. Classify rounds receiving mechanism hints or source-derived approaches as assisted and separate their scores. |
| A scorer's plausible assumption is wrong | Independently verify header/proxy handling, effective settings, middleware ordering and counter storage before freezing the inventory. A bad header assumption distorted two rounds in the originating exercise. Re-score affected reports with one corrected baseline. |
| Rule list changes each round | Freeze IDs, rubric, scope and denominator. If a real inventory defect requires revision, re-score all rounds or explicitly mark them non-comparable. Do not optimize the list to the latest findings. |
| Wrong claims disappear from coverage math | Partition rules into C/P/W/M. Keep W in N; do not count a rule as both W and M. Track unrelated false claims separately. |
| Failed-login budget cannot reach a boundary | Pre-plan separate budgets for login and MFA and enough disposable identities for independent checks. If the cap prevents inference, report a bound/unknown; don't silently exceed it or count budget exhaustion as a product rule. |
| “Unlimited” means unbounded loops | Agree a practical request/time ceiling even for disposable accounts. A long time window can remain unknown. Stop on unexpected provider effects or scope changes. |
| Header changes appear to clear a lockout | Do not infer scope from one success/failure or assume forwarding headers are ignored. State exactly which responses occurred, with account, session, timing and allowed header variations controlled. Verification belongs to the private scorer check; don't leak the explanation into feedback. |
| Spam trigger or clearing rule remains hidden | Consent, routing, tenant state, callback authenticity, counter windows or absent workers can prevent reaching the relevant decision. State reachability limits. Do not invent exact thresholds from a few negative results or call direct DB edits HTTP inference. |
| Tokens cannot be obtained without email | Provide a local non-relaying sink or declared file capture. Separate email-enabled and email-free cohorts. A returned generic success does not establish delivery, token expiry, or single-use behavior. |
| Waiting is confused with expiry | Record server/observer time and actual elapsed intervals. Sleeping below/above one suspected boundary establishes bounds, not necessarily the exact threshold or reset window. |
| Dirty fixtures or retries contaminate results | Reset all state consistently. Cookie jars, counters, previous failures, asynchronous jobs and automatic client retries can affect later requests. Record every attempt, including failed tool actions separately from HTTP responses. |
| A tool refusal is recorded as a server result | No request was sent. Mark the check unexecuted and retain the approval limitation; never invent a 403/409/500 response. |
| High scores are built from route enumeration | Require rule assertions plus distinguishing behavior, not just schema copies or endpoint lists. Denial-only observations do not demonstrate the successful path. |
| Local fixture stands in for production | Publish relevant configuration differences and access tiers. A seeded admin, captured mailbox and disabled callback verification provide capabilities an anonymous outsider normally lacks. |
| Agent isolation is overstated | Fresh context and separate working directories reduce contamination but do not enforce access restrictions. Same-UID chmod is reversible. Record actual tool/filesystem/network controls. |
| A plateau is “fixed” by hints | Keep a predeclared plateau and round cap. The originating run plateaued near 50–60% after round three; later gains depended heavily on hints. Interpret 50–65% as a practical expectation, not a universal benchmark. |

Exposure and vulnerability are different. A discoverable validation rule or plan limit may be intended functionality. Owner remediation should address sensitive disclosures, inconsistent controls or weak boundaries supported by evidence; do not recommend hiding all documentation or treating obscurity as a security control.
