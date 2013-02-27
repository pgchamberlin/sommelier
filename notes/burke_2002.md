# Notes on Burke, 2002 "Hybrid Recommender Systems"

Burke (2002) 'Hybrid Recommender Systems: Survey and Experiments' User Modeling and User-Adapted Interaction, Volume 12 Issue 4, November 2002, Pages 331 - 370. Kluwer Academic Publishers: Hingham, MA, USA

Section 1:

Burke (2002) cites Resnick and Varian's (1997) definition: "people provide recommendations as inputs, which the system then aggregates and directs to appropriate recipients", but goes on to assert that, "the term now has a broader connotation, describing any system that produces individualized recommendations as output or has the effect of guiding the user in a personalized way to interesting or useful objects in a large space of possible options."

"Amount of online information vastly outstrips any individual's capability to survey it"

"Semantic ratings made available by the knowledge-based portion of the system provide an additional boost to the hybrid's performance"

1.1:

Three inputs:
 i.   Background data       - exists before recommendation process
 ii.  Input data            - derived from user
 iii. Recommender algorithm - by which i & ii are combined, resulting in recommendations

Five kinds of system:
 1.   Collaborative
 2.   Content-based
 3.   Demographic
 4.   Utility-based
 5.   Knowledge-based

Collaborative:
 - most mature, researched
   - sometimes time degrades preferences
   - sometimes binary (like/unlike)
   - sometimes real-value

"The greatest strength of collaborative techniques is that they are completely independent of any machine-readable representation of the objects being recommended, and work well for complex objects such as music and movies where variations in taste are responsible for much of the variation in preferences."

Demographic:
 - Sometimes up-front survey data gathered to segment users
 - Sometimes demographic classifier developed through machine learning
 - Demographic techniques do not require rating history (unlike CF)

