import scipy.stats
import sys

class Sommelier():

  people = ['bruce','carl','derek']
  people[0] = [1,2,3,4]
  people[1]  = [2,3,4,5]
  people[2] = [4,0,9,1]
  
  def run(self):
    print(scipy.stats.pearsonr(self.people[0],self.people[1]));
    print(scipy.stats.pearsonr(self.people[0],self.people[2]));
    print(scipy.stats.pearsonr(self.people[1],self.people[2]));
  
sm = Sommelier()
sm.run()

