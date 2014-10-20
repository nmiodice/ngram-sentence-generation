import operator
import sys
from nltk.util import ngrams


# Top level handler that uses ngrams to suggest the next likely word in a
# sequence
class WordGenerator:
    
    # Class Members:
    #   self.word_probs: The top level object that manages ngrams and converting
    #       ngram data into probabilities
    
    # Creates a new WordGenerator using a given NG, which is of type 
    # NLTK.UTIL.NGRAMS. While the object is initialized with just one NG, 
    # more can be added later. An optional parameter is INCLUDE_SHORTER_GRAMS,
    # which if true, will include ngrams shorter than the original set of
    # ngrams (i.e., if a 5gram is included, 4gram, 3gram and 2grams will be
    # saved too)
    def __init__(self, ng, include_shorter_grams = True):
        self.word_probs = WordProb()
        self.add_list_of_ngrams(ng, include_shorter_grams)

    # Adds an NG of type NLTK.UTIL.NGRAMS to the list of words in the master
    # dictionary inside self.word_probs. An optional parameter is 
    # INCLUDE_SHORTER_GRAMS, which if true, will include ngrams shorter than the
    # original set of ngrams (i.e., if a 5gram is included, 4gram, 3gram and 
    # 2grams will be saved too)
    def add_list_of_ngrams(self, ng, include_shorter_grams = True):
        self.word_probs.add_ngram_observations(ng, include_shorter_grams)
    
    # Returns a sorted list of the most likely words that will come after
    # the sequence of of strings in WORDS, according to the NGRAMS added with 
    # ADD_LIST_OF_NGRAMS, or through the constructor. MIN_PRECEDING_MATCH
    # is the minimum number of elements from WORDS that must match for the
    # method to return a valid next word. NUM_TO_RETURN indicates how many
    # of the highest ranked choices should be returned. If no matches are found,
    # NONE is returned. 
    #
    # Notes:
    #   1. The returned value is matched against the largest possible number of
    #       matched terms. That is, ['hello', 'world'] will be matched before
    #       ['hello'], and ['hello'] will never be considered alone if
    #       ['hello', 'world'] is matched
    #
    #   2. If NUM_TO_RETURN specifies some value, and cutting the returned
    #       list short at NUM_TO_RETURN element would cut out equally as well
    #       matched terms, all of the equally as well matched terms will be
    #       returned
    #
    #   3. If NUM_TO_RETURN is 1 (default), then only the best matched words
    #       are returned
    def get_next_words(self, words, min_preceding_match = -1, 
        num_to_return = 1):
        
        if num_to_return < 0:
            num_to_return = 1

        match = False
        matches = None
        while (match == False) and (min_preceding_match <= len(words)):
            matches = self.word_probs.get_word_likelihood(words)
            if matches != None:
                match = True
            else:
                words = words[1:]
                if len(words) == 0:
                    break
        if matches == None:
            return None

        # now, filter out matches and return at least NUM_TO_RETURN elements,
        # as specified in the comments for this method
        min_match_set = matches[0:num_to_return]
        matches = matches[num_to_return:]
        while len(matches) > 0 and (min_match_set[-1][1] == matches[0][1]):
            min_match_set.append(matches.pop(0))
        return min_match_set
  
# Maintains a list of probabilities associated with a set of ngrams.
class WordProb:

    # Class Members:
    #   self.master: The top-level dictionary that maintains access to the 
    #       probabilities of each word associated with an ngram. For example,
    #       if three ngrams are observed that have the first word = 'my' and
    #       second word is 'name', self.master.get('my_name') gives access to 
    #       the probabilities of the next word in the sequence    

    # Creates a WORDPROB object initialized with an ngram passed in as NG.
    # NG is of type NLTK.UTIL.NGRAMS. NG holds ngrams of size 2 or more
    def __init__(self):
        self.master = dict()
    
    # Convert an ngram into a key and value pair, which is then stored in
    # the master dictionary. An optional parameter is INCLUDE_SHORTER_GRAMS,
    # which if true, will include ngrams shorter than the original set of
    # ngrams (i.e., if a 5gram is included, 4gram, 3gram and 2grams will be
    # saved too)
    def add_ngram_observations(self, ng, include_shorter_grams = True):
        for ng_tuple in ng:
            num_keys = len(ng_tuple) - 1
            assert(num_keys) >= 1
            observed_word = ng_tuple[-1]

            keys = []
            append = keys.append
            if include_shorter_grams == True:
                for i in range(num_keys):
                    append('_'.join(ng_tuple[0:i + 1]))
            else:
                append('_'.join(ng_tuple[0:num_keys]))
            
            for key in keys:
                try:
                    self.master[key].add_word_observation(observed_word)
                except:
                    self.master[key] = NgramProb(key)
                    self.master[key].add_word_observation(observed_word)

    # Get the likelihood of a particular word given a list of preceding words
    # in the PRECEDING_WORDS list. Returns None if no key is matched in 
    # self.master
    def get_word_likelihood(self, preceding_words):
        key = ""
        for word in preceding_words:
            key += word
            key += '_'
        key = key[0:-1]

        if key in self.master:
            return self.master[key].get_sorted_word_likelihood()
        else:
            return None
        
# Holds information about the count of 'next' words seen after some undefined
# sequence of words
class NgramProb:
    # Class Members:
    #   self.seen_next_words: A dictionary that holds information about which
    #       words might be the next word. Keys are words, values are
    #       the count of times that word has been seen
    #   self.total_words_seen: A count of how many words have been added
    #   self.key: The key that led to these word observations

    def __init__(self, key):
        self.seen_next_words = dict()
        self.total_words_seen = 0
        self.key = key
    
    # Add a word to the observation dictionary, or create a new entry if
    # the word hasn't been seen yet
    def add_word_observation(self, word):
        if word in self.seen_next_words:
            self.seen_next_words[word] += 1
        else:
            self.seen_next_words[word] = 1;
        self.total_words_seen += 1
            
    # Returns a list of tuples in the following format:
    #   [(most common word, probability), (2nd most common, probability...)
    def get_sorted_word_likelihood(self):
        sorted_by_prob = []
        for key, count in self.seen_next_words.items():
            sorted_by_prob.append((key, count/self.total_words_seen))

        sorted_by_prob = sorted(sorted_by_prob, key=operator.itemgetter(1), 
            reverse = True)
        return sorted_by_prob
        
        
        
