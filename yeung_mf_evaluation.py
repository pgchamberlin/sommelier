#!flask/bin/python
from src.recommender import SommelierYeungMFRecommender, SommelierRecommender
y = SommelierYeungMFRecommender()
m = y.generate_lists_ui_matrix()
y.multiple_factorizations(m, [
    {"steps":250,  "factors":15},
    {"steps":500,  "factors":15},
    {"steps":750,  "factors":15},
    {"steps":1000, "factors":15},
    ])
y.multiple_factorizations(m, [
    {"steps":250,  "factors":20},
    {"steps":500,  "factors":20},
    {"steps":750,  "factors":20},
    {"steps":1000, "factors":20},
    ])
y.multiple_factorizations(m, [
    {"steps":1250, "factors":15},
    {"steps":1500, "factors":15},
    {"steps":1750, "factors":15},
    {"steps":2000, "factors":15},
    ])
y.multiple_factorizations(m, [
    {"steps":1250, "factors":20},
    {"steps":1500, "factors":20},
    {"steps":1750, "factors":20},
    {"steps":2000, "factors":20},
    ])
y.multiple_factorizations(m, [
    {"steps":2500, "factors":10},
    {"steps":3000, "factors":10},
    ])
y.multiple_factorizations(m, [
    {"steps":2500, "factors":15},
    {"steps":3000, "factors":15},
    ])
y.multiple_factorizations(m, [
    {"steps":2500, "factors":20},
    {"steps":3000, "factors":20},
    ])
y.multiple_factorizations(m, [
    {"steps":3500, "factors":10},
    {"steps":4000, "factors":10},
    ])
y.multiple_factorizations(m, [
    {"steps":3500, "factors":15},
    {"steps":4000, "factors":15},
    ])
y.multiple_factorizations(m, [
    {"steps":3500, "factors":20},
    {"steps":4000, "factors":20},
    ])

