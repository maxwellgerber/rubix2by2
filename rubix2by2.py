import numpy as np

def generate_basic_moveset():
  ## Generates matrix representations of the three basic quarter-turn moves possible with a 2x2x2 rubix cube
  ## In Singmaster notation, these correspond to F, R, and D
  
  # Magic number arrays - see README
  F_result = np.array([0, 12, 2, 13, 4, 5, 3, 1, 10, 8, 11, 9, 18, 16, 14, 15, 6, 17, 7, 19, 20, 21, 22, 23])
  R_result = np.array([0, 1, 2, 3, 4, 9, 6, 11, 8, 13, 10, 15, 12, 22, 14, 20, 18, 16, 19, 17, 7, 21, 5, 23])
  D_result = np.array([0, 1, 22, 23, 4, 5, 6, 7, 8, 9, 2, 3, 14, 12, 15, 13, 16, 17, 10, 11, 20, 21, 18, 19])
  
  moves = []
  for result in F_result, R_result, D_result:
    changes = []
    for i, val in enumerate(result):
      if i != val:
        changes.append((i, val))
  
    M = np.identity(24, dtype=int)
  
    for x,y in changes:
      M[y][y] = 0
      M[x][y] = 1
      
    assert len(changes) == 12
  
    moves.append(M)
  
  return moves
  
def generate_quarter_moveset():
  ## Generates matrix representations of the six basic quarter-turn moves possible with a 2x2x2 rubix cube
  ## In Singmaster notation, these correspond to F, R, D, Fi, Ri, and Di
  
  moves = generate_basic_moveset()
  for M in moves[::]:
    M_inv = np.linalg.inv(M).astype(int)
    moves.append(M_inv)
  
  return moves

def generate_half_moveset():
  ## Generates matrix representations of the nine moves possible with a 2x2x2 rubix cube
  ## In Singmaster notation, these correspond to F, Fi, F2, R, Ri, R2, D, Di, and D2

  moves = generate_quarter_moveset()
  moves.append(moves[0].dot(moves[0]))
  moves.append(moves[1].dot(moves[1]))
  moves.append(moves[2].dot(moves[2]))
  
  return moves
  
def count_positions(moveset):
  # Prints out the number of positions that can be reached in n moves from the start,
  # but which cannot be reached in fewer than n moves.
  # Using only the moves found in moveset
  
  print("Moves Deep   arrangements")
  
  sol = np.array(range(24))
  results = set()
  results.add(tuple(sol))
  
  last_set = set()
  last_set.add(tuple(sol))
  
  count = 0
  total = 1
  while len(last_set):
    print("{:^10}        {:<12}".format(count, len(last_set)))
    count += 1
    next_set = set()
    for state in last_set:
      for move in moveset:
        nstate = move.dot(state)
        s = tuple(nstate)
        if s not in results:
          results.add(s)
          next_set.add(s)
    total += len(next_set)
    last_set = next_set
  return total
  
if __name__ == "__main__":
    
  print("Solving for OEIS A079761")
  print("This is the number of positions that can be reached in n moves from the start,\n"+\
        "but which cannot be reached in fewer than n moves")
        
  h_moves = generate_half_moveset()
  t1 = count_positions(h_moves)
  
  print("Solving for OEIS A079762")
  print("This is the number of positions that can be reached in n quarter moves from the start,\n"+\
        "but which cannot be reached in fewer than n moves")
        
  q_moves = generate_quarter_moveset()
  t2 = count_positions(q_moves)
  
  print("Solving for OEIS A152169")
  print("This is the number of positions that can be reached in n one-way quarter moves from the start,\n"+\
        "but which cannot be reached in fewer than n moves")
        
  b_moves = generate_basic_moveset()
  t3 = count_positions(b_moves)
  
  assert t1==t2 and t2==t3 and t3==3674106
  
  print("This is the number of positions that can be reached in n one-way quarter moves from the start, using only 2 moves")
  count_positions(b_moves[:2])
  
  # print("Number of positions only using R and D")
  # count_positions((q_moves[2], q_moves[4]))
  
  # print("Number of positions only using F and D")
  # count_positions((q_moves[0], q_moves[4]))
