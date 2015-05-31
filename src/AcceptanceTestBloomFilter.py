from BloomFilter import BloomFilter
import random
import string

def removeMatchingWord( aWordToFind, aWords ):
    if aWordToFind in aWords:
        aWords.remove( aWordToFind )

if __name__ == '__main__':
    theBloomFilter = BloomFilter()
    [theBloomFilter.addWord( line.strip() ) for line in open('/usr/share/dict/words')]

    theWrongWords = []
    theCountOfRandomWords = 0

    while len(theWrongWords) < 300:
        theCountOfRandomWords = theCountOfRandomWords + 1
        theRandomString = ''.join(random.choice(string.ascii_lowercase) for x in range(5))

        if ( theBloomFilter.checkWord( theRandomString ) ):
            theWrongWords.append( theRandomString )

    print '# random words checked: ' + str( theCountOfRandomWords )

    [ removeMatchingWord( line.strip(), theWrongWords ) for line in open('/usr/share/dict/words')]

    print '# false positives: ' + str( len( theWrongWords ) )

    print 'false positive rate: ' + str( 100.0 * float( len( theWrongWords ) ) / float( theCountOfRandomWords ) )
