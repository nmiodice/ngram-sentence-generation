from nltk.corpus import brown
from nltk.util import ngrams
from wordprob import WordGenerator
from text import TextUtils
import random
import sys

# trains the word generator on a number of NGRAM sources
def train():
    words = brown.words()
    cleaned_words = []
    for word in words:
        clean = TextUtils.normalize_line(word)
        if clean != []:
            cleaned_words.append(clean[0])
    ngram = ngrams(cleaned_words, 3)
    word_gen = WordGenerator(ngram)
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
    print(seed_str)
        
        
    

def simple_word_predictor(seed_str, limit = 10):
    print("Training data...")
    predictor = train()
    predict_words(predictor, seed_str, limit)

if __name__ == "__main__":
    
    simple_word_predictor(sys.argv[1])
    
    
#import simple_word_predictor
#wg = simple_word_predictor.train()