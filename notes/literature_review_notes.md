# Literature review (notes)

## Information retrieval agents
 - Such as collaborative filtering, or content-based filtering agents

## What is CF?
 - "the technique of using peer opinions to predict the interest of others." (Claypool et al., 1999)
 
## Problems with CF
 Claypool et al., 1999
  - Early rater problem (cold-start problem)
      A new system, or new user, does not have any basis for recommendation
  - Sparsity problem
      Many items, few of which any one user will ever have data for, lead to sparse matrices
  - Gray sheep
      People who never consistently agree or disagree with the community at large

## Content based filtering
 - analyse content of item user has rated / commented

## Problems with CB
 Claypool et al., 1999
  - "As the number of items grows, the number of items in the same content-based category increases"
     This is especially problematic for wines as there are many very similar items

## CF / CB in combination
 Claypool et al., 1999
  - "Vogt et al. showed..." -> use linear combination of scores from muliple systems to improve performance
  - "The trick is to come up with the weight that result in the most accurate prediction."
