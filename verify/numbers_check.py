# Independent recomputation using the csv module only (no shared code with merge.py / convexity.py)
import csv
from pathlib import Path
DATA = Path(__file__).resolve().parent.parent / 'data' / 'owid-co2.csv'
rows=[r for r in csv.DictReader(open(DATA, newline='', encoding='utf-8')) if r['year']=='2022']
data={}
for r in rows:
    iso=r['iso_code']
    if len(iso)==3 and not iso.startswith('OWID') and r['population'] and r['gdp']:
        data[iso]=(float(r['population']),float(r['gdp']))
EU="AUT BEL BGR HRV CYP CZE DNK EST FIN FRA DEU GRC HUN IRL ITA LVA LTU LUX MLT NLD POL PRT ROU SVK SVN ESP SWE".split()
AU=[i for i in "DZA AGO BEN BWA BFA BDI CPV CMR CAF TCD COM COG COD CIV DJI EGY GNQ ERI SWZ ETH GAB GMB GHA GIN GNB KEN LSO LBR LBY MDG MWI MLI MRT MUS MAR MOZ NAM NER NGA RWA STP SEN SYC SLE SOM ZAF SSD SDN TZA TGO TUN UGA ZMB ZWE".split() if i in data]
print('countries',len(data),'EU',sum(i in data for i in EU),'AU with data',len(AU))
W={i:p*p/g for i,(p,g) in data.items()}; tot=sum(W.values())
for name,m in (('EU',EU),('AU',AU)):
    ws=sum(W[i] for i in m); P=sum(data[i][0] for i in m); G=sum(data[i][1] for i in m); wm=P*P/G
    print(name,'separate %.3f%%'%(100*ws/tot),'bloc %.3f%%'%(100*wm/(tot-ws+wm)),'weight ratio %.4f'%(ws/wm))
