LUS mid-term project, Spring 2017 <br />
Student: Marco Mancini, 187403 <br />

-----Description-----<br />
1- Basic Project <br />
&emsp This is the basic part of the project, it performs sequence labeling. <br />
   The main operations it does are: <br />
   1- Create the lexicon <br />
   2- Calculate the likelihoods (probabilities of words given the concept) <br />
   using the training set
   3- Train both the WFST for the likelihood and the LM (the LM is generated using opengram) <br />
   , taking care about unknowns and giving the possibility to change the size of the ngram,
   the smoothing and to use or not the frequency cut-off on the likelihoods.
   4- Evaluate the trained model on a test set <br />

-----HOW-TO USE-----
#1- Basic Project
   Do not touch any file in the Basic Project directory, use the following arguments to launch the project:<br />
   1- arg1 = order [1-3] <br />
   2- arg2 = smoothing [| absolute || katz || kneser_ney || presmoothed || unsmoothed || witten_bell |]  <br />
   3- arg3 = threshold for the cut-off frequency (0- No cut-off) <br />
   4- arg4 = test set <br />
   
   Once finished, the results will be showed into the results directory, the performance file indicate in its
   name all the parameters set (i.e. performancesabsolute_1_0.txt indicates an absolute smoothing, unigrams and
   threshold for the cut-off set to 0 (no cut-off in this case) ).
'''
