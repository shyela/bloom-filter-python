from BloomFilter import BloomFilter, TrackingHasher

if __name__ == '__main__':
    theHasher = TrackingHasher()
    theBloomFilter = BloomFilter( theHasher )
#    theBloomFilter = BloomFilter()

    [theBloomFilter.addWord( line.strip() ) for line in open('/usr/share/dict/words')]

    theHasher.printTrackingData()

    while True:
        theInput = raw_input( 'Enter a word: ' )

        if theInput == 'q!':
            break

        if ( theBloomFilter.checkWord( theInput ) ):
            print theInput + ' was found!'
        else:
            print theInput + ' was not found...'
            theBloomFilter.printDebuggingData( theInput )
