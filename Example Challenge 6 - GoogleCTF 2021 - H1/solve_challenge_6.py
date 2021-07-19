from Crypto.Cipher import AES, PKCS1_OAEP, PKCS1_v1_5
from Crypto.PublicKey import RSA
from Crypto.Util.number import inverse, long_to_bytes, bytes_to_long, isPrime, getPrime, GCD
from tqdm import tqdm
from pwn import *
from sage.all import *
import itertools, sys, json, hashlib, os, math, time, base64, binascii, string, re, struct, datetime, subprocess
import numpy as np
import random as rand
import multiprocessing as mp
from base64 import b64encode, b64decode
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from sage.modules.free_module_integer import IntegerLattice

def Babai_CVP(mat, target):
	M = IntegerLattice(mat, lll_reduce=True).reduced_basis
	G = M.gram_schmidt()[0]
	diff = target
	for i in reversed(range(G.nrows())):
		diff -=  M[i] * ((diff * G[i]) / (G[i] * G[i])).round()
	return target - diff

def solve(mat, lb, ub, weight = None):
	num_var  = mat.nrows()
	num_ineq = mat.ncols()

	max_element = 0 
	for i in range(num_var):
		for j in range(num_ineq):
			max_element = max(max_element, abs(mat[i, j]))

	if weight == None:
		weight = num_ineq * max_element

    # sanity checker
	if len(lb) != num_ineq:
		print("Fail: len(lb) != num_ineq")
		return

	if len(ub) != num_ineq:
		print("Fail: len(ub) != num_ineq")
		return

	for i in range(num_ineq):
		if lb[i] > ub[i]:
			print("Fail: lb[i] > ub[i] at index", i)
			return

    	# heuristic for number of solutions
	DET = 0

	if num_var == num_ineq:
		DET = abs(mat.det())
		num_sol = 1
		for i in range(num_ineq):
			num_sol *= (ub[i] - lb[i])
		if DET == 0:
			print("Zero Determinant")
		else:
			num_sol //= DET
			# + 1 added in for the sake of not making it zero...
			print("Expected Number of Solutions : ", num_sol + 1)

	# scaling process begins
	max_diff = max([ub[i] - lb[i] for i in range(num_ineq)])
	applied_weights = []

	for i in range(num_ineq):
		ineq_weight = weight if lb[i] == ub[i] else max_diff // (ub[i] - lb[i])
		applied_weights.append(ineq_weight)
		for j in range(num_var):
			mat[j, i] *= ineq_weight
		lb[i] *= ineq_weight
		ub[i] *= ineq_weight

	# Solve CVP
	target = vector([(lb[i] + ub[i]) // 2 for i in range(num_ineq)])
	result = Babai_CVP(mat, target)

	for i in range(num_ineq):
		if (lb[i] <= result[i] <= ub[i]) == False:
			print("Fail : inequality does not hold after solving")
			break
    
    	# recover x
	fin = None

	if DET != 0:
		mat = mat.transpose()
		fin = mat.solve_right(result)
	
	## recover your result
	return result, applied_weights, fin

ra1, sa1, ca1 = (8618416354247009865173783322782283385800726568519779763790691157278063798628048418532907783021806238103423515210146966468025964847364086792099622893845216, 2932674107137731789093617068375500084388905453653468925392946088867116597531950960271857205235755778202380084260003117176704579423285955014316540314931750, 27865871384804321325511205140263204607)
rb1, sb1, cb1 = (6706720197123832142768727143395528571627385686729472279085077699672602636953568596628477227511870037092766007177588966333093607595831000050978265637877796, 1073779379108240410856990657565545229209771903946426639922087094813786902448520023335130808991515066506036954730763452318418336144389425011731474342543709, 111403492170712993917428321974111102656)
ra2, sa2, ca2 = (8832295267397231051293216564016639537146222596144354850230682204978731311879255662259663270183445827348338041752369314181111940713714991119349376636404112, 8683784208731634307361157916911868656279723101808163939313971801256736484458199874570532609285522391139002296248059424750941962344918156540408403221858292, 105398535464409171419472607677747462033030589690350997911381059472020486557672504778060748058626707326992258591478040500759349352824508941100030623708235493999018571171774658661651532338275358740821547158517615704187173346885098836066743736788259192831313414309775979590033581301910426314601982482556670097620)
rb2, sb2, cb2 = (7616464676048536081690041693308621105395807976530049374449777558721544903144139995398352331701243976154631946836252022822278420653297509476320989403738186, 7381293847317597354132365685036776332763847784351725370466906894121224725876600151244989563125805807680044723478850091886778158534219876869209592138625256, 7994736246642278834331127451449673561762900804586058657648578638831731501930073150317394505661139656896430884711113)

INF = (1, 1, 0)

mod = 8948962207650232551656602815159153422162609644098354511344597187200057010413552439917934304191956942765446530386427345937963894309923928536070534607816947
a = 6294860557973063227666421306476379324074715770622746227136910445450301914281276098027990968407983962691151853678563877834221834027439718238065725844264138
b = 3245789008328967059274849584342077916531909009637501918328323668736179176583263496463525128488282611559800773506973771797764811498834995234341530862286627 
n = 8948962207650232551656602815159153422162609644098354511344597187200057010413418528378981730643524959857451398370029280583094215613882043973354392115544169
G = (5139617820728399941653175323358137352238277428061991823713659546881441331696699723004749024403291797641521696406798421624364096550661311227399430098134141,
	 1798860115416690485862271986832828064808333512613833729548071279524320966991708554765227095605106785724406691559310536469721469398449016850588110200884962,
	 5042518522433577951395875294780962682755843408950010956510838422057522452845550974098236475624683438351211176927595173916071040272153903968536756498306512)

def get_z(msg):
	h = hashlib.sha512(msg)
	z = Transform(int.from_bytes(h.digest(), 'big'), h.digest_size*8)
	return z

def Double(p):
	x, y, z = p
	if z == 0 or y == 0:
		return INF
	ysqr = y * y % mod
	zsqr = z * z % mod
	s = 4 * x * ysqr % mod
	m = (3 * x * x + a * zsqr * zsqr) % mod
	x2 = (m * m - 2 * s) % mod
	y2 = (m * (s - x2) - 8 * ysqr * ysqr) % mod
	z2 = 2 * y * z % mod
	return x2, y2, z2

def Add(p, q):
	if p[2] == 0:
		return q
	if q[2] == 0:
		return p
	x1, y1, z1 = p
	x2, y2, z2 = q
	z1sqr = z1 * z1 % mod
	z2sqr = z2 * z2 % mod
	u1 = x1 * z2sqr % mod
	u2 = x2 * z1sqr % mod
	s1 = y1 * z2 * z2sqr % mod
	s2 = y2 * z1 * z1sqr % mod
	if u1 == u2:
		if s1 != s2:
			return INF
		else:
			return Double(p)
	h = u2 - u1 % mod
	hsqr = h * h % mod
	hcube = hsqr * h % mod
	r = s2 - s1 % mod
	t = u1 * hsqr % mod
	x3 = (r * r - hcube - 2 * t) % mod
	y3 = (r * (t - x3) - s1 * hcube) % mod
	z3 = h * z1 * z2 % mod
	return x3, y3, z3

def Multiply(p, x):
	if p == INF:
		return p
	res = INF
	while x:
		x, r = divmod(x, 2)
		if r:
			res = Add(res, p)
		p = Double(p)
	return res

def Transform(m, l):
	z = m
	shift = l - n.bit_length()
	if shift > 0:
		z >>= shift
	return z

def RNG(nbits, a, b):
	nbytes = nbits // 8
	B = os.urandom(nbytes)
	return a * sum([B[i] * b ** i for i in range(len(B))]) % 2**nbits

def Sign(msg, d):
	h = hashlib.sha512(msg)
	z = Transform(int.from_bytes(h.digest(), 'big'), h.digest_size*8)
	k = RNG(n.bit_length(), 16843009, 4294967296)
	x1, y1, z1 = Multiply(G, k)
	r = (x1 * pow(z1, -2, mod) % mod) % n
	s = pow(k, -1, n) * (z + r * d) % n
	return r, s

def Verify(msg, Q, r, s):
	h = hashlib.sha512(msg)
	z = Transform(int.from_bytes(h.digest(), 'big'), h.digest_size*8)
	u1 = z*pow(s, -1, n) % n
	u2 = r*pow(s, -1, n) % n
	x1, y1, z1 = Add(Multiply(G, u1), Multiply(Q, u2))
	return r == (x1 * pow(z1, -2, mod) % mod) % n

def Encrypt(plaintext, x):
	key = hashlib.sha256(str(x).encode()).digest()
	aes = algorithms.AES(key)
	encryptor = Cipher(aes, modes.ECB(), default_backend()).encryptor()
	padder = padding.PKCS7(aes.block_size).padder()
	padded_data = padder.update(plaintext) + padder.finalize()
	ciphertext = encryptor.update(padded_data) + encryptor.finalize()
	return ciphertext

def Decrypt(ciphertext, x):
	print(len(ciphertext))
	key = hashlib.sha256(str(x).encode()).digest()
	aes = algorithms.AES(key)
	decryptor = Cipher(aes, modes.ECB(), default_backend()).decryptor()
	unpadder = padding.PKCS7(aes.block_size).unpadder()
	decrypted_data = decryptor.update(ciphertext) + decryptor.finalize() 
	print(decrypted_data)
	plaintext = unpadder.update(decrypted_data) + unpadder.finalize()
	return plaintext 

msga1 = b'Hello Bob.'
msgb1 = b'Hello Alice.'
msgb2 = b'Dinner sounds good. Thanks for the flag.'
za1 = get_z(msga1)
zb1 = get_z(msgb1)
zb2 = get_z(msgb2)

aa = 16843009

# calculate db via Lattices
M = Matrix(ZZ, 33, 33)
lb = [0] * 33
ub = [0] * 33

for i in range(0, 16):
	M[i, 32] = (rb2 * aa * sb1 * (1 << (32 * i))) % n
	M[i+16, 32] = n - (rb1 * aa * sb2 * (1 << (32 * i))) % n
	M[32, 32] = n
	lb[32] = (rb2 * zb1 - rb1 * zb2) % n
	ub[32] = (rb2 * zb1 - rb1 * zb2) % n

for i in range(0, 32):
	M[i, i] = 1
	lb[i] = 0
	ub[i] = 255

result, applied_weights, fin = solve(M, lb, ub, weight = 1)

kb1 = 0
kb2 = 0

for i in range(16):
	kb1 += aa * (1 << (32 * i)) * int(fin[i])
	kb2 += aa * (1 << (32 * i)) * int(fin[i + 16])

db1 = ((kb1 * sb1 - zb1 + n) * inverse(rb1, n)) % n
db2 = ((kb2 * sb2 - zb2 + n) * inverse(rb2, n)) % n

assert db1 == db2
db = (db1 + db2) >> 1

u1 = (za1 * inverse(sa1, n)) % n 
u2 = (ra1 * inverse(sa1, n)) % n

E = EllipticCurve(GF(mod), [a, b])
P = (n - 1) * E.lift_x(GF(mod)(ra1)) # try 1 or n-1
G_x = (G[0] * inverse(G[2] * G[2], mod)) % mod
G_y = (G[1] * inverse(G[2] * G[2] * G[2], mod)) % mod
GG = E(G_x, G_y)

Qa = int(inverse(u2, n)) * (P + (n - u1) * GG)

res = int(u2) * Qa + int(u1) * GG

common = db * Qa
common = int(common.xy()[0]) % mod

print(Decrypt(long_to_bytes(ca2), common))