## TL,DR:

Independent verification of OEIS Sequences A079761, A079762, A152169,
all relating to permutations of a 2x2x2 rubix cube

# Background:

I was playing around with the idea of making a Rubix Cube solver in Python when I stumbled across
http://cube20.org/ - A cool project showing that every position attainable by the 3x3 rubix cube
can be solved in 20 moves or less. It's a great project, but it took 35 CPU-years to complete!

That got me interested in solving the same problem in the 2x2 case. Of course, the solution is already
on Wikipeida and in OEIS, but there wasn't any code to be found. Both OEIS and Wikipeida referenced the same
source, http://cubeman.org/fullcube.txt. As far as I could tell, nobody else had done any work on it. 
The cubeman website contains the following printout:

```
        Analysis of the 2x2x2 cube group
        --------------------------------

Originally computed on a DEC VAX 11/780 in over 51 hours of CPU time
 on Sept. 9, 1981
Moves Deep     arrangements (q+h)   arrangements (q)  loc max (q+h) loc max (q)

  0                    1                   1                 0               0
  1                    9                   6                 0               0
  2                   54                  27                 0               0
  3                  321                 120                 0               0
  4                1,847                 534                11               0
  5                9,992               2,256                 8               0
  6               50,136               8,969                96               0
  7              227,536              33,058               904              16
  8              870,072             114,149            13,212              53
  9            1,887,748             360,508           413,392             260
 10              623,800             930,588           604,516           1,460
 11                2,644           1,350,852             2,644          34,088
 12                                  782,536                           402,260
 13                                   90,280                            88,636
 14                                      276                               276
               ---------           ---------         ---------         -------
               3,674,160           3,674,160         1,034,783         527,049
```
I assume I could do better than 51 hours on a modern day processor.

# Writeup:
Take a 2x2x2 rubix cube. Ennumerate the sides from 0,...,23 so in the solved configuration it would be represented as :
```
          UP
      | 4  5  |
      | 6  7  |
  LEFT  FRONT   RIGHT   BACK
| 0 1 | 8  9  | 16 17 | 20 21 |
| 2 3 | 10 11 | 18 19 | 22 23 |
        DOWN
      | 12 13 |
      | 14 15 |
```
and encoded in the vector [0,1,...,24]

Now we have 6 rotations. Holding the back left cube steady, we can rotate the front face, right face, or bottom face 
either clockwise or counterclockwise. We can denote these rotations as F, Fi, R, Ri, D, and Di respectively. 
For example, applying F to our original rotation we get:
```
           UP
       | 4  5  |
       | 3  1  |
  LEFT   FRONT   RIGHT  BACK
| 0 12 | 10 8  | 6 17 | 20 21 |
| 2 13 | 11 9  | 7 19 | 22 23 |
         DOWN
       | 18 16 |
       | 14 15 |
```
We can encode this state as a new vector. This means we can represent each move as a matrix multiplication!
F can be represented as a 24x24 sparse matrix. Only 12 values change positions. Similarly the Fi move
corresponds to the inverse of the F matrix.

How do we construct this matrix?
If the start vector is [0,1,...,23] then we know from doing it by hand that the end vector is
[0, 12, 2, 13, 4, 5, 3, 1, 10, 8, 11, 9, 18, 16, 14, 15, 6, 17, 7, 19, 20, 21, 22, 23]
We can see values at indicies 1, 3, 6, 7, 8, 9, 10, 11, 12, 13, 16, and 18 change

We need to zero out the matrix in all the positions where things changed.
We also have 12 new 1's to insert for each new location. 12 went to 1, 1 went to 7, etc.
These changes can be represented as tuples.
We can generate them programmatically from the differences between the result vector and the original!

Now we just need to do the same thing for the R and D rotations
```
R:
          UP
      | 4  9  |
      | 6  11 |
  LEFT  FRONT   RIGHT   BACK
| 0 1 | 8  13 | 18 16 | 7 21 |
| 2 3 | 10 15 | 19 17 | 5 23 |
        DOWN
      | 12 22 |
      | 14 20 |
```
This corresponds to the vector
[0, 1, 2, 3, 4, 9, 6, 11, 8, 13, 10, 15, 12, 22, 14, 20, 18, 16, 19, 17, 7, 21, 5, 23]
```
U:
            UP
        | 4  5  |
        | 6  7  |
  LEFT    FRONT   RIGHT   BACK
| 0  1  | 8  9  | 16 17 | 20 21 |
| 22 23 | 2  3  | 10 11 | 18 19 |
          DOWN
        | 14 12 |
        | 15 13 |
```
This corresponds to the vector
[0, 1, 22, 23, 4, 5, 6, 7, 8, 9, 2, 3, 14, 12, 15, 13, 16, 17, 10, 11, 20, 21, 18, 19]

There! Now we have matrix representations of our 6 basic moves. In addition, we can
easily generate F2, R2, and U2 by computing F*F, R*R, and U*U. We can generate all possible configurations 
of the cube using the following algorithm:
```
  Create two sets, RESULTS and LAST_SET. Add the [0,1,...,23] starting configuration to both.
  Let moves be the set of all possible moves.
  While LAST_SET is not empty:
    For each state in LAST_SET:
      Let NEXT_SET be an empty set
      For each move in moves:
        newstate = DO_MOVE(state, move)
        If newstate is in RESULTS, ignore it. We have seen it before
        Otherwise, add it to RESULTS and NEXT_SET
    Let NEXT_SET become LAST_SET
```
We terminate when we cannot generate a new state from any previous state. Since all states must be 
reachable from all other states, this means we must have generated all possible states.

### Future Optimizations:
1. Use scipy's sparse matrix library to speed up calculations

2. We could keep track of the last move used on the cube. If the last move used was F, 
   we could skip applying Fi because that would take us to a previous state. We can also 
   skip applying F2 because that would take us to the previous state + Fi, which we've 
   presumably already calculated. Similarly if our last move was F2 we could skip F2, F, 
   and Fi This should cut the branching of the tree down to 6 for the half/quarter case and 
   4 for the quarter case, but increases our space complexity because now we must maintain 
   a dictionary instead of a set.
3. Multiprocessing? Hard because the set is shared between all processes

### Future Work:
1. Do something similar for the 3x3x3 cube?
2. Figure out how to generate the turning matrix for an NxNxN cube programmatically
