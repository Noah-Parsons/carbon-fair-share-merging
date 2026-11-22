from pathlib import Path
import pandas as pd, numpy as np
DATA = Path(__file__).resolve().parent / 'data' / 'owid-co2.csv'
d=pd.read_csv(DATA)
c=d[d.iso_code.notna() & (d.iso_code.str.len()==3) & ~d.iso_code.str.startswith('OWID')]
y=c[c.year==2022].dropna(subset=['population','gdp']).set_index('iso_code')
EU=['AUT','BEL','BGR','HRV','CYP','CZE','DNK','EST','FIN','FRA','DEU','GRC','HUN','IRL','ITA','LVA','LTU','LUX','MLT','NLD','POL','PRT','ROU','SVK','SVN','ESP','SWE']
AU=[i for i in ['DZA','AGO','BEN','BWA','BFA','BDI','CPV','CMR','CAF','TCD','COM','COG','COD','CIV','DJI','EGY','GNQ','ERI','SWZ','ETH','GAB','GMB','GHA','GIN','GNB','KEN','LSO','LBR','LBY','MDG','MWI','MLI','MRT','MUS','MAR','MOZ','NAM','NER','NGA','RWA','STP','SEN','SYC','SLE','SOM','ZAF','SSD','SDN','TZA','TGO','TUN','UGA','ZMB','ZWE'] if i in y.index]
def bloc_effect(members, phi, name):
    g=y.loc[members]; P=g.population; z=g.gdp/g.population
    sep=(P*phi(z)).sum(); Pt=P.sum(); zt=g.gdp.sum()/Pt; mer=Pt*phi(zt)
    return sep, mer
for name,members in [('EU27',EU),('African Union (with data)',AU)]:
    g=y.loc[members]; z=g.gdp/g.population; w=g.population/g.population.sum()
    am=(w*z).sum(); hm=1/(w/z).sum()
    s,m=bloc_effect(members, lambda z:1/z, name)
    print(f'{name}: n={len(members)}  Approach 2 weight separate/merged = {s/m:.4f};  pop-weighted AM/HM of GDP per capita = {am/hm:.4f}')
    T=7500.0
    s2,m2=bloc_effect(members, lambda z:np.maximum(0,z-T), name)
    ratio = f'{s2/m2:.4f}' if m2 > 0 else 'undefined (the merged bloc is below T and has zero capacity)'
    print(f'   GDR-style capacity with national averages (T={T:.0f}): separate {s2:.4g}, merged {m2:.4g}, ratio {ratio}  (members below T: {(z<T).sum()})')

def shares(members):
    w=y.population**2/y.gdp; S=w.sum(); ws=w.loc[members].sum()
    P=y.loc[members].population.sum(); G=y.loc[members].gdp.sum(); wm=P**2/G
    return ws/S, wm/(S-ws+wm)
for name,m in [('EU27',EU),('AU',AU)]:
    a,b=shares(m); print(f'{name} Approach 2 share of global positive emissions: separate {a*100:.2f}%  as one bloc {b*100:.2f}%')
