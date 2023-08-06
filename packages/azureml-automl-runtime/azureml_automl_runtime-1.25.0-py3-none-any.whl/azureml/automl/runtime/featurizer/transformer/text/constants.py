# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
"""Constants for various tranformers."""


class TFIDF_VECTORIZER_CONFIG:
    """Param values for TFIDF Vectorizer."""
    USE_IDF = False
    NORM = 'l2'
    MAX_DF = 0.95
    CHAR_ANALYZER = 'char'
    CHAR_NGRAM_RANGE = (3, 3)
    WORD_ANALYZER = 'word'
    WORD_NGRAM_RANGE = (1, 2)
    SUBSAMPLE_SIZE = 10000
    MIN_WORD_NGRAM = 2


class NIMBUS_ML_PARAMS:
    """Param keys/values for NimbusML pipeline."""
    FEATURIZER_KEY = "featurizer"
    CLASSIFIER_KEY = "classifier"
    NGRAM_CHAR_WEIGHTING = "Tf"
    NGRAM_CHAR_KEY = 'char_feature_extractor'   # keyword arg for NimbusML ngram char_feature_extractor
    NGRAM_CHAR_LENGTH_KEY = 'ngram_char_length'
    NGRAM_CHAR_LENGTH = 3
    NGRAM_CHAR_ALL_LENGTHS = False
    NGRAM_WORD_WEIGHTING = "Tf"
    NGRAM_WORD_KEY = 'word_feature_extractor'   # keyword arg for NimbusML ngram word_feature_extractor
    NGRAM_WORD_LENGTH_KEY = 'ngram_word_length'
    NGRAM_WORD_LENGTH = 2
    NGRAM_WORD_ALL_LENGTHS = True
    AVG_PERCEPTRON_ITERATIONS = 10
    NIMBUS_ML_PACKAGE_NAME = "nimbusml"
