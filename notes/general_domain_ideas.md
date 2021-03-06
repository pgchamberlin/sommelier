# Sommelier: Social Recommender for Wines

An application which recommends wines to users based on their preferences and behaviour.

## The system
  - a database of wines, with their associated meta information
  - a JSON based, HTTP REST interface for accessing and acting upon the database

## Features
  - create and share notes and ratings of wines in the database
  - view notes and ratings by other users
  - receive recommendations of wines based on their own preferences and notes
  - Time decay? Use drink YY-YY data to determine?
  - Recommendation up/down voting to train recommendations?
  - Cold start problem: alleviated by fact that items entered 'rich'?
  -

## Domain questions
 
### What is a good wine recommendation?
   
#### Similarity
  - Shared qualities
    - Grape, region etc.
    - Taste profile: adjectives
  -  Interestingness
    - Wines the user would be interested in trying, buying, or otherwise finding out more about

## Domain characteristics
  - Many items
  - Many dimensions for categorisation (colour, region, grape variety, sweetness)
  - Sparseness of data. Like movies, most people wont rate most wines
  - Requirement for scalability: recommendations must be fast

## Validation
  - Mean absolute error (?)

## Methods (as described in Su et al. 2007, IEEE Int. Conf. on Web Intel.)
  - CF (Item|User)
  - Content-based
  - Hybrid
    - Weighted Pearson correlation + naïve Bayes
    - Sequential mixture CF (proposed by Su et al. 2007) = Tree augmented naïve Bayes + extended logistic regression (TAN-ELR)
    - Joint mixture CF (proposed by Su et al. 2007) = 3 separate experts: Pearson correlation-based CF, TAN-ELR content-based predictor, TAN-ELR model-based CF.

