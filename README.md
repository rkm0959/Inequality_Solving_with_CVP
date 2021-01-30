# Inequality Solving with CVP

a.k.a. the method rkm0959 uses all the time for CTFs, worked well so far, but has no idea why

obviously I'm not going to claim anything like "I uSed tHIs iDea FirST!!!", since I've seen others use it

## How to use

The solve function has four inputs, matrix ``mat``, lower/upper bounds ``lb, ub``, and a ``weight``.

Assume ``mat`` is an ``n x m`` integer matrix. This means there are ``n`` variables and ``m`` inequalities.

Each column of the ``mat`` represents a linear combination of the ``n`` variables. 

Each entry of ``lb, ub`` denotes a lower/upper bound to that linear combination.

Of course, we require the length of ``lb, ub`` to be ``m``. 

``weight`` is a variable that you do *NOT* have to initialize. It will be explained later.



## The reasoning behind the algorithm

**Warning : the stuff I say here are not mathematically precise. It's 100% intuition**

Basically what the algorithm does, is to build a lattice with the given matrix and find a closest vector (with Babai's algorithm) to ``(lb + vb) / 2``. However, there is one more twist to the algorithm.

The reason we hope that CVP will solve our problem is basically as follows

- CVP will try to minimize ``||x - (lb + vb) / 2||`` where ``x`` is in our lattice
- Usually, that *implies* trying to minimize ``|x_i - (lb_i + ub_i) / 2|`` for each `i`
- Therefore, it will try to keep `|x_i - (lb_i + ub_i) / 2|` below `|(ub_i - lb_i) / 2|`!

However, there's a case where this reasoning fails. 

- Assume we have an instance with`lb = [0, 0]`, `ub = [10 ** 300, 1]`
- Does the CVP algorithm "respect" the bound `lb_2 = 0, ub_2 = 1`?
- CVP algorithm will ignore it to keep the first entry close to `(10 ** 300) / 2` as possible

To do this, we have to *scale* our inequalities so `ub_i - lb_i` becomes of similar size. 

- This can be done by multiplying an entire column, as well as `lb_i` and `ub_i`
- What if `lb_i = ub_i`? Then, we have to multiply a `super large integer` to that column.
- This `super large integer` is the `weight` in the input. 
- The default `weight` is what I think is "super large", but you can definitely change it :)



## Further Comments

- **Babai's Algorithm implementation is NOT MINE - read solver.sage for details**
- I have included 4 example challenges I have solved using this technique.
- You can also break truncated LCG with this idea.  left as exercise.
- This method does not work *that* well with low density 0/1 knapsack - CJ LOSS is much better.
- The *scaling* method (obviously) increases the runtime of the LLL.
- It seems like sometimes SVP gives better results than CVP...
- If failed, it's a good idea to try a different scaling by observing the failed output.


## Simple "tricks"

- Inequalities with `(mod n)` things can be done by adding a dummy variable and multiplying `n`

- After retrieving solution, you *must* note that the values retrieved are scaled. 

- If you want to retrieve the value of a certain variable, add a simple constraint to it.

- For example, if you want `d`, add a constraint like `0 <= d <= n` to the matrix/lb/ub.

- Most of these "tricks" are relatively obvious, and they are used in the example solutions.

  

 

