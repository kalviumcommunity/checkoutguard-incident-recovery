# Q4: Recover a Release and Document Incident Evidence

**Course:** DevOps Foundation · **Module:** 5, Monitoring, Cost & Production Readiness  
**Submission:** one PDF file upload · **Difficulty:** medium · **Marks:** 20  
**Target duration:** 34 minutes, including screenshots and PDF assembly after preparation. Budget 40 minutes maximum; pilot timing not yet measured.  
**Lesson alignment:** 5.4 queries; 5.5 mitigation; 5.8 evidence-backed postmortem.

## Problem statement

CheckoutGuard fails checkout requests after a supplied release change, while its shallow health endpoint remains green. Establish evidence, restore bundled known-good release variant and document measured local recovery.

**Starter repository:** https://github.com/kalviumcommunity/checkoutguard-incident-recovery  
**Allowed edits:** release.env: RELEASE value only; postmortem.md: five short sections. Preserve app variants, log helpers, request batch, health probe and supplied release record.

## Preparation (before assessment timer)

Use Python 3.10+ on host, Git, Docker Engine/Desktop and Compose v2 (supports --no-log-prefix). Linux/macOS or prepared WSL. No pip packages, jq, paid tools, registry credentials or cloud account required. Docker Desktop subject to its license; free Linux Docker Engine sufficient.

Clone supplied repo (fork optional), enter directory and reserve host port 18094. Download/build before timer:

```sh
docker pull python:3.12-slim
# No additional monitoring image needed.
docker compose config --quiet
docker compose build
mkdir -p evidence
docker compose up -d
```

Wait up to 15 seconds for listeners/probes/scrapes before diagnosing. Initial task faults are intentional, not setup failures. If Docker/tool/download or port setup fails, resolve before starting timer. Commands run from repo root. Host evidence/ is ignored. Use a fresh exercise stack with no unrelated traffic. Do not edit helpers to force checks to pass.

## Task 1: Establish incident evidence (6 marks, ~10 minutes)

Run before batch of five checkout requests; save and query records belonging to those request IDs. Compare observed release/error with release-record.md. State measured failed/total requests and evidence-supported rollback decision. Healthy liveness alone does not establish checkout success. Record actual local detection time with timezone.

```sh
date '+%Y-%m-%dT%H:%M:%S%z'
python3 batch.py before
docker compose logs --no-color --no-log-prefix api > evidence/before.jsonl
python3 batch_logs.py evidence/before-batch.json < evidence/before.jsonl
python3 -c "from pathlib import Path; print(Path('release-record.md').read_text())"
```

**Evidence:** capture actual commands/results requested above and add a short cause/fix/result caption. Extra screenshots are allowed when output cannot fit readably. At least one labelled screenshot per task; one screenshot need not contain all checks.

## Task 2: Perform and verify local rollback (7 marks, ~12 minutes)

Change RELEASE selector only to supplied known-good variant; recreate API using SAME prepared image, no rebuild. Record rollback time. Run same-size after batch and query only its request IDs. Prove five HTTP200 successes, zero error events within new batch, /health200 and healthy container. Do not claim old historical errors disappeared. This is a local bundled-variant rollback, not an image-registry or cloud rollback.

```sh
# After release.env edit:
date '+%Y-%m-%dT%H:%M:%S%z'
docker compose up -d --force-recreate --no-build api
# Wait for listener and up to 15 seconds for healthy status.
python3 batch.py after
docker compose logs --no-color --no-log-prefix api > evidence/after.jsonl
python3 batch_logs.py evidence/after-batch.json < evidence/after.jsonl
python3 http_get.py http://localhost:18094/health
docker compose ps
date '+%Y-%m-%dT%H:%M:%S%z'
```

**Evidence:** capture actual commands/results requested above and add a short cause/fix/result caption. Extra screenshots are allowed when output cannot fit readably. At least one labelled screenshot per task; one screenshot need not contain all checks.

## Task 3: Write short evidence-backed postmortem (7 marks, ~12 minutes)

Complete five sections in postmortem.md (1–2 sentences each): actual local detection/rollback/verification timestamps with timezone; measured before/after failed totals; operational cause connecting release record to observed log (not just symptom); recovery target and batch/health proof; one concrete prevention control. Be blameless. Do not invent users, incident duration, root-code analysis or production deployment.

```sh
# Fill postmortem.md using actual observations, not supplied invented timestamps.
python3 -c "from pathlib import Path; print(Path('postmortem.md').read_text())"
```

**Evidence:** capture actual commands/results requested above and add a short cause/fix/result caption. Extra screenshots are allowed when output cannot fit readably. At least one labelled screenshot per task; one screenshot need not contain all checks.

## Submission: one PDF only

Three labelled task sections with readable genuine terminal screenshots, requested written findings, and complete diff of permitted files once. No PR, video, ZIP or separate code upload. Retain evidence locally; only PDF is uploaded. Tool choice for PDF assembly is unrestricted; export/print labelled screenshots and text to PDF. Do not expose secrets or personal data. No separate marks for filename, URLs, fork ownership, branch labels or submission commit IDs. An instructor standalone reference is valid under identical technical criteria.

The scored work is exactly the three tasks above. No hidden rubric requirements, duplicate deductions or automatic whole-submission zero for an unrelated missing item. Technical request IDs and release values requested within tasks ARE evidence, not submission metadata. Score missing technical evidence only against its corresponding subcriterion.

## Evaluation rubric

| Task | Explicit task criteria | Marks |
|---|---|---|
| Task 1 | Failed batch and measured impact (2); matching request/release log evidence and supplied record (2); justified rollback decision (2). | 6 |
| Task 2 | Correct selector/minimal diff (2); new batch five successes/no error events (3); health200 and healthy status (2). | 7 |
| Task 3 | Observed timeline (1); measured impact (1); evidence-backed operational cause (2); recovery proof (1); concrete prevention control (2). | 7 |

**Total: 6 + 7 + 7 = 20.** Written alternatives accepted when technically correct and supported by requested evidence. No cloud execution required or credited.

## Cleanup (after evidence capture)

```sh
docker compose down
```

Remove only exercise resources, never unrelated containers or images. Source code, supplied fixtures and helper scripts outside allowed edits must remain unchanged.
