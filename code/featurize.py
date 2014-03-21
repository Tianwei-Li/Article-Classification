#!/usr/bin/env python

import sys

def featurize(train_articles, test_articles):
    '''
    Returns a tuple (train_features, test_features) of matrices of
    features. Each matrix is list of feature vectors, where a feature vector is
    simply a list of numbers. Note that features must be converted here to the
    proper numerical type (e.g., booleans should be converted to integers).
        
    You may find that returning a list of feature vectors is too
    memory-intensive. You can reduce memory usage considerably by defining the
    matrix as a Python generator that yields feature vectors, instead of
    building the whole list of vectors. For example, if your matrix was defined
    as [make_features(article) for article in articles], you could instead write
    (make_features(article) for article in articles). See
    https://wiki.python.org/moin/Generators for more details on
    generators. (Note that this approach may increase running time.)

    If you would like to examine an actual instance of the return type, try
    running the following function call using the default implementation:
       featurize(['train 1', 'training article 2'], ['test 1', 'the second test article'])
    and inspecting the return value.
    '''

    ### REPLACE THE REST OF THIS FUNCTION WITH YOUR FEATURE GENERATION CODE ###
    def make_features(articles):
        return [[len(article.split()), int(article.startswith('the'))] for article in articles]
    return (make_features(train_articles), make_features(test_articles))

def articles_to_features(train_in_name, train_out_name, test_in_name, test_out_name):
    with open(train_in_name, 'r') as in_file:
        train_lines = in_file.readlines()
    with open(test_in_name, 'r') as in_file:
        test_lines = in_file.readlines()

    train_features, test_features = featurize(train_lines, test_lines)

    for features, out_name in ((train_features, train_out_name),
                               (test_features, test_out_name)):
        with open(out_name, 'wb') as csvfile:
            # Output features in MATLAB-readable CSV format
            for row in features:
                csvfile.write(', '.join([str(feature) for feature in row]))
                csvfile.write('\n')

if __name__ == '__main__':
    articles_to_features(*sys.argv[1:5])
