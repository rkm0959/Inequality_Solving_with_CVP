from Crypto.Util.number import GCD, long_to_bytes
from tqdm import tqdm

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
## in CTF context, if gcd(A, M) != 1, we can factorize M and we can solve the challenge
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

N = 124588792854585991543122421017579759242707321792822503200983206042530513248160179498235727796077646122690756838184806567078369714502863053151565317001149999657802192888347495811627518984421857644550440227092744651891241056244522365071057538408743656419815042273198915328775318113249292516318084091006804073157
e = 109882604549059925698337132134274221192629463500162142191698591870337535769029028534472608748886487359428031919436640522967282998054300836913823872240009473529848093066417214204419524969532809574214972094458725753812433268395365056339836734440559680393774144424319015013231971239186514285386946953708656025167
gift = 870326170979229749948990285479428244545993216619118847039141213397137332130507928675398
enc = 67594553703442235599059635874603827578172490479401786646993398183588852399713973330711427103837471337354320292107030571309136139408387709045820388737058807570181494946004078391176620443144203444539824749021559446977491340748598503240780118417968040337516983519810680009697701876451548797213677765172108334420
 
R = (-e * (gift << 120)) % N
L = (-e * (gift << 120) - 3 * (int)(N ** 0.9)) % N

val = solve(e, N, L, R, 0, 1 << 120)
num_sol = len(val)

for i in tqdm(range(num_sol)):
	d = (gift << 120) + val[i]
	s = long_to_bytes(pow(enc, d, N))
	if s[:5] == b"pbctf":
		print(s)
