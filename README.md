# Fair Shares That Depend on How Countries Are Counted

Noah Parsons, as of 22 November 2026

Code and data for the paper *Fair Shares That Depend on How Countries Are Counted: Merging, Splitting and the Allocation of the Carbon Budget* (`fairshare_merging.pdf`, source `fairshare_merging.tex`).

## Question

Equity-based assessments divide a global emissions budget among countries using indicators such as population, income and historical emissions, and they are applied to blocs such as the European Union as well as to their members. Does a party's fair share change when the same people, income and emissions are counted as one party rather than several?

## Results

- For rules that give each party a share proportional to a weight computed from its indicators, the result is unaffected by merging or splitting if and only if the weight is linear in the indicators (a special case of Ju, Miyagawa and Sakai, 2007).
- No such rule can at once keep every allocation non-negative, give less to parties with higher income or higher historical emissions, and be unaffected by merging or splitting.
- When the weight is population times a function of per-capita indicators, convex functions reward splitting and concave ones reward merging.
- For the capability approach in which shares are proportional to population divided by income per head, the ratio of a group's total assessed separately to its total as one bloc is the population-weighted arithmetic mean of its members' incomes per head divided by their harmonic mean.

With 2022 data:

| Group | Share assessed separately | Share as one bloc | Ratio |
|---|---|---|---|
| European Union (27) | 1.02% | 0.98% | 1.045 |
| African Union (50 members with data) | 47.4% | 31.0% | 2.005 |

Truncating cumulative-per-capita budgets at zero: 25 of the 27 EU members have negative balances; their positive balances sum to 0.15 Gt when truncated separately, while the EU's combined balance is −68 Gt, which truncates to zero.

## Files

| Path | Contents |
|---|---|
| `fairshare_merging.pdf`, `fairshare_merging.tex` | The paper |
| `merge.py` | EU and African Union shares under the capability approach, and the truncated cumulative-per-capita balances |
| `convexity.py` | Bloc effects, the arithmetic/harmonic mean identity, and a capacity-above-threshold example |
| `verify/proofs_check.py` | Checks of the propositions on 20,000 random instances |
| `verify/numbers_check.py` | Independent recomputation of the shares using the `csv` module only, sharing no code with the analysis scripts |
| `verify/ecpc_check.py` | Independent recomputation of the truncated cumulative-per-capita balances |
| `data/owid-co2.csv` | Our World in Data CO₂ and greenhouse gas emissions dataset, downloaded 22 November 2026 |

## Reproducing

Requires Python 3 with `numpy` and `pandas` (tested with Python 3.12, numpy 2.4 and pandas 3.0). The scripts can be run from any directory.

```bash
python merge.py
python convexity.py
python verify/proofs_check.py
python verify/numbers_check.py
python verify/ecpc_check.py
```

`proofs_check.py` should report 0 failures for every check.

## Data

`data/owid-co2.csv` is from [Our World in Data](https://github.com/owid/co2-data), used under the Creative Commons BY 4.0 licence. It is included so that the figures above can be reproduced exactly; later versions of the dataset may give slightly different numbers.

## AI assistance

The analysis code and drafts were produced with the help of an AI assistant (Claude, made by Anthropic).
