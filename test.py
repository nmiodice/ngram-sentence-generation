from nltk.util import ngrams
from util import Utilities
from text import TextUtils
from wordprob import NgramProb
from wordprob import WordProb
from wordprob import WordGenerator

# Some constants. If testing materials are moved, reflect it here
TST_DIR = "testing_docs/"
TXT_NORMAL_FILE = "test_normalize.txt"
TXT_NORMAL_FILE_EXP = "test_normalize_expected.txt"
TXT_FILE_TO_NGRAM = "test_file_to_ngram.txt"


# Entry point for all text.py class method tests
def run_test_suite():
	run_text_tests()
	run_word_prob_tests()
	
# Test NgramProb, WordProb, and WordGenerator
def run_word_prob_tests():
    test_ngram_prob()
    test_word_prob()
    test_word_generator()
    
def test_word_generator():
    str = "hello world, I am Nick Iodice"
    str += " and I really like to go skiing."
    str += "Hello world, Alex is a friend of mine"
    str += "a b c d a b c d a b d"

    strContent = TextUtils.normalize_line(str)
    ng = ngrams(strContent, 3)
    wg = WordGenerator(ng)    
    match = wg.get_next_words(['hello', 'world'])
    assert (match[0][0] == 'alex') or (match[0][0] == 'i')
    assert (match[1][0] == 'alex') or (match[1][0] == 'i')
    assert len(match) == 2

    match = wg.get_next_words(['ignore', 'hello', 'world'], 
        min_preceding_match = 2)
    assert (match[0][0] == 'alex') or (match[0][0] == 'i')
    assert (match[1][0] == 'alex') or (match[1][0] == 'i')
    assert len(match) == 2
    
    # should have length 2, because each word has equal probability
    match = wg.get_next_words(['hello', 'world'], num_to_return = 1)
    assert (match[0][0] == 'alex') or (match[0][0] == 'i')
    assert len(match) == 2

    # each word does not have equal probability, so the expected length is 1
    match = wg.get_next_words(['alex', 'is'], num_to_return = 1)
    assert (match[0][0] == 'a')
    assert len(match) == 1
    
    match = wg.get_next_words(['ignore', 'hello', 'world'], 
        min_preceding_match = 2, num_to_return = 2)
    assert (match[0][0] == 'alex') or (match[0][0] == 'i')
    assert (match[1][0] == 'alex') or (match[1][0] == 'i')
    assert len(match) == 2
        
    print("PASSED: WordGenerator")
    
# test WordProb
def test_word_prob():
    str = "one two three"
    str += " one two three"
    str += " one two nine"
    str += " a b c"
    str += " b c d" 
    strContent = TextUtils.normalize_line(str)
    
    # first we try to add the words, and ensure that bad input is properly
    # rejected
    ng = ngrams(strContent, 1)
    word_prob = WordProb()
    try:
        # this should fail because ng size is 1
        for gram in ng:
            word_prob.add_ngram_observation(gram)
    except:
        # this is expected
        pass
    else:
        assert 0 == 1
        
    ng = ngrams(strContent, 3)
#    for gram in ng:
    word_prob.add_ngram_observations(ng)

    # now that the words are added, see if the calculations are correct
    words = word_prob.get_word_likelihood(['one', 'two'])
    assert len(words) == 2
    assert words[0][0] == 'three'
    assert words[0][1] == 2/3
    assert words[1][0] == 'nine'
    assert words[1][1] == 1/3
    assert word_prob.get_word_likelihood(['one', 'two', 'three']) == None
    assert word_prob.get_word_likelihood([]) == None
    assert word_prob.get_word_likelihood(['one', 'three']) == None
    
    print("PASSED: WordProb")
   
# Test NgramProb
def test_ngram_prob():
    ngp = NgramProb('fake key')
    assert ngp.total_words_seen == 0
    assert len(ngp.get_sorted_word_likelihood()) == 0
    
    for i in range(30):
        if i < 10:
            ngp.add_word_observation('hello')
        if i < 20:
            ngp.add_word_observation('world')
        ngp.add_word_observation('nick')
    assert ngp.total_words_seen == 60
    word_likelihoods = ngp.get_sorted_word_likelihood()
    assert len(word_likelihoods) == 3
    assert word_likelihoods[0][0] == 'nick'
    assert word_likelihoods[0][1] == 1/2
    assert word_likelihoods[1][0] == 'world'
    assert word_likelihoods[1][1] == 1/3
    assert word_likelihoods[2][0] == 'hello'
    assert word_likelihoods[2][1] == 1/6
    print("PASSED: NgramProb")  
    
# Test TestUtils
def run_text_tests():
	textutils_normalize_line()
	textutils_file_to_ngram()
	print("PASSED: TextUtils")

# Test TextUtils.normalize_line
def textutils_normalize_line():
	expected_file = Utilities.open_file(TST_DIR + TXT_NORMAL_FILE_EXP)
	expected_output = []
	for line in expected_file:
		# need to strip new line characters
		expected_output += line.rstrip().split()

    # this constructs a list where each element is the normalized version
    # of the corresponding line in the file
	test_file = Utilities.open_file(TST_DIR + TXT_NORMAL_FILE)
	test_output = []
	for line in test_file:
		test_output += TextUtils.normalize_line(line)
	assert test_output == expected_output

# Test TextUtils.file_to_ngram
def textutils_file_to_ngram():
	ng = TextUtils.file_to_ngram("fake file", 3)
	assert ng == None

	ng = TextUtils.file_to_ngram(TST_DIR + TXT_FILE_TO_NGRAM, 0)
	assert ng == None
	ng = TextUtils.file_to_ngram(TST_DIR + TXT_FILE_TO_NGRAM, -1)
	assert ng == None
	ng = TextUtils.file_to_ngram(TST_DIR + TXT_FILE_TO_NGRAM, 1)
	assert ng != None

	ng = TextUtils.file_to_ngram(TST_DIR + TXT_FILE_TO_NGRAM, 3)
	assert ng != None
	i = 0
	for gram in ng:
		i += 1
	assert i > 0


if __name__ == "__main__":
	run_test_suite()
	