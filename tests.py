import unittest, numpy as np
from rubix2by2 import *

class BasicRotationTest(unittest.TestCase):
  
  def setUp(self):
    self.sol = np.array(range(24))
    
  def test_forward_rotation(self):
    F_result = np.array([0, 12, 2, 13, 4, 5, 3, 1, 10, 8, 11, 9, 18, 16, 14, 15, 6, 17, 7, 19, 20, 21, 22, 23])
    F = generate_basic_moveset()[0]
    self.assertTrue((F_result == F.dot(self.sol)).all())
  
  def test_right_rotation(self):
    R_result = np.array([0, 1, 2, 3, 4, 9, 6, 11, 8, 13, 10, 15, 12, 22, 14, 20, 18, 16, 19, 17, 7, 21, 5, 23])
    R = generate_basic_moveset()[1]
    self.assertTrue((R_result == R.dot(self.sol)).all())
  
  def test_down_rotation(self):
    D_result = np.array([0, 1, 22, 23, 4, 5, 6, 7, 8, 9, 2, 3, 14, 12, 15, 13, 16, 17, 10, 11, 20, 21, 18, 19])
    D = generate_basic_moveset()[2]
    self.assertTrue((D_result == D.dot(self.sol)).all())
  
class InvertedRotationTest(unittest.TestCase):
  def setUp(self):
    self.eye = np.eye(24)
    
  def test_forward_inv_rotation(self):
    Fi = generate_quarter_moveset()[3]
    F2 = generate_half_moveset()[6]
    self.assertTrue((Fi.dot(Fi.dot(F2)) == self.eye).all())
    self.assertTrue((Fi.dot(F2.dot(Fi)) == self.eye).all())
    self.assertTrue((F2.dot(Fi.dot(Fi)) == self.eye).all())
  
  def test_right_inv_rotation(self):
    Ri = generate_quarter_moveset()[4]
    R2 = generate_half_moveset()[7]
    self.assertTrue((Ri.dot(Ri.dot(R2)) == self.eye).all())
    self.assertTrue((Ri.dot(R2.dot(Ri)) == self.eye).all())
    self.assertTrue((R2.dot(Ri.dot(Ri)) == self.eye).all())
  
  def test_down_inv_rotation(self):
    Di = generate_quarter_moveset()[5]
    D2 = generate_half_moveset()[8]
    self.assertTrue((Di.dot(Di.dot(D2)) == self.eye).all())
    self.assertTrue((Di.dot(D2.dot(Di)) == self.eye).all())
    self.assertTrue((D2.dot(Di.dot(Di)) == self.eye).all())
  
  
  
if __name__ == "__main__":
  unittest.main()
