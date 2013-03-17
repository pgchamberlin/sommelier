# Literature review (notes)

From Wikipedia/Recommender_System:
  Montaner provides the first overview of recommender systems, from an intelligent agents perspective.[7] Adomavicius provides a new overview of recommender systems.[8] Herlocker provides an additional overview of evaluation techniques for recommender systems.[9]

Montaner: http://link.springer.com/article/10.1023%2FA%3A1022850703159
Adomavicius: http://dl.acm.org/citation.cfm?id=1070611.1070751
Herlocker et al.: http://dl.acm.org/citation.cfm?id=963772



On weighting the importance of an items features to users:
  For the purpose of filtering, the features of a wine can not be analysed in the same way that features of many other items can. The features of a car, for example, can be for the most part translated into ordinal data; engine capacity, number of doors, passenger legroom, wheel diameter, whereas the attributes of a wine are for the most part nominal; grape variety, region of origin, colour. There are some characteristics of wine which are measured ordinally, such as residual sugar or alcohol content, but these are not necessarily attributes that carry very much information about similarity... ???

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
