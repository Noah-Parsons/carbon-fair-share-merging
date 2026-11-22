from pathlib import Path
import pandas as pd, numpy as np
DATA = Path(__file__).resolve().parent / 'data' / 'owid-co2.csv'
d=pd.read_csv(DATA)
c=d[d.iso_code.notna() & (d.iso_code.str.len()==3) & ~d.iso_code.str.startswith('OWID')]
EU=['AUT','BEL','BGR','HRV','CYP','CZE','DNK','EST','FIN','FRA','DEU','GRC','HUN','IRL','ITA','LVA','LTU','LUX','MLT','NLD','POL','PRT','ROU','SVK','SVN','ESP','SWE']
y=c[c.year==2022].dropna(subset=['population','gdp'])
print('countries with pop+gdp 2022:',len(y), 'EU present:',y.iso_code.isin(EU).sum())
w=y.population**2/y.gdp            # Approach 2: population / GDP per capita
S=w.sum()
sep=w[y.iso_code.isin(EU).values].sum()/S
P=y[y.iso_code.isin(EU)].population.sum(); G=y[y.iso_code.isin(EU)].gdp.sum()
wm=P**2/G; Sm=S-w[y.iso_code.isin(EU).values].sum()+wm
merged=wm/Sm
print(f'Approach 2, 2022 data: EU members assessed separately: {sep*100:.3f}% of global positive emissions')
print(f'EU assessed as one bloc: {merged*100:.3f}%   ratio separate/merged = {sep/merged:.3f}')
# Approach 1-style historical budget 1950-2022, equal per capita of actual global emissions, 1.5% discount
h=c[(c.year>=1950)&(c.year<=2022)].dropna(subset=['population','co2'])
wld=d[(d.country=='World')&(d.year>=1950)&(d.year<=2022)].set_index('year')
disc=lambda t: (1.015)**(-(2022-t))
h=h.assign(ew=h.year.map(wld.co2)*h.population/h.year.map(wld.population)*h.year.map(disc), ei=h.co2*h.year.map(disc))
b=h.groupby('iso_code').apply(lambda g:(g.ew-g.ei).sum())
be=b[b.index.isin(EU)]
print(f'\nApproach 1 historical balance 1950-2022 (GtCO2, discounted): EU members negative: {(be<0).sum()} of {len(be)}')
print(f'sum of truncated member balances  sum max(0,b_i) = {be.clip(lower=0).sum()/1e3:.2f} Gt')
print(f'truncated balance of the bloc      max(0, sum b_i) = {max(0,be.sum())/1e3:.2f} Gt   (sum b_i = {be.sum()/1e3:.2f} Gt)')
print(be.sort_values().head(6).round(0))
