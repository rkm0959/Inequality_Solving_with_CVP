from Crypto.Cipher import AES, PKCS1_OAEP
from Crypto.PublicKey import RSA
from Crypto.Util.Padding import pad, unpad
from Crypto.Util.number import inverse, long_to_bytes, bytes_to_long, isPrime, getPrime
from tqdm import tqdm
from pwn import *
from sage.all import *
import sys, json, hashlib, os, math, time, base64, binascii, string
import random as rd # avoid confusion with sage
import multiprocessing as mp


def ceil(n, m): # returns ceil(n/m)
	return (n + m - 1) // m

def is_inside(L, R, M, val): # is L <= val <= R in mod M context?
	if L <= R:
		return L <= val <= R
	else:
		R += M
		if L <= val <= R:
			return True
		if L <= val + M <= R:
			return True 
		return False

## some notes : it's good idea to check for gcd(A, M) = 1
## in CTF context, if gcd(A, M) != 1, we can factorize M and sometimes we can solve the challenge
## in competitive programming context, we need to check gcd(A, M) = 1 and decide whether solution even exists..
def optf(A, M, L, R): # minimum nonnegative x s.t. L <= Ax mod M <= R
	if L == 0:
		return 0
	if 2 * A > M:
		L, R = R, L
		A, L, R = M - A, M - L, M - R
	cc_1 = ceil(L, A)
	if A * cc_1 <= R:
		return cc_1
	cc_2 = optf(A - M % A, A, L % A, R % A)
	return ceil(L + M * cc_2, A)

# check if L <= Ax (mod M) <= R has a solution
def sol_ex(A, M, L, R):
	if L == 0 or L > R:
		return True
	g = GCD(A, M)
	if (L - 1) // g == R // g:
		return False
	return True

## find all solutions for L <= Ax mod M <= R, S <= x <= E:
def solve(A, M, L, R, S, E):
	# this is for estimate only : if very large, might be a bad idea to run this
	if sol_ex(A, M, L, R) == False:
		return []
	cur = S - 1
	ans = []
	num_sol = 0
	while cur <= E:
		NL = (L - A * (cur + 1)) % M
		NR = (R - A * (cur + 1)) % M
		if NL > NR:
			cur += 1
		else:
			val = optf(A, M, NL, NR)
			cur += 1 + val
		if cur <= E:
			ans.append(cur)
			# remove assert for performance if needed
			assert is_inside(L, R, M, (A * cur) % M)
			num_sol += 1
	return ans
                                                                                               
p = 403564885370838178925695432427367491470237155186244212153913898686763710896400971013343861778118177227348808022449550091155336980246939657874541422921996385839128510463                                                                                                                                                                                                                                                                                                                                                            
pub = 246412225456431779180824199385732957003440696667152337864522703662113001727131541828819072458270449510317065822513378769528087093456569455854781212817817126406744124198
r = 195569213557534062135883086442918136431967939088647809625293990874404630325238896363416607124844217333997865971186768485716700133773423095190740751263071126576205643521                                                                                                                                                                                                                                                                                                                                                               
s = 156909661984338007650026461825579179936003525790982707621071330974873615448305401425316804780001319386278769029432437834130771981383408535426433066382954348912235133967
g = 3


message = b"blockchain-ready deterministic signatures"
h = int(hashlib.sha256(message).hexdigest(), 16)  

'''
priv = x * ((1 << 256) + 1)
k = (1 << 256) * y + h + small
sk == -r * priv + h (mod (p-1)/2)
s(1<<256) y + sh + s * small == -rx(1<<256) - rx + h (mod (p-1)/2)
'''

for small in tqdm(range(1, 5000)):
    N = (p-1) // 2
    A = (s * (1 << 256)) % N
    B = (r * ((1 << 256) + 1)) % N
    Target = (h - s * h - s * small) % N
    Mul = (A * inverse(B, N)) % N
    TT = (Target * inverse(B, N)) % N
    res = solve(Mul, N, TT - (1 << 256), TT, 0, 1 << 256)
    if len(res) == 0:
        continue
    y = res[0]
    x = (TT - Mul * y) % N
    priv = (x * ((1 << 256) + 1))
    if pow(3, priv, p) == pub:
        print(str(priv))
        break