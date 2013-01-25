import unittest

class TestSommelier(unittest.TestCase):

  def setUp(self):
    self.name = 'sommelier'
  
  def test_name(self):
    self.assertEqual(self.name, 'sommelier')
  
if __name__ == '__main__':
  unittest.main()

