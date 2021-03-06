from Crypto.Util.number import GCD

## L <= Ax mod M <= R means Ax mod M lies inside the "circular arc" between L and R
## to visualize, think of 0 ~ M lying on a circle - the key is that for example,
## M-2 <= Ax mod M <= 2 means [Ax mod M = M-2, M-1, 0, 1, 2] : hopefully you get the idea...

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
	print("Expected Number of Solutions : ", ((E - S + 1) * (R - L + 1)) // M + 1)
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
	print("Actual Number of Solutions : ", num_sol)
	return ans

