# Recover a Release and Document Incident Evidence

CheckoutGuard fails checkout requests after a supplied release change, while its shallow health endpoint remains green. Establish evidence, restore bundled known-good release variant and document measured local recovery.

**Starter repository:** https://github.com/kalviumcommunity/checkoutguard-incident-recovery  
**Allowed edits:** release.env: RELEASE value only; postmortem.md: five short sections. Preserve app variants, log helpers, request batch, health probe and supplied release record.

## Prerequisites and startup

Use Python 3.10+ on host, Git, Docker Engine/Desktop and Compose v2 (supports --no-log-prefix). Linux/macOS or prepared WSL. No pip packages, jq, paid tools, registry credentials or cloud account required. Docker Desktop subject to its license; free Linux Docker Engine sufficient.

Clone supplied repo (fork optional), enter directory and reserve host port 18094. Build and start:

```sh
docker pull python:3.12-slim
# No additional monitoring image needed.
docker compose config --quiet
docker compose build
mkdir -p evidence
docker compose up -d
```

Wait up to 15 seconds for listeners/probes/scrapes before diagnosing. Initial task faults are intentional, not setup failures. Commands run from repo root. Host evidence/ is ignored. Use a fresh exercise stack with no unrelated traffic. Do not edit helpers to force checks to pass.

## Task 1: Establish incident evidence

Run before batch of five checkout requests; save and query records belonging to those request IDs. Compare observed release/error with release-record.md. State measured failed/total requests and evidence-supported rollback decision. Healthy liveness alone does not establish checkout success. Record actual local detection time with timezone.

```sh
date '+%Y-%m-%dT%H:%M:%S%z'
python3 batch.py before
docker compose logs --no-color --no-log-prefix api > evidence/before.jsonl
python3 batch_logs.py evidence/before-batch.json < evidence/before.jsonl
python3 -c "from pathlib import Path; print(Path('release-record.md').read_text())"
```


## Task 2: Perform and verify local rollback

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


## Task 3: Write short evidence-backed postmortem

Complete five sections in postmortem.md (1–2 sentences each): actual local detection/rollback/verification timestamps with timezone; measured before/after failed totals; operational cause connecting release record to observed log (not just symptom); recovery target and batch/health proof; one concrete prevention control. Be blameless. Do not invent users, incident duration, root-code analysis or production deployment.

```sh
# Fill postmortem.md using actual observations, not supplied invented timestamps.
python3 -c "from pathlib import Path; print(Path('postmortem.md').read_text())"
```


## Cleanup

```sh
docker compose down
```

Remove only resources created for this exercise. Preserve supplied fixtures and helpers; do not bypass checks or fabricate results.
