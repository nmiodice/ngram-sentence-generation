Welcome!
===================
You've made it to the README file for (insert cool name here), a sentence generator that uses statistics to predict the most likely next words in a sentence.

---
Notes:
---
While the generated sentences do look like real sentences, they often times don't make sense, and thats OK. The goal of this code is to:
> - Showcase sentence generation using the ngram model
> - Showcase how bad sentence generation can be using the ngram model

If you are unfamiliar with the ngram model, it works like so:
> - Break input sentences into sequences of length **n**. For example, if n = 3, "The brown fox jumps" becomes ['the', 'brown', 'fox], ['brown', 'fox', 'jumps']
> - Calculate how frequently sets of words show up together
> - Predict the next word based off the frequency of previously seen word sets
> - Rinse and repeat

So, there are many limitations of this model, but hey, it is fun to play around with!

----------

> **Requiremenets:**

> - python3
> - natural language tool kit: nltk
> - nltk corpus packages (technically optional, but definitely recommended)

---

**Usage Examples:**
Display help:
```
$ python3 word_predictor.py --help
usage: word_predictor.py [-h] [-dt] [-rn RETRAIN_NLTK] [-rf RETRAIN_FILE]
                         [-n NGRAM_SIZE] [-s SEED_STRING] [-l LIMIT_LENGTH]

optional arguments:
  -h, --help            show this help message and exit
  -dt, --delete_training_set
                        delete the currently hashed training set
  -rn RETRAIN_NLTK, --retrain_nltk RETRAIN_NLTK
                        retrain using a specified corpus from nltk.corpus
  -rf RETRAIN_FILE, --retrain_file RETRAIN_FILE
                        retrain using a specified text file
  -n NGRAM_SIZE, --ngram_size NGRAM_SIZE
                        specify the size of the ngrams used for training
  -s SEED_STRING, --seed_string SEED_STRING
                        predict words starting with a seed string
  -l LIMIT_LENGTH, --limit_length LIMIT_LENGTH
                        limit the number of words predicted (default = 20)
```

Retrain model on the **brown** and **abc** corpora, and generate a prediction from the seed sentence "saturated fats"
```
$ python3 word_predictor.py --retrain_nltk brown --retrain_nltk abc --seed_string "saturated fats"
outputs:
saturated fats can accommodate no more than a hundred years ago and that s the matter of fact this latter failure is
```
