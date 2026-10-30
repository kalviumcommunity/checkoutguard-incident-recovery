"""Select only application logs belonging to saved batch request IDs."""
import json,sys
with open(sys.argv[1]) as f:ids={r["request_id"] for r in json.load(f)}
rows=[json.loads(l) for l in sys.stdin if l.strip()]
rows=[r for r in rows if r.get("request_id") in ids]
for r in rows:print(json.dumps(r))
print("MATCHED="+str(len(rows))+" ERRORS="+str(sum(r["level"]=="error" for r in rows)))
assert len(rows)==len(ids),"Missing request records"
