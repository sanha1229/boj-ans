from math import gcd

def mrpt_seg (n, a):
    d = ~-n
    r = 0
    while -~d & 1:
        d >>= 1
        r += 1
    t = pow(a, d, n)
    if t == 1 or t == ~-n:
        return 1
    for i in range(~-r):
        t = pow(t, 2, n)
        if t == ~-n:
            return 1
    return 0
	
def mrpt (n):
    tmp = 0
    prime = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41]
    if n in prime:
        return 1
    if -~n & 1:
        return 0
    for a in prime:
        if not mrpt_seg(n, a):
            return 0
    return 1

def numadd (a, b, m = 0):
    if not m:
        return a+b
    return (a+b) % m

def nummul (a, b, m = 0):
    if not m:
        return a*b
    return ((a%m) * (b%m)) % m

def rho_seg (n, x, c = 1):
    if n == 1:
        return 0
    if -~n & 1:
        return 2
    if mrpt(n):
        return n
		
    y = x
    d = 1

    while d == 1:
        x = numadd(nummul(x, x, n), c, n)
        y = numadd(nummul(y, y, n), c, n)
        y = numadd(nummul(y, y, n), c, n)
		
        d = gcd(abs(x-y), n)
		
    if d == n:
        return rho_seg(d, x, -c if c > 0 else -c+1)
    else:
        if mrpt(d):
            return d
        else:
            return rho_seg(d, x)		

def plr (n, return_dict = 0):
    x = 2
    if return_dict:
        res = {}
    else:
        res = []
    while n > 1:
        p = rho_seg(n, x)
        if p:
            if return_dict:
                if p in res:
                    res[p] += 1
                else:
                    res[p] = 1
            else:
                res.append(p)
            n //= p
            if n == 1:
                return res
            if mrpt(n):
                if return_dict:
                    if n in res:
                        res[n] += 1
                    else:
                        res[n] = 1
                else:
                    res.append(n)
                return res
        else:
            x = 0
    return res

def phi (n):
    res = n
    pr = plr(n, return_dict=1)
    for k in pr:
        res *= k-1
        res //= k
    return res

def divisor (n):
    res = []
    pr = plr(n, return_dict=1)

    s = ''
    t = []

    i = 0
    for k in pr:
        s += ' '*i + f'for p_{i} in range({pr[k]+1}):\n'
        t.append(f'({k}**p_{i})')
        i += 1

    s += ' '*i + f'res.append({"*".join(t)})'
    exec(s)

    return res

def modpow (a, x, p):
    if x == 0:
        return 1
    _t = modpow(a, x//2, p)
    if x % 2 == 1:
        return _t*_t*a % p
    else:
        return _t*_t % p

def tet_seg (x, i, m):
    if m == 1:
        return 1
    if i == len(x)-1:
        return x[i]

    t = tet_seg(x, i+1, phi(m))

    if t*log2(x[i]) < log2(m):
        return modpow(x[i], t, m)
    else:
        return modpow(x[i], t, m) + m

def tetration (x, m, seg=1):
    if len(x) == 1: return x[0] % m
    return modpow(x[0], tet_seg(x, 1, phi(m)), m)
