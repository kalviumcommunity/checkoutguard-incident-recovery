"""Five sequential checkout requests. Labels identify evidence; results measured live."""
import json,urllib.request,urllib.error,sys
label=sys.argv[1]
assert label in ["before","after"]
records=[]
for _ in range(5):
    try:
        with urllib.request.urlopen("http://localhost:18094/checkout",timeout=3) as r:status=r.status;body=json.loads(r.read())
    except urllib.error.HTTPError as r:status=r.code;body=json.loads(r.read())
    records.append({"http_status":status,**body})
    print(json.dumps(records[-1]))
with open("evidence/"+label+"-batch.json","w") as f:json.dump(records,f,indent=2)
print("BATCH_TOTAL="+str(len(records))+" FAILED="+str(sum(r["http_status"]>=500 for r in records)))
