import sys, json, openpyxl
wb = openpyxl.load_workbook(sys.argv[1]); ws = wb["Sheet1"]
LV = {"FFD9EAD3": "fo", "FFFFF2CC": "extra", "FFF4CCCC": "nem"}
segs = ["szinhaz", "rendezveny", "szalloda", "muzeum"]
out = []
for r in range(2, ws.max_row + 1):
    name = " ".join(str(ws.cell(r, 1).value).split())
    row = {"excel_sor": r, "excel_nev": name}
    for i, s in enumerate(segs):
        c = ws.cell(r, 2 + i)
        row[s] = LV[c.fill.fgColor.rgb]
    out.append(row)
json.dump(out, open(sys.argv[2], "w"), ensure_ascii=False, indent=1)
for o in out: print(f'{o["excel_nev"][:42]:44s}', *[f'{o[s]:6s}' for s in segs])
