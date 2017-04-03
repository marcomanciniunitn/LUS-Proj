LUS mid-term project, Spring 2017
Student: Marco Mancini, 187403

#### Description ####
#1- Basic Project
   This is the basic part of the project, it performs sequence labeling. 
   The main operations it does are:
   1- Create the lexicon
   2- Calculate the likelihoods (probabilities of words given the concept) 
   using the training set
   3- Train both the WFST for the likelihood and the LM (the LM is generated using opengram) 
   , taking care about unknowns and giving the possibility to change the size of the ngram,
   the smoothing and to use or not the frequency cut-off on the likelihoods.
   4- Evaluate the trained model on a test set

#### HOW-TO USE####
#1- Basic Project
   Do not touch any file in the Basic Project directory, use the following arguments
   to launch the project:
   1- arg1 = order [1-3]
   2- arg2 = smoothing [| absolute || katz || kneser_ney || presmoothed || unsmoothed || witten_bell |] 
   3- arg3 = threshold for the cut-off frequency (0- No cut-off)
   4- arg4 = test set 
   
   Once finished, the results will be showed into the results directory, the performance file indicate in its
   name all the parameters set (i.e. performancesabsolute_1_0.txt indicates an absolute smoothing, unigrams and
   threshold for the cut-off set to 0 (no cut-off in this case) ).
'''
