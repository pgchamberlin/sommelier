#!flask/bin/python
from src.recommender import SommelierYeungMFRecommender, SommelierRecommender
y = SommelierYeungMFRecommender()
y.split_data_evaluation([
    {"steps":10,  "factors":10, "verbose":True},
], percent_train=95)
