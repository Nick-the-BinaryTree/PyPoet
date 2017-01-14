import nltk
import pronouncing
import sys
from urllib.request import Request, urlopen
from random import randint

def getRhymes(word):
    return pronouncing.rhymes(word.lower())


def isRhyme(word1, word2, rhymes):
    isPass = word2 in rhymes
    print("Do " + word2 + " and " + word1 + " rhyme? " + str(isPass))
    return isPass

def getSentences(fileName):
    if fileName[:4] == "http":
        req = Request(fileName, headers={'User-Agent': 'Mozilla/5.0'})
        data = urlopen(req).read().decode('utf-8', errors="replace")
    else:
        fp = open(fileName)
        data = fp.read()
    tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')
    final = []
    for sen in tokenizer.tokenize(data):
        final.append(sen.replace("\n"," "))
    return final

def isBase(foundCount):
    return foundCount % 2 == 0

def clean(s):
    s = s.rstrip('?:!.,;"\'')
    return s.lstrip('?:!.,;"\'')

def getLastWord(sen):
    lastWord = sen.split()[-1]
    lastWord = clean(lastWord)
    return lastWord.lower()

def senChecks(sen, rhymeWith, foundCount, SENTENCE_LENGTH, SENTENCE_THRESHOLD, RHYMES_THRESHOLD = 3):

    fitsLength = SENTENCE_LENGTH - SENTENCE_THRESHOLD <= len(sen.split()) \
           <= SENTENCE_LENGTH + SENTENCE_THRESHOLD
    lastWord = getLastWord(sen)
    rhymes = getRhymes(lastWord)

    if isBase(foundCount):
        return fitsLength and len(rhymes) > RHYMES_THRESHOLD
    else:
        return fitsLength and isRhyme(lastWord, rhymeWith, rhymes)

def buildPoem(sentences, START_INDEX, TOTAL_LINES, SENTENCE_LENGTH, SENTENCE_TARGET):
    if START_INDEX < 0 or START_INDEX > len(sentences):
        START_INDEX = randint(0, len(sentences))
    foundCount = 0
    lastWord = ""
    final = ""

    for i in range(START_INDEX, len(sentences)):
        if not foundCount < TOTAL_LINES:
            break

        sen = sentences[i]
        # print("Checking " + sen)

        if senChecks(sen, lastWord, foundCount, SENTENCE_LENGTH, SENTENCE_TARGET):
            foundCount += 1
            lastWord = getLastWord(sen)
            print("Last Word: " + lastWord)
            final += clean("".join(sen)) + "\n"
            if isBase(foundCount):
                final+="\n"

    if foundCount < TOTAL_LINES:
        final += "\n Could not complete."

    return final

def main():

    # Defaults
    TOTAL_LINES = 8  # Number of lines in final poem
    SENTENCE_LENGTH = 5  # Target length of poem sentences
    SENTENCE_THRESHOLD = 5  # Allowed variation from target sentence length
    START_INDEX = 0

    if len(sys.argv) != 2 and len(sys.argv) != 6:
        print("Format: PyPoet [file location] \n" \
              "Optional: \n" \
              "[sentence index to start building poem at (negative for random)] \n" \
              "[result number of poem lines]\n" \
              "[target line sentence length] \n" \
              "[threshold on target sentence length]")
    else:
        if len(sys.argv) > 2:
            try:
                if sys.argv[2]:
                    START_INDEX = int(sys.argv[2])
                if sys.argv[3]:
                    TOTAL_LINES = int(sys.argv[3])
                if sys.argv[4]:
                    SENTENCE_LENGTH = int(sys.argv[4])
                if sys.argv[5]:
                    SENTENCE_THRESHOLD = int(sys.argv[5])
            except:
                print("You must have all the optional parameters if you want to use them.")
                print("Also, they all must be integers.")

        try:
            if TOTAL_LINES < 0:
                TOTAL_LINES = 0
            if SENTENCE_LENGTH < 0:
                SENTENCE_LENGTH = 0
            if SENTENCE_THRESHOLD < 0:
                SENTENCE_THRESHOLD = 0
            print("File location: " + sys.argv[1])
            print("Start index: " + str(START_INDEX))
            print("Total poem lines: " + str(TOTAL_LINES))
            print("Target sentence length: " + str(SENTENCE_LENGTH))
            print("Target sentence length threshold: " + str(SENTENCE_THRESHOLD))
            print()
            print("\n\n" + buildPoem(getSentences(sys.argv[1]), START_INDEX, TOTAL_LINES, SENTENCE_LENGTH, SENTENCE_THRESHOLD))
        except TypeError as e:
            print(e)
            print("Probably invalid file location.")

if __name__ == "__main__":
    main()

"""
Requires:
NLTK
NTLK punkt tokenizers
Prounouncing

Sources:
http://stackoverflow.com/questions/4576077/python-split-text-on-sentences
Bird, Steven, Edward Loper and Ewan Klein (2009), Natural Language Processing with Python. O’Reilly Media Inc.
"""