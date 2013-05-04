#!flask/bin/python
from src.recommender import SommelierYeungMFRecommender, SommelierRecommender
y = SommelierYeungMFRecommender()
y.split_data_evaluate_movielens_file('ml-100k/u.data', [
    {"steps":1,  "factors":10, "verbose":True},
    {"steps":2,  "factors":10, "verbose":True},
    {"steps":3,  "factors":10, "verbose":True},
    {"steps":4,  "factors":10, "verbose":True},
    {"steps":5,  "factors":10, "verbose":True},
    {"steps":6,  "factors":10, "verbose":True},
    {"steps":7,  "factors":10, "verbose":True},
    {"steps":8,  "factors":10, "verbose":True},
    {"steps":9,  "factors":10, "verbose":True},
    {"steps":10,  "factors":10, "verbose":True},
    {"steps":12,  "factors":10, "verbose":True},
    {"steps":14,  "factors":10, "verbose":True},
    {"steps":16,  "factors":10, "verbose":True},
], percent_train=80)

y.split_data_evaluate_movielens_file('ml-100k/u.data', [
    {"steps":1,  "factors":10, "verbose":True},
    {"steps":2,  "factors":10, "verbose":True},
    {"steps":3,  "factors":10, "verbose":True},
    {"steps":4,  "factors":10, "verbose":True},
    {"steps":5,  "factors":10, "verbose":True},
    {"steps":6,  "factors":10, "verbose":True},
    {"steps":7,  "factors":10, "verbose":True},
    {"steps":8,  "factors":10, "verbose":True},
    {"steps":9,  "factors":10, "verbose":True},
    {"steps":10,  "factors":10, "verbose":True},
    {"steps":12,  "factors":10, "verbose":True},
    {"steps":14,  "factors":10, "verbose":True},
    {"steps":16,  "factors":10, "verbose":True},
], percent_train=80)

