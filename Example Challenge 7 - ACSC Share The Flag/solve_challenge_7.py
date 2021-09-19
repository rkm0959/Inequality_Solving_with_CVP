from Crypto.Cipher import AES, PKCS1_OAEP, PKCS1_v1_5
from Crypto.PublicKey import RSA
from Crypto.Util.Padding import pad
from Crypto.Util.number import inverse, long_to_bytes, bytes_to_long, isPrime, getPrime
from sympy.matrices.matrices import num_mat_mul
from tqdm import tqdm
from pwn import *
from sage.all import *
import gmpy2, pickle, itertools, sys, json, hashlib, os, math, time, base64, binascii, string, re, struct, datetime, subprocess
import numpy as np
import random as rand
import multiprocessing as mp
from base64 import b64encode, b64decode
from sage.modules.free_module_integer import IntegerLattice
from ecdsa import ecdsa
from Crypto.Hash import SHA3_256, HMAC, BLAKE2s
from sage.modules.free_module_integer import IntegerLattice
from Crypto.Cipher import AES, ARC4, DES

def SVP_oracle(mat):
	M = mat.BKZ(block_size = 30)
	return M

def solve(mat, lb, ub, weight = None, auto = True, mode = None, block_size = None, verbose = False):
	num_var  = mat.nrows()
	num_ineq = mat.ncols()

	max_element = 0 
	for i in range(num_var):
		for j in range(num_ineq):
			max_element = max(max_element, abs(mat[i, j]))

	if weight == None or weight < 0:
		weight = num_ineq * max_element

	# sanity checker
	if len(lb) != num_ineq:
		print("Fail: len(lb) != num_ineq")
		return None, None 

	if len(ub) != num_ineq:
		print("Fail: len(ub) != num_ineq")
		return None, None 

	for i in range(num_ineq):
		if lb[i] > ub[i]:
			print("Fail: lb[i] > ub[i] at index", i)
			return None, None 

	if num_var != num_ineq:
		print("Fail: This time, we require num_var = num_ineq")
		return None, None
	
	N = (num_var + num_ineq) // 2
	
	# heuristic for number of solutions
	DET = abs(mat.det())
	num_sol = 1
	for i in range(N):
		num_sol *= (ub[i] - lb[i] + 1)
	
	if DET == 0:
		print("Fail: Zero Determinant")
		return None, None
	else:
		num_sol //= DET
		# + 1 added in for the sake of not making it zero...
		print("Expected Number of Solutions : ", num_sol + 1)

	# recentering + scaling process begins
	max_diff = max([ub[i] - lb[i] for i in range(N)])
	applied_weights = []

	for i in range(N):
		ineq_weight = 0
		if lb[i] == 0 and ub[i] == 251:
			ineq_weight = 1
		else: ineq_weight = 100 * max_diff // (ub[i] - lb[i])
		applied_weights.append(ineq_weight)
		for j in range(N):
			mat[j, i] *= ineq_weight
		lb[i] *= ineq_weight
		ub[i] *= ineq_weight

	target = vector([(lb[i] + ub[i]) // 2 for i in range(N)])

	embedding = 251

	Kannan = Matrix(ZZ, N+1, N+1)
	for i in range(0, N):
		for j in range(0, N):
			Kannan[i, j] = mat[i, j]
		Kannan[i, N] = 0
	for i in range(0, N):
		Kannan[N, i] = target[i]
	Kannan[N, N] = embedding

	# SVP time
	result = SVP_oracle(Kannan)

	# finding solution
	fin_result = None 
	for i in range(N+1):
		isok = True
		if abs(result[i, N]) != embedding:
			isok = False
		result_vector = result[i]
		if result[i, N] == embedding:
			result_vector = -result_vector
			# now result = actual_vector - target
		for j in range(N):
			if (lb[j] <= result_vector[j] + target[j] <= ub[j]) == False:
				isok = False
		if isok == False:
			continue
		print("Found Vector!!")
		fin_result = result_vector[:N] + target
	
	if fin_result == None:
		print("Fail: could not solve...")
		return None, None
	
	return fin_result, applied_weights



# r = remote('share-the-flag.chal.acsc.asia', 37896)
# r.interactive()

p = 251
X = bytes.fromhex("02d4623be12c8f01cb2ebe5f837c1d")
Y = bytes.fromhex("bbdc06ceb34da7b16336b007dc5492")
X2 = bytes.fromhex("2fb9e753b237e68d35e266b0f01c9e")
Y2 = bytes.fromhex("20c0be9140f5a33d71b9e82f8f9409")
X3 = bytes.fromhex("f42e3ee10edeade0a3804a22e86a63")
Y3 = bytes.fromhex("c7224da73d9d96254f94136d9a65f1")
X4 = bytes.fromhex("37c9b07870283dd3f6198c46f027dd")
Y4 = bytes.fromhex("8101a88a365526e8faf417b79599a0")
X5 = bytes.fromhex("b0342cb7b3f5a022d927f9019a1bf3")
Y5 = bytes.fromhex("e2666d892955494775aa3c96c441f5")
X6 = bytes.fromhex("e56bf4f9e746252dbacb93a0a95087")
Y6 = bytes.fromhex("cbb43831857333b2c4663ba2c9189a")
X7 = bytes.fromhex("99ca36b1633cf3d903d8e6291f1bdc")
Y7 = bytes.fromhex("25180068651818171d10422dbdb395")

M = Matrix(GF(p), 105, 128)
vec = []
for i in range(105):
	x, y = 0, 0
	if i < 15:
		x = int(X[i])
		y = int(Y[i])
	elif i < 30:
		x = int(X2[i - 15])
		y = int(Y2[i - 15])
	elif i < 45:
		x = int(X3[i - 30])
		y = int(Y3[i - 30])
	elif i < 60:
		x = int(X4[i - 45])
		y = int(Y4[i - 45])
	elif i < 75:
		x = int(X5[i - 60])
		y = int(Y5[i - 60])
	elif i < 90:
		x = int(X6[i - 75])
		y = int(Y6[i - 75])
	elif i < 105:
		x = int(X6[i - 90])
		y = int(Y6[i - 90])

	vec.append(y)
	for j in range(16):
		M[i, j] = (x ** j) % p
	if i < 15:
		for j in range(16):
			M[i, j + 16] = (x ** (j + 16)) % p
	elif i < 30:
		for j in range(16):
			M[i, j + 32] = (x ** (j + 16)) % p
	elif i < 45:
		for j in range(16):
			M[i, j + 48] = (x ** (j + 16)) % p
	elif i < 60:
		for j in range(16):
			M[i, j + 64] = (x ** (j + 16)) % p
	elif i < 75:
		for j in range(16):
			M[i, j + 80] = (x ** (j + 16)) % p
	elif i < 90:
		for j in range(16):
			M[i, j + 96] = (x ** (j + 16)) % p
	elif i < 105:
		for j in range(16):
			M[i, j + 112] = (x ** (j + 16)) % p

vec = vector(GF(p), vec)

bas = M.right_kernel().basis()
print(len(bas))
v = M.solve_right(vec)

# v + bas -> all in 97 ~ 122

M = Matrix(ZZ, 151, 151)
lb = [0] * 151
ub = [0] * 151

for i in range(23):
	for j in range(128):
		M[i, j] = int(bas[i][j])
	M[i, 128 + i] = 1
for i in range(128):
	M[23 + i, i] = p
for i in range(128):
	if i >= 16:
		lb[i] = int(97 - int(v[i]))
		ub[i] = int(122 - int(v[i]))
	else:
		lb[i] = int(32-int(v[i]))
		ub[i] = int(128-int(v[i]))
for i in range(23):
	lb[i + 128] = 0
	ub[i + 128] = p

fin_result, applied_weights = solve(M, lb, ub)

flag = ''

for i in range(16):
	flag += chr((fin_result[i] // applied_weights[i] + int(v[i]) + 251 * 30) % 251)

print("ACSC{" + flag + "}")