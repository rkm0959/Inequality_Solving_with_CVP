# The Special Case

This algorithm can solve for **all** `x` such that the following inequality holds.

- `L <= Ax (mod M) <= R`
- `S <= x <= E`

This algorithm is used in some competitive programming challenges as well.

For a discussion, check https://codeforces.com/blog/entry/15488 and https://neerc.ifmo.ru/archive/2019.html

(Codeforces Good Bye 2014 Problem G), (NWRRC 2019 Problem G)


## How to use

Call `solve(A, M, L, R, S, E)` to retrieve the array of all solutions.

There are heuristically `(E-S+1) * (R-L+1) / M` solutions, so if this is large don't run it.

The time complexity is proportional to number of solutions.

For each solution, the time complexity needed to compute it is polynomial.

As a benchmark : a few million solutions can be calculated without much trouble.

There are 3 challenges in this repository to serve as examples.



It's also important to clarify what I mean by `L <= Ax (mod M) <= R`.

To do so, imagine the numbers modulo `M` as a circle, starting from `0` to `M-1` and back to `0`.

The inequality means that `Ax (mod M)` lies in the 'arc' from `L` to `R`, clockwise.

This means that, for example, `M-5 <= Ax (mod M) <= 3` has a solution. 



Of course, you can also use `optf` function directly. I don't know why I named it like that but anyway...
