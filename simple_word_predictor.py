import word_predictor as wp
import nltk
import sys

def simple_word_predictor(seed_str, limit = 10):
    print("Training data...")
    predictor = wp.train_on_corpus(3, [nltk.corpus.brown, nltk.corpus.abc])
    predicted = wp.predict_words(predictor, seed_str, limit)
    print(predicted)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print('Usage:\n\t%s "<seed sentence>"' % sys.argv[0])
    else:
        simple_word_predictor(sys.argv[1])
    