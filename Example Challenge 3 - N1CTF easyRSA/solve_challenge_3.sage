from sage.modules.free_module_integer import IntegerLattice

# Directly taken from rbtree's LLL repository
# From https://oddcoder.com/LOL-34c3/, https://hackmd.io/@hakatashi/B1OM7HFVI
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
    
    ## recover your result
    return result, applied_weights

## Example 3 : N1CTF easyRSA (factorization part only)

N = 32846178930381020200488205307866106934814063650420574397058108582359767867168248452804404660617617281772163916944703994111784849810233870504925762086155249810089376194662501332106637997915467797720063431587510189901

## From the code : N is a divisor of polynomial of 3 ^ 66 with degree 8 and coefficients less than 8 * (2 ^ 32) ^ 2 = 2^67

## coef_0 + 3^66 * coef_1 + ... + 3^(66 * 8) * coef_8 + c * N == 0
## 0 <= coef_i <= 2^67 for each i

# 10 variables, 10 inequalities

# build matrix and lb/ub
M = matrix(ZZ, 10, 10)
lb = [0] * 10
ub = [0] * 10

for i in range(0, 9):
    M[i, 0] = (3 ** 66) ** i
M[9, 0] = N

lb[0] = 0
ub[0] = 0

for i in range(0, 9):
    M[i, i + 1] = 1
    lb[i + 1] = 0
    ub[i + 1] = (2 ** 67)

# solve CVP
res, weights = solve(M, lb, ub)

P.<x> = PolynomialRing(ZZ)
f = 0
for i in range(1, 10):
    f += (res[i] // weights[i]) * x^(i-1)

factorization = f.factor()
print(factorization)

# 3 * (2187594805*x^4 + 2330453070*x^3 + 2454571743*x^2 + 2172951063*x + 3997404950) * (3053645990*x^4 + 3025986779*x^3 + 2956649421*x^2 + 3181401791*x + 4085160459)

# factors! now each factor will have a common prime with N
poly_1 = factorization[1][0]
poly_2 = factorization[2][0]

ev = 0
for i in range(0, 5):
    ev += poly_1[i] * ((3 ** 66) ** i)

p = gcd(ev, N)

assert p != 1 and p != N

q = int(N) // p

assert p * q == int(N)

print("Factorization: ", p, q)