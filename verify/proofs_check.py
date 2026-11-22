# Independent numerical checks of the propositions in the carbon paper.
import numpy as np
rng=np.random.default_rng(1)
def alloc(w,B=1.0): w=np.asarray(w,float); return B*w/w.sum()
fails={}
def chk(name,cond):
    fails.setdefault(name,0)
    if not cond: fails[name]+=1
for trial in range(20000):
    n=rng.integers(3,9); P=rng.uniform(0.1,100,n); Y=rng.uniform(0.1,100,n)*P*rng.uniform(0.05,5,n); H=rng.uniform(0,50,n)
    S=rng.choice(n,size=rng.integers(2,n),replace=False); R=np.setdiff1d(np.arange(n),S)
    def merged(wf):
        wS=wf(P[S].sum(),Y[S].sum(),H[S].sum()); wR=wf(P[R],Y[R],H[R])
        sep=alloc(wf(P,Y,H))[S].sum(); mer=alloc(np.r_[wS,wR])[0]; return sep,mer
    # Prop 1: linear non-negative weight -> merging-proof
    c=rng.uniform(0,3,3); lin=lambda p,y,h: c[0]*p+c[1]*y+c[2]*h
    s,m=merged(lin); chk('P1 linear merging-proof',abs(s-m)<1e-12)
    # Prop 1 (ii) level consistency for linear
    w=lin(P,Y,H); direct=alloc(w)[S]; td=alloc(np.r_[lin(P[S].sum(),Y[S].sum(),H[S].sum()),lin(P[R],Y[R],H[R])])[0]*w[S]/w[S].sum()
    chk('P1 linear level-consistent',np.allclose(direct,td,atol=1e-12))
    # Thm 2: convex phi(y)=1/y -> separate >= merged
    cap=lambda p,y,h: p*p/y
    s,m=merged(cap); chk('T2 convex 1/y splitting favoured',s>=m-1e-15)
    # concave phi(y)=sqrt(y) -> merged >= separate
    conc=lambda p,y,h: p*np.sqrt(y/p)
    s,m=merged(conc); chk('T2 concave merging favoured',m>=s-1e-15)
    # Cor 1 identity AM/HM
    lam=P[S]/P[S].sum(); yv=Y[S]/P[S]; am=(lam*yv).sum(); hm=1/(lam/yv).sum()
    chk('C1 AM/HM identity',abs((P[S]**2/Y[S]).sum()/(P[S].sum()**2/Y[S].sum())-am/hm)<1e-9*am/hm)
    # Thm 1 sanity: truncated linear weight with negative income coeff is not merging-proof in general (count only)
print(fails)
# Theorem 1 counterexample existence for truncated rule: max(0, a*P - b*Y)
P=np.array([1.,1.,1.]); Y=np.array([0.5,3.,1.]); f=lambda p,y: np.maximum(0,2*p-y)
sep=alloc(f(P,Y))[:2].sum(); mer=alloc(np.r_[f(P[:2].sum(),Y[:2].sum()),f(P[2],Y[2])])[0]
print('truncated capability rule, parties 1+2: separate',round(sep,4),'merged',round(mer,4))
