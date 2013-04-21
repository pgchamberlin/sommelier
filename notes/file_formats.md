# Recommender system file formats

Sparse text matrix:

http://tedlab.mit.edu/~dr/SVDLIBC/SVD_F_ST.html

"""
Format:

numRows numCols totalNonZeroValues
for each column:
  numNonZeroValues
  for each non-zero value in the column:
    rowIndex value
Rows are indexed starting with 0. Newlines and spaces are equivalent.

Example:

Dense Text Format:
4 3
2.3  0  4.2
0   1.3 2.2
3.8  0  0.5
0    0   0 
Sparse Text Format:
4 3 6
2
0 2.3
2 3.8
1
1 1.3
3
0 4.2
1 2.2
2 0.5
"""

Movielens:

http://www.grouplens.org/system/files/ml-10m-README.html

"""
Ratings Data File Structure

All ratings are contained in the file ratings.dat. Each line of this file represents one rating of one movie by one user, and has the following format:

UserID::MovieID::Rating::Timestamp

The lines within this file are ordered first by UserID, then, within user, by MovieID.

Ratings are made on a 5-star scale, with half-star increments.

Timestamps represent seconds since midnight Coordinated Universal Time (UTC) of January 1, 1970.
"""

