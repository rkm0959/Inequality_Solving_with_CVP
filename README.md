# Inequality Solving with CVP

A special case of this problem has another algorithm : check the "Special Case" folder for details

A full writeup on this toolkit (in Korean) will hopefully be posted for SAMSUNG Software Membership blog.

http://www.secmem.org/blog/2021/03/15/Inequality_Solving_with_CVP/

## How to use

The solve function has four inputs, matrix ``mat``, lower/upper bounds ``lb, ub``, and a ``weight``.

Assume ``mat`` is an ``n x m`` integer matrix. This means there are ``n`` variables and ``m`` inequalities.

Each column of the ``mat`` represents a linear combination of the ``n`` variables. 

Each entry of ``lb, ub`` denotes a lower/upper bound to that linear combination.

Of course, we require the length of ``lb, ub`` to be ``m``. 

``weight`` is a variable that you do *NOT* have to initialize. It will be explained later.

`result` is the result of the CVP 

`applied_weights` is the applied weights during the weighting process (see below)

`fin` is the actual value of the variables, recovered when `n = m` and vectors are linearly independent

We also have a heuristic for number of solutions for the inequality. This is a good way to decide if this method is feasible. For some notes on this topic, check out [Mystiz's writeup on Example Challenge 5.](https://mystiz.hk/posts/2021-02-28-aeroctf/)

## The reasoning behind the algorithm

**Warning : the stuff I say here are not mathematically precise. It's based on intuition**

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
- I have included some example challenges I have solved using this technique.
- You can also break truncated LCG with this idea.
- This method does not work *that* well with low density 0/1 knapsack - CJ LOSS is much better.
- The *scaling* method (obviously) increases the runtime of the LLL.
- It seems like sometimes SVP gives better results than CVP...
- If failed, it's a good idea to try a different scaling by observing the failed output.
