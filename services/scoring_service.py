
WEIGHTS={"revenue":.3,"pain":.25,"competition":.15,"ai":.1,"solo":.1,"trend":.1}
def score(x):
    return round(sum(x[k]*v for k,v in WEIGHTS.items()),2)
