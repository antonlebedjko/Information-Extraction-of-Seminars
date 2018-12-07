import nltk
from nltk.corpus import brown
from nltk.corpus import treebank
from nltk.tag import DefaultTagger
from nltk.tag import UnigramTagger
from nltk.tag import BigramTagger
from nltk.tag import TrigramTagger

brown.tagged_words(tagset = 'universal')


train_sents = treebank.tagged_sents()[:3500]
test_sents = treebank.tagged_sents()[3500:]
tagger = DefaultTagger('NN')


def back_off_tagger(train_sents,tagger_classes, backoff=None):
    for cls in tagger_classes:
        backoff = cls(train_sents,backoff=backoff)
    return backoff


tagger = back_off_tagger(train_sents,[UnigramTagger,BigramTagger,TrigramTagger],backoff=DefaultTagger('NN'))

tagged = tagger.tag(["The", "lecture", "will","be","in", "Wean", "4623"])
print(tagged)
print (tagger.evaluate(test_sents))
