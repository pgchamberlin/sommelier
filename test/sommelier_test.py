import unittest
import scipy.stats.stats

class TestSommelier(unittest.TestCase):

  def setUp(self):
    self.people = ['bruce','carl','derek']
    self.people['bruce'] = [1,2,3,4]
    self.people['carl']  = [2,3,4,5]
    self.people['derek'] = [4,0,9,1]
  
  def test_name(self):
    scipy.stats.pearsonr(self.people['bruce'],self.people['carl']);
    self.assertEqual(self.name, 'sommelier')
  
if __name__ == '__main__':
  unittest.main()

