LUS mid-term project, Spring 2017 <br />
Student: Marco Mancini, 187403 <br />

----- DESCRIPTION ----- <br />
- Basic Project <br />
  This is the basic part of the project, it performs sequence labeling. <br />
   The main operations it does are: <br />
   - Create the lexicon <br />
   - Calculate the likelihoods (probabilities of words given the concept) <br />
   using the training set
   - Train both the WFST for the likelihood and the LM (the LM is generated using opengram),taking care about unknowns and giving the possibility to change the size of the ngram,
   the smoothing and to use or not the frequency cut-off on the likelihoods.
   - Evaluate the trained model on a test set <br />

- Advanced Project 1 (PoS + Lemma) 
   This is the first advanced part of the project, it performs sequence labeling. 
   The main operations it does are:
   1- Create the lexicon
   2- Calculate the likelihoods (probabilities of words given the concept) 
   using the training set
   3- Train both the WFST for the likelihood and the LM (the LM is generated using opengram) 
   , taking care about unknowns and giving the possibility to change the size of the ngram,
   the smoothing and to use or not the frequency cut-off on the likelihoods.
   4- Evaluate the trained model on a test set
   5- Give the possibility to add features to the computation. It is possible to take into account
   Word + PoS or Lemma + PoS, depending on the specified paramete


----- HOW-TO USE ----- <br />
Do not touch any file in any folder, the results are showed in the results folder of each project. 
- Basic Project <br />
   -Syntax- <br />
   - arg1 = order [1-3] <br />
   - arg2 = smoothing [| absolute || katz || kneser_ney || presmoothed || unsmoothed || witten_bell |]  <br />
   - arg3 = threshold for the cut-off frequency (0- No cut-off) <br />
   - arg4 = Word cut-off | Noise cut-off [1 = Word-cutoff, 0 = Noise-cutoff]  <br />
   - arg5 = test set file <br />
   
   Once finished, the results will be showed into the results directory, the performance file indicate in its
   name all the parameters set (i.e. performancesabsolute_1_0.txt indicates an absolute smoothing, unigrams and
   threshold for the cut-off set to 0 (no cut-off in this case) ). 

- Advanced Project 1 (PoS + Lemma)
   -Syntax- <br />
   1- arg1 = order [1-3]
   2- arg2 = smoothing [| absolute || katz || kneser_ney || presmoothed || unsmoothed || witten_bell |] 
   3- arg3 = threshold for the cut-off frequency (0- No cut-off)
   4- arg4 = Word cut-off | Noise cut-off [1 = Word-cutoff, 0 = Noise-cutoff] 
   5- arg5= Add features (0: WORD-PoS , 1: LEMMA-PoS)

   The results are saved in the results directory as for the Basic Project.

