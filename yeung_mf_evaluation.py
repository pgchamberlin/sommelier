#!flask/bin/python
from src.recommender import SommelierYeungMFRecommender, SommelierRecommender
y = SommelierYeungMFRecommender()
m = y.generate_lists_ui_matrix()
y.multiple_factorizations(m, [
    {"steps":3500, "factors":15},
    {"steps":4000, "factors":15},
    ])
y.multiple_factorizations(m, [
    {"steps":3500, "factors":20},
    {"steps":4000, "factors":20},
    ])

