"""Read a saved JSONL application log: validate, errors, or request REQUEST_ID."""
import json,sys
mode=sys.argv[1]
records=[json.loads(line) for line in sys.stdin if line.strip()]
assert all(isinstance(r,dict) and all(k in r for k in ["timestamp","level","message","request_id"]) for r in records)
if mode=="validate":
    print("VALID_JSON_RECORDS="+str(len(records)))
    assert records, "No application records supplied"
elif mode=="errors":
    for r in records:
        if r["level"]=="error": print(json.dumps(r))
elif mode=="request":
    for r in records:
        if r["request_id"]==sys.argv[2]: print(json.dumps(r))
else: raise SystemExit("Use validate, errors, or request REQUEST_ID")
