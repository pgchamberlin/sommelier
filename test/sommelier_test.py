import unittest
import pprint
import scipy.stats.stats

class TestSommelier(unittest.TestCase):

  def setUp(self):
    self.people = [
      [1,2,3,4],
      [2,3,4,5],
      [1,3,0,2]
    ]
  
  def test_name(self):
    self.pearsonr = [
      scipy.stats.pearsonr(self.people[0],self.people[1]),
      scipy.stats.pearsonr(self.people[0],self.people[2]),
    ]
    self.assertEqual(self.pearsonr[0][0], 1)
    self.assertEqual(self.pearsonr[1][0], 0)
  
if __name__ == '__main__':
  unittest.main()

