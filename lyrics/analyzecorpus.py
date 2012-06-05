import os
import nltk
from parseSentic import parseSenticNet
from approx_key_dict import approx_key_dict
from nltk.corpus import wordnet as wn
from conceptnet5client import *

# given corpus, assign emotional content to each song
def ngram_lookup(words, size, dictionary):
    count = 0.0
    polarity_sum = 0.0
    for left in xrange(len(words)-size+1):
        right = left+size
        key = ' '.join(words[left:right])
        if dictionary.has_key(key):
            count += 1.0
            polarity_sum += float(dictionary[key])
    return count, polarity_sum
        
def calc_polarity(words, dictionary):
     #for each word, look up polarity in sentic net and calculate value
    count = 0.0
    polarity_sum = 0.0
    # up to 4-word concepts in the dictionary
    for i in range(1,5):
        c, p = ngram_lookup(words, i, dictionary)
        #print i,c, p
        count += c
        polarity_sum += p
    if count > 0:
        polarity_sum = round(polarity_sum/count,3)
    return polarity_sum


def analyze_corpus(dictionary, path='corpus'):
    count = 0
    emotion_dict = approx_key_dict()
    artist_dict = {}
    lyrics_dict = {}
    dirlist = os.listdir(path)
    for filename in dirlist:
        if os.path.splitext(filename)[1] != '.txt':
            continue
        fullname = path+'/'+filename
        words = nltk.word_tokenize(open(fullname).read().decode('ascii','ignore'))
        score = calc_polarity(words, dictionary)
        #print score, filename
        lyrics_dict[filename] = score
       
        artist = filename.split(',')[0]
        if artist_dict.has_key(artist):
            artist_dict[artist].append(score)
        else:
            artist_dict[artist] = [score]
        if emotion_dict.has_key(score):
            emotion_dict[score].append(filename)
        else:
            emotion_dict[score] = [filename]
    return emotion_dict, artist_dict, lyrics_dict
        
##########################################################
# match song by conceptual similarity
def get_similar_conceptnet(word, limit=5):
    return similar_to_concept5(word, limit)

def get_similar_wordnet(word):
    print "GET SIMILAR WORD",word
    result = []
    word_morphy = wn.morphy(word)
    if word_morphy is not None:
        print word_morphy
        for synset in wn.synsets(word_morphy)[0:2]:
            print synset.name
            for hyp in synset.hyponyms()[0:2]:
                term = hyp.name.split('.')[0]
                result.append(term.replace('_',' '))
    return result
            
def genkeywords(phrase, useConceptNet=True, useWordNet=False):
    words = phrase.split()
    words = [w for w in words if not w in nltk.corpus.stopwords.words('english')]
    words = [w.lower() for w in words]
    if not useConceptNet and not useWordNet:
        return words
    totalwords = []
    for word in words:
        if useConceptNet:
            totalwords.extend(get_similar_conceptnet(word))
        if useWordNet:
            totalwords.extend(get_similar_wordnet(word))
    totalwords.extend(words)
    return totalwords

def match_by_context(phrase, path='corpus/', useConceptNet=True, useWordNet=False):
    topscore = 0
    topmatches = []
    toplyrics = []

    keywords = genkeywords(phrase, useConceptNet, useWordNet)
    print keywords
    dirlist = os.listdir(path)
    for filename in dirlist:
        if os.path.splitext(filename)[1] != '.txt':
            continue
        fullname = path+filename
        words = nltk.word_tokenize(open(fullname).read().decode('ascii','ignore'))
        words = [w.lower() for w in words]
        text = " ".join(words)
        
        score = 0
        matchwords=[]
        for keyword in keywords:
            #for each word in the phrase, check to see if it's in the lyrics
            if keyword in text:
                score += 1
                matchwords.append(keyword)
        if score > topscore:
            topscore = score
            topmatches = [(filename, matchwords)]
        elif score == topscore:
            topmatches.append((filename, matchwords))
    toplyrics = [(f[0], open(path+f[0]).read().decode('ascii', 'ignore')) for f in topmatches]
    return topscore, topmatches, toplyrics

##########################################################
# match song by emotional content
def match_by_sentiment(sent, sentic_corpus, emotion_dict, lyrics_dict, path='corpus/'):
    words = sent.split()
    words = [w for w in words if not w in nltk.corpus.stopwords.words('english')]
    score = calc_polarity(words, sentic_corpus)
    topfilenames = emotion_dict[score]
    topsongs = [(f, lyrics_dict[f]) for f in topfilenames]
    toplyrics = map(lambda x: (x, open(path+x).read().decode('ascii','ignore')), topfilenames)
    return score, topsongs, toplyrics
            
if __name__ == "__main__":
    print 'analyzecorpus loaded'
    #sentic_corpus = parseSenticNet()
    #emotion_dict, artist_dict, lyrics_dict = analyze_corpus(sentic_corpus)

