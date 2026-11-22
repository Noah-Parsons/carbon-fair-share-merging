import csv
from pathlib import Path
DATA = Path(__file__).resolve().parent.parent / 'data' / 'owid-co2.csv'
from collections import defaultdict
EU=set("AUT BEL BGR HRV CYP CZE DNK EST FIN FRA DEU GRC HUN IRL ITA LVA LTU LUX MLT NLD POL PRT ROU SVK SVN ESP SWE".split())
world={}; bal=defaultdict(float)
rows=list(csv.DictReader(open(DATA, newline='', encoding='utf-8')))
for r in rows:
    if r['country']=='World' and r['co2'] and r['population'] and 1950<=int(r['year'])<=2022:
        world[int(r['year'])]=(float(r['co2']),float(r['population']))
for r in rows:
    if r['iso_code'] in EU and r['co2'] and r['population']:
        t=int(r['year'])
        if 1950<=t<=2022:
            d=1.015**(-(2022-t)); Ew,Pw=world[t]
            bal[r['iso_code']]+=(Ew*float(r['population'])/Pw-float(r['co2']))*d
neg=sum(v<0 for v in bal.values())
print('EU members',len(bal),'negative',neg,'sum max(0,b) Gt %.2f'%(sum(max(0,v) for v in bal.values())/1e3),'sum b Gt %.2f'%(sum(bal.values())/1e3))
