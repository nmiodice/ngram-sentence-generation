from wordprob import WordGenerator
from nltk.util import ngrams
from util import Utilities
from text import TextUtils
import word_predictor
import nltk.corpus
import argparse
import pickle
import random
import sys
import os

# the default filename for the ngram hash saved after training
NGRAM_HASH_NAME = 'ngram_hash.pkl'

# Trains the word generator on a number of NGRAM sources. The sources can be
# specified in a list (or any iterable container) using LIST_OF_CORPUS. The type
# must be of NLTK.CORPUS, and must implement the WORDS() method, which returns
# an iterable container of words. An existing WordProb object can be passed in
# using the WORD_GEN parameter
def train_on_corpus(ngram_size, 
    list_of_corpus = [nltk.corpus.brown, nltk.corpus.abc], word_gen = None):
    for i in range(len(list_of_corpus)):
        words = ' '.join(list_of_corpus[i].words())
        cleaned_words = TextUtils.normalize_line(words)
        ngram = ngrams(cleaned_words, ngram_size)
        if i == 0:
            word_gen = WordGenerator(ngram)
        else:
            word_gen.add_list_of_ngrams(ngram)
    return word_gen
    
# Trains the word generator on a number of plain text sources. The sources can
# be specified in a list (or any iterable container) using LIST_OF_CORPUS. An 
# existing WordProb object can be passed in using the WORD_GEN parameter
def train_on_plain_text(ngram_size, list_of_files, word_gen = None):
    word_gen = None
    for file in list_of_files:
        ng = TextUtils.file_to_ngram(file, ngram_size)
        if ng == None:
            sys.exit("Fatal Error: file '%s' cannot be opened" % file)
        if word_gen == None:
            word_gen = WordGenerator(ng)
        else:
            word_gen.add_list_of_ngrams(ng)
    return word_gen

# Produces a string prediction based on the provided seed srings. PREDICTOR
# is a WordProb object trained with any number of ngrams. SEED_STR is a base
# string for which all other predictions will be based. MAX_PREDICTED_WORDS is
# a limit for the length of the produced string           
def predict_words(predictor, seed_str, max_predicted_words):
    # cleans the lines and returns an array of individual words, in order
    # of appearance in string
    cleaned_string = TextUtils.normalize_line(seed_str)
    seed_str = ' '.join(cleaned_string)    
    for i in range(max_predicted_words):
        # gets only the best matches because NUM_TO_MATCH is 1. See comments
        # of WordProb.get_next_word
        seeds = TextUtils.normalize_line(seed_str)
        candidates = predictor.get_next_words(seeds, num_to_return = 1)
        if candidates == None:
            break
        # now, get a random best choice word
        word_prob_pair = random.choice(candidates)
        next_word = word_prob_pair[0]
        seed_str += ' '
        seed_str += next_word
    return seed_str

# Saves a WordGenerator object to the given file
def save_word_gen(filename, word_gen):
    try:
        file = open(filename, 'wb')
    except:
        sys.exit("Fatal Error: cannot open file '%s' to save word hash")
    pickle.dump(word_gen, file)

# Loads a WordGenerator object to the given file
def load_word_gen(filename):
    if Utilities.is_file(filename) == False:
        sys.exit("Fatal Error: no word hash found for file '%s'. Please \
            re-train the model and try again" % filename)
    try:
        file = open(filename, 'rb')
    except:
        sys.exit("Fatal Error: cannot open word hash '%s' for \
            reading" % filename)
    return pickle.load(file)
    
# Deletes a WordGenerator object if it exists at the given file
def del_word_gen(filename):
    try:
        os.remove(filename)
    except OSError:
        pass

# The main entry point for the word_predictor utility. The tool has a few major
# functionalities, all related to sentence generation using an ngram model.
# Specifically, the tool can:
#   1. Save, load, and delete training datasets into a pickled format
#   2. Retrain on new data, specified by a plain text source file or a corpus
#       from the nltk.corpus package, with parameterized ngram size
#   3. Generate a sentence given a seed string, allowing for length limiting
#
# Usage details can be displayed by using the -h or --help flags
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-dt", "--delete_training_set", 
                    help="delete the currently hashed training set",
                    action="store_true")
    parser.add_argument("-rn", "--retrain_nltk", 
                    help="retrain using a specified corpus from nltk.corpus",
                    action="append")
    parser.add_argument("-rf", "--retrain_file", 
                    help="retrain using a specified text file",
                    action="append")
    parser.add_argument("-n", "--ngram_size",
                    type = int,
                    help="specify the size of the ngrams used for training",
                    action="store")
    parser.add_argument("-s", "--seed_string", 
                    help="predict words starting with a seed string",
                    action="store")
    parser.add_argument("-l", "--limit_length",
                    type = int,
                    default = 20,
                    help="limit the number of words predicted (default = 20)",
                    action="store")
    args = parser.parse_args()
    
    if not len(sys.argv) > 1:
        parser.print_help()
        sys.exit()

    if (args.ngram_size != None) and (args.retrain_nltk == None) \
        and (args.retrain_file == None):
        parser.error('--retrain_nltk or --retrain_file required when \
            --ngram_size specified')
    if args.ngram_size == None:
        args.ngram_size = 3
        
    # delete the model if required
    if args.delete_training_set:
        del_word_gen(NGRAM_HASH_NAME)
    
    # retrain the model if necessary
    word_gen = None
    retrained = False
    if args.retrain_file:
        word_gen = train_on_plain_text(args.ngram_size, args.retrain_file, 
            word_gen)
        retrained = True
    if args.retrain_nltk:
        corpus_list = []
        for c in args.retrain_nltk:
            try:
                corp_obj = getattr(nltk.corpus, c)
            except:
                sys.exit("Fatal Error: corpus '%s' does not exist in \
                    nltk.corpus" % c)
            corpus_list.append(corp_obj)
        word_gen = train_on_corpus(args.ngram_size, corpus_list, word_gen)
        retrained = True
        
    if retrained == True:
        save_word_gen(NGRAM_HASH_NAME, word_gen)

    # generate new words if necessary
    if args.seed_string != None:
        if word_gen == None:
            word_gen = load_word_gen(NGRAM_HASH_NAME)
        args.seed_string = TextUtils.normalize_line(args.seed_string)
        args.seed_string = ' '.join(args.seed_string)
        generated = predict_words(word_gen, args.seed_string, args.limit_length)
        print(generated)