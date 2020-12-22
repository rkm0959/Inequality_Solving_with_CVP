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

## Example 2 : SECCON CTF 2020 sharsable

n  = 142793817321992828777925840162504083304079023834001118099549928854335392622287928254035247188624975743042449746066633491912316354241339908190889792327014012472372654378644158878787350693992259970146885854641856991605625756536504266728483088687985429310233421251081614258665472164668993082471923690196082829593
e_1 = 82815162880874815458042429141267540989513396527359063805652845923737062346339641683097075730151688566721221542188377672708478777831586255213972947470222613130635483227797717393291856129771004300757155687587305350059401683671715424063527610425941387424425367153041852997937972925839362190900175155479532582934
C_1 = 108072697038795075732704334514926058617161875495016327352871122917196026504758904760148391499245235850616838765611460630089577948665981247735905622903872682862860306107704253287284051312867625831877418240290183661755993649928399992531008191618616452091127799880839665225093055618092869662205901927957599941568
e_2 = 84856171747859965508406237198459622554468224770252249975158471902036102010991476445962577679301719179079633469099994226630172251817358960347828156301869905575867853640850107406452911333646573296923235424617864473580743418995994067645338437540627399276292679100115018844287273293945121023787594592185295794983
C_2 = 101960082023987498941061751761131381167414505957511290567652602520714324823481487410890478130601013005035303795327512367595187718926017321227779179404306882163521882309833982882201152721855538832465833869251505131262098978117904455226014402089126682222497271578420753565370375178303927777655414023662528363360

# build matrix
M = matrix(ZZ, 3, 3)

# encode d_1
M[0, 0] = 1 

# encode d_2
M[1, 1] = 1 

# encode e_1d_1 + e_2d_2 + nd_3
M[0, 2] = e_1
M[1, 2] = e_2
M[2, 2] = n

# build lb/ub
lb = [0, 0, -int(n ** 0.66)]
ub = [int(n ** 0.16), int(n ** 0.16), 0]

# solve system
res, weights = solve(M, lb, ub)

# this result will be d_1 * weight[0] * [1, 0, e_1] + d_2 * weight[1] * [0, 1, e_2] + d_3 * weight[2] * [0, 0, n]
d_1 = res[0] // weights[0]
d_2 = res[1] // weights[1]

phi_mul = e_1 * d_1 + e_2 * d_2 - 1

if GCD(e_1, phi_mul) == 1:
    d_1 = inverse_mod(e_1, phi)
    flag = pow(C_1, d_1, n)
    print(bytes.fromhex(hex(flag)[2:]))

if GCD(e_2, phi_mul) == 1:
    d_2 = inverse_mod(e_2, phi)
    flag = pow(C_2, d_2, n)
    print(bytes.fromhex(hex(flag)[2:]))