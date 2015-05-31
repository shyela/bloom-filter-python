from BloomFilter import Hash
import unittest



class TestHasher(unittest.TestCase):

    def setUp( self ):
        self.myHash = Hash('', 0, 0)

    def testGetFormatCode(self):
        self.myHash.myNumberOfBytesToEncode = 2
        self.assertEquals( '>H', self.myHash.getFormatCode(), 'wrong format code returned for 2 bytes' )

        self.myHash.myNumberOfBytesToEncode = 3
        self.assertEquals( '>I', self.myHash.getFormatCode(), 'wrong format code returned for 3 bytes' )

        self.myHash.myNumberOfBytesToEncode = 4
        self.assertEquals( '>I', self.myHash.getFormatCode(), 'wrong format code returned for 4 bytes' )

    def testGetPartFromHashStringFor1Bytes(self):
        self.myHash.myNumberOfBytesToEncode = 1
        theHash = '\xf0\x0f\xf1\x1f'

        self.validateGetPartFromHashString(theHash, 0, '\xf0')
        self.validateGetPartFromHashString(theHash, 1, '\x0f')
        self.validateGetPartFromHashString(theHash, 2, '\xf1')
        self.validateGetPartFromHashString(theHash, 3, '\x1f')

    def testGetPartFromHashStringFor2Bytes(self):
        self.myHash.myNumberOfBytesToEncode = 2
        theHash = '\xf0\x0f\xf1\x1f'

        self.validateGetPartFromHashString(theHash, 0, '\xf0\x0f')
        self.validateGetPartFromHashString(theHash, 1, '\xf1\x1f')

    def testGetPartFromHashStringFor3Bytes(self):
        self.myHash.myNumberOfBytesToEncode = 3
        theHash = '\xf0\x0f\xf1\x1f\x0f\xf1'

        self.validateGetPartFromHashString(theHash, 0, '\x00\xf0\x0f\xf1')
        self.validateGetPartFromHashString(theHash, 1, '\x00\x1f\x0f\xf1')

    def testGetPartFromHashFor4Bytes(self):
        self.myHash.myNumberOfBytesToEncode = 4
        theHash = '\xf1\xf0\x0f\xf1\x1f\x0f\x10\xf1'

        self.validateGetPartFromHashString(theHash, 0, '\xf1\xf0\x0f\xf1')
        self.validateGetPartFromHashString(theHash, 1, '\x1f\x0f\x10\xf1')

    def validateGetPartFromHashString(self, aHashString, aPartIndex, anExpectedPart):
        self.myHash.myHashString = aHashString

        theActualPart = self.myHash.getPartFromHashString(aPartIndex)

        self.assertEquals( anExpectedPart, theActualPart, 'wrong hash part returned for index ' + str(aPartIndex)
                                                                + ', actual = ' + theActualPart.encode('hex')
                                                                + ', expected = ' + anExpectedPart.encode('hex') )

    def testConvertToUnsignedFor2Bytes(self):
        self.validateHashConvertsToNumberWithSpecifiedEncoding( 2, '\x00\x01', 1 )
        self.validateHashConvertsToNumberWithSpecifiedEncoding( 2, '\x00\x0f', 15 )
        self.validateHashConvertsToNumberWithSpecifiedEncoding( 2, '\x00\x10', 16 )
        self.validateHashConvertsToNumberWithSpecifiedEncoding( 2, '\x00\xf0', 240 )
        self.validateHashConvertsToNumberWithSpecifiedEncoding( 2, '\x01\x00', 256 )
        self.validateHashConvertsToNumberWithSpecifiedEncoding( 2, '\x01\x01', 257 )
        self.validateHashConvertsToNumberWithSpecifiedEncoding( 2, '\x0f\x00', 3840 )
        self.validateHashConvertsToNumberWithSpecifiedEncoding( 2, '\x0f\x01', 3841 )
        self.validateHashConvertsToNumberWithSpecifiedEncoding( 2, '\xf0\x00', 61440 )

    def testConvertToUnsignedFor3Bytes(self):
        self.validateHashConvertsToNumberWithSpecifiedEncoding( 3, '\x00\x00\x00\x01', 1 )
        self.validateHashConvertsToNumberWithSpecifiedEncoding( 3, '\x00\x00\x00\x0f', 15 )
        self.validateHashConvertsToNumberWithSpecifiedEncoding( 3, '\x00\x00\x00\x10', 16 )
        self.validateHashConvertsToNumberWithSpecifiedEncoding( 3, '\x00\x00\x00\xf0', 240 )
        self.validateHashConvertsToNumberWithSpecifiedEncoding( 3, '\x00\x00\x01\x00', 256 )
        self.validateHashConvertsToNumberWithSpecifiedEncoding( 3, '\x00\x00\x01\x01', 257 )
        self.validateHashConvertsToNumberWithSpecifiedEncoding( 3, '\x00\x00\x0f\x00', 3840 )
        self.validateHashConvertsToNumberWithSpecifiedEncoding( 3, '\x00\x00\x0f\x01', 3841 )
        self.validateHashConvertsToNumberWithSpecifiedEncoding( 3, '\x00\x01\x00\x00', 65536 )
        self.validateHashConvertsToNumberWithSpecifiedEncoding( 3, '\x00\x0f\x00\x01', 983041 )

        self.validateHashConvertsToNumberWithSpecifiedEncoding( 3, '\x00\xf0\x0f\xf1', 15732721 )
        self.validateHashConvertsToNumberWithSpecifiedEncoding( 3, '\x00\x1f\x0f\xf1', 2035697 )

    def validateHashConvertsToNumberWithSpecifiedEncoding(self, aNumBytesToEncode, aHashString, anExpectedNumber):
        self.myHash.myNumberOfBytesToEncode = aNumBytesToEncode

        theActualNumber = self.myHash.convertHashToUnsignedNumber(aHashString)

        self.assertEqual( anExpectedNumber, theActualNumber, 'the hash ' + aHashString.encode('hex')
                                                                + ' was not properly converted to an unsigned number:'
                                                                + ' actual = ' + str( theActualNumber )
                                                                + ', expected = ' + str( anExpectedNumber ) )

    def testGetIndexes(self):
        self.myHash.myNumberOfIndexesToReturn = 3

        self.validateGetIndexes(2, '\xf0\x0f\xf1\x1f\x0f\xf1', [61455, 61727, 4081])
        self.validateGetIndexes(3, '\xf0\x0f\xf1\x1f\x0f\xf1', [15732721, 2035697])
        self.validateGetIndexes(4, '\xf0\x0f\xf1\x1f', [4027576607])

    def testGetIndexesIgnoresPartials(self):
        self.myHash.myNumberOfIndexesToReturn = 3

        self.validateGetIndexes(2, '\xf0\x0f\xf1\x1f\x0f', [61455, 61727])
        self.validateGetIndexes(3, '\xf0\x0f\xf1\x1f\x0f', [15732721])
        self.validateGetIndexes(4, '\xf0\x0f\xf0\x1f\xf1\x1f\x0f', [4027576351])

    def testGetIndexesReturnsSpecifiedNumberOfIndexes(self):
        self.myHash.myNumberOfIndexesToReturn = 1

        self.validateGetIndexes(2, '\xf0\x0f\xf1\x1f\x0f\xf1', [61455])
        self.validateGetIndexes(3, '\xf0\x0f\xf1\x1f\x0f\xf1', [15732721])
        self.validateGetIndexes(4, '\xf0\x0f\xf1\x1f\xf0\x0f\xf1\x1e', [4027576607])

    def validateGetIndexes(self, aNumBytesToEncode, aHashString, anExpectedResult):
        self.myHash.myNumberOfBytesToEncode = aNumBytesToEncode
        self.myHash.myHashString = aHashString

        theResults = self.myHash.getIndexes()

        self.assertListEqual(anExpectedResult, theResults, 'the wrong indexes were returned for hash = ' + aHashString.encode('hex')
                                                             + ', # bytes to encode = ' + str( aNumBytesToEncode )
                                                             + ', actual = ' + str(theResults)
                                                             + ', expected = ' + str(anExpectedResult))

if __name__ == '__main__':
    unittest.main()
