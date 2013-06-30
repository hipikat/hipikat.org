
g = globals()
s = lambda k, *v: g.setdefault(k, v[0]) if len(v) else g.get(k)
