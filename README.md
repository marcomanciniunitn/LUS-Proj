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
   This is the first advanced part of the project, it performs sequence labeling. All the functions are basically the same with respect to the basic project but here we've added 
2 more functions to adapt the train/test sets in order to work well on the advanced features.
   The main operations it does are:
   - Create the lexicon
   - Calculate the likelihoods (probabilities of words given the concept) 
   using the training set
   - Train both the WFST for the likelihood and the LM (the LM is generated using opengram) 
   , taking care about unknowns and giving the possibility to change the size of the ngram,
   the smoothing and to use or not the frequency cut-off on the likelihoods.
   - Evaluate the trained model on a test set
   - Give the possibility to add features to the computation. It is possible to take into account
   Word + PoS or Lemma + PoS, depending on the specified paramete

- Advanced Project 2 (Clusters) 

This was a test to see if the clusters of concepts with more performance dispersions give better performances. 
What is changed with respect to the other versions is the following composition of machines:
1- Word -> Cluster, this transducer basically map words into cluster of concepts (if the word should not be mapped to any cluster than it is mapped to its concept)
2- Cluster -> Concept, this transducer re-map the clusters into concepts (the likelihoods has been calculated as C(Cluster, Concept)/C(Cluster))
3- Language Model for the concepts

These three machines then have been composed and tested, but the performances (FB1 measure particularly) has been dropped of 4/5%, then I've decided not to continue
with this implementation.

- Advanced Project 3 (O to Concepts)

This is the best and last version of the project, it is basically the Basic Project but works on an edited training set.
The training set has been modified assigning as concept for each word the word itself instead of the O (obviously only when possible), this editing permitted me to reach the ~83% F1-Measure and ~95% of accuracy.
Initially only the most discriminant words where mapped to concept (thanks to @Federico Giannoni for the script generating the concepts for the specified words), this gave me better results, then I tried to use the whole words, and this last trial worked well.


----- HOW-TO USE ----- <br />
Do not touch any file in any folder, the results are showed in the results folder of each project. 
- Basic Project <br />
   -Syntax- <br />
   - arg1 = order [1-3] <br />
   - arg2 = smoothing [| absolute || katz || kneser_ney || presmoothed || unsmoothed || witten_bell |]  <br />
   - arg3 = threshold for the cut-off frequency (0- No cut-off) <br />
   - arg4 = Word cut-off | Noise cut-off [1 = Word-cutoff, 0 = Noise-cutoff]  <br />
   
   Once finished, the results will be showed into the results directory, the performance file indicate in its
   name all the parameters set (i.e. performancesabsolute_1_0.txt indicates an absolute smoothing, unigrams and
   threshold for the cut-off set to 0 (no cut-off in this case) ). 

- Advanced Project 1 (PoS + Lemma) <br />
   -Syntax- <br />
   - arg1 = order [1-3]
   - arg2 = smoothing [| absolute || katz || kneser_ney || presmoothed || unsmoothed || witten_bell |] 
   - arg3 = threshold for the cut-off frequency (0- No cut-off)
   - arg4 = Word cut-off | Noise cut-off [1 = Word-cutoff, 0 = Noise-cutoff] 
   - arg5= Add features (0: WORD-PoS , 1: LEMMA-PoS)

   The results are saved in the results directory as for the Basic Project.

- Advanced Project 2 (Clusters) <br />
   Do not test it, it is only present in the directory since it was tested but with no good results.

- Advanced Project 3 (O to concepts) <br />
   -Syntax- <br />
   - arg1 = order  <br />
   - arg2 = smoothing [| absolute || katz || kneser_ney || presmoothed || unsmoothed || witten_bell |]  <br />
   - arg3 = threshold for the cut-off frequency (0- No cut-off) <br />
   - arg4 = Word cut-off | Noise cut-off [1 = Word-cutoff, 0 = Noise-cutoff]  <br />



