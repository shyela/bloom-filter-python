from BloomFilter import Hasher, BloomFilter
from bitarray import bitarray
import unittest


class TestBloomFilter(unittest.TestCase):

    def setUp( self ):
        self.myHasherForTest = HasherForTest()
        self.myBloomFilter = BloomFilter( self.myHasherForTest )

    def testHasBitField(self):
        self.assertIsNotNone( self.myBloomFilter.myBitArray, 'bitfield does not exist' )

    def testBitFieldDefaultsToFalse(self):
        self.assertFalse( self.myBloomFilter.myBitArray.any(), 'bitfield should be initialized to all Falses' )

    def testAddWord(self):
        self.myHasherForTest.myTestResults[ 'foo' ] = [ 4, 5 ]
        self.myHasherForTest.myTestResults[ 'bar' ] = [ 2, 7, 5 ]

        self.myBloomFilter.addWord( 'foo' )
        self.myBloomFilter.addWord( 'bar' )

        self.assertThatOnlyIndexesAreTrue( [ 4, 5, 2, 7 ] )

    def assertThatOnlyIndexesAreTrue(self, anIndexes):
        theBitArrayCopy = bitarray( self.myBloomFilter.myBitArray )

        for theIndex in anIndexes:
            self.assertTrue( self.myBloomFilter.myBitArray[theIndex], 'index ' + str( theIndex ) + ' is false when it should be true' )
            theBitArrayCopy[theIndex] = False

        self.assertFalse( theBitArrayCopy.any(), 'an unexpected index(es) were True, they should be false: ' + str( theBitArrayCopy ) )

    def testCheckWord(self):
        self.myHasherForTest.myTestResults[ 'foo' ] = [ 4, 5 ]
        self.myHasherForTest.myTestResults[ 'bar' ] = [ 2, 7, 5 ]
        self.myBloomFilter.addWord( 'foo' )

        self.assertTrue( self.myBloomFilter.checkWord( 'foo' ), 'word foo should be in the filter' )
        self.assertFalse( self.myBloomFilter.checkWord( 'bar' ), 'word bar should NOT be in the filter' )

    def testCheckWordWithRealHasher(self):
        theBloomFilter = BloomFilter()

        self.validateAddingWord( theBloomFilter, "foo" );
        self.validateAddingWord( theBloomFilter, "bar" );
        self.validateAddingWord( theBloomFilter, "barf" );
        self.validateAddingWord( theBloomFilter, "barge" );
        self.validateAddingWord( theBloomFilter, "barn" );
        self.validateAddingWord( theBloomFilter, "bart" );
        self.validateAddingWord( theBloomFilter, "fnarfle-pants" );
        self.validateAddingWord( theBloomFilter, "BLARG" );
        self.validateAddingWord( theBloomFilter, "blarg" );
        self.validateAddingWord( theBloomFilter, "a" );
        self.validateAddingWord( theBloomFilter, "aardvark" );
        self.validateAddingWord( theBloomFilter, "platypus" );
        self.validateAddingWord( theBloomFilter, "melee" );
        self.validateAddingWord( theBloomFilter, "somethingreallylong" );
        self.validateAddingWord( theBloomFilter, "carrot" );
        self.validateAddingWord( theBloomFilter, "derpa derpa der" );
        self.validateAddingWord( theBloomFilter, "b" );
        self.validateAddingWord( theBloomFilter, "#winning" );

        self.assertFalse( theBloomFilter.checkWord( "bat" ));
        self.assertFalse( theBloomFilter.checkWord( "mele" ));
        self.assertFalse( theBloomFilter.checkWord( "blah" ));

    def validateAddingWord(self, aBloomFilter, aWordToTest):
        self.assertFalse( aBloomFilter.checkWord( aWordToTest ) );
        aBloomFilter.addWord( aWordToTest );
        self.assertTrue( aBloomFilter.checkWord( aWordToTest ) );


class HasherForTest(Hasher):

    def __init__(self):
        super(HasherForTest, self).__init__()
        self.myTestResults = {}

    def getBitArraySize(self):
        return 10

    def getIndexesForWord(self, aWord, aGoingToAddWordFlag = False):
        if aWord in self.myTestResults:
            return self.myTestResults[aWord]
        else:
            return super(HasherForTest, self).getIndexesForWord( aWord )


if __name__ == '__main__':
    unittest.main()
