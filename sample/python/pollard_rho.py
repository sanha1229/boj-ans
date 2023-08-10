from math import gcd, log2, floor, sqrt
from random import random

def mrpt_seg (n, a):
    d = n-1 
    r = 0
    while d % 2 == 0:
        d >>= 1
        r += 1
    t = pow(a, d, n)
    if t == 1 or t == n-1:
        return 1
    for i in range(r-1):
        t = pow(t, 2, n)
        if t == n-1:
            return 1
    return 0
	
def mrpt (n):
    tmp = 0
    prime = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41]
    if n in prime:
        return 1
    if n % 2 == 0:
        return 0
    for a in prime:
        if not mrpt_seg(n, a):
            return 0
    return 1

def numadd (a, b, p = 0):
    if p == 0:
        return a+b
    return (a+b)%p

def nummul (a, b, p = 0):
    if p == 0:
        return a*b
    return a*b%p

def rho_seg (n, x, c = 1):
    if n == 1:
        return 0
    if n % 2 == 0:
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
            x = floor((random()*log2(n+1)))+2
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

def tet2_seg (x, i, m):
    if m == 1:
        return 1
    if i == len(x)-1:
        return x[i]

    t = tet2_seg(x, i+1, phi(m))

    if x[i]**t < m:
        return modpow(x[i], t, m)
    else:
        return modpow(x[i], t, m) + m

def tetration2 (x, m):
    if len(x) == 1: return x[0] % m
    if m == 1: return 1

    phi_m = phi(m)
    return modpow(x[0], tet2_seg(x, 1, phi(m)), m)

def tet3_seg (x, i, m):
    if m == 1:
        return 1

    if i == len(x)-1:
        return x[i]

    t = tet3_seg(x, i+1, phi(m))
    u = modpow(x[i], t, m)

    return u if u else m

def tetration3 (x, m):
    if len(x) == 1: return x[0] % m
    if m == 1: return 1

    phi_m = phi(m)
    return modpow(x[0], tet3_seg(x, 1, phi(m)), m)
