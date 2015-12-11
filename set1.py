import binascii
import itertools

def myHexToBase64( string ):
  table = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/="
  out = ""
  offset = 0
  value = 0
  for i in xrange( 0, len(string) ):
    value <<= 4
    value |= int(string[i], 16)
    offset += 4
    if offset >= 6:
      offset -= 6
      index = ( value >> offset )
      out += table[ index ]
      value = value & ( (2 ** offset  ) - 1 )

  if offset > 0:
    out += table[ value ]

  return out


def hexToBase64( string ):
  return binascii.b2a_base64( binascii.unhexlify(string) )

def fixedXOR( string1, string2 ):
  return hex( int(string1,16)^int(string2,16) )

def getFrequencyDiff(string):
  freqTable = { 
               'E':	12.02, 'T':	9.10, 'A':	8.12, 'O':	7.68, 'I':	7.31, 	'N':	6.95, 	'S': 6.28, 'R':	6.02, 'H':	5.92, 	'D':	4.32, 	'L':	3.98, 	'U':	2.88, 'C':	2.71, 	'M':	2.61, 	'F':	2.30, 	'Y':	2.11, 'W':	2.09, 	'G':	2.03, 	'P':	1.82, 	'B':	1.49, 'V':	1.11, 	'K':	0.69, 	'X':	0.17, 	'Q':	0.11, 'J':	0.10, 'Z': 0.07, ' ': 20.0
							 }
  diff = 0
  for f in freqTable:
    x = 100 * (float(string.count(f)) / len(string))
    diff += abs( x - freqTable[f] )

  return diff

def byteXOREncrypt( string, key ):
  result = ""
  for j in xrange( 0, len(string), 2 ):
    #print string[j:j+2], int(string[j:j+2],16)
    #print int(string[j:j+2],16)^i
    result += chr(int(string[j:j+2],16)^key  )

  return result

def byteXOREncryptHex( string, key ):
  result = ""
  for j in xrange( 0, len(string), 2 ):
    #print string[j:j+2], int(string[j:j+2],16)
    #print int(string[j:j+2],16)^i
    result += hex(int(string[j:j+2],16)^key)[2:].ljust(2,'0')

  return result

def byteXOREncrypt2( string, key ):
  result = ""
  for j in xrange( 0, len(string) ):
    #print string[j:j+2], int(string[j:j+2],16)
    #print int(string[j:j+2],16)^i
    result += chr(ord(string[j:j+1])^key)

  return result

def decodeByteXOR(string):
  bestDiff = 99999
  bestDiffString = 0

  for i in xrange( 0, 2**8 ):
    #print "i=",i
    hexDecodedString = byteXOREncrypt( string, i )
    #print hexDecodedString
    #decodedString = binascii.unhexlify( hexDecodedString[2:-1] )
    #print decodedString
    diff = getFrequencyDiff( hexDecodedString.upper() )
    if diff < bestDiff:
      bestDiff = diff
      bestDiffString = hexDecodedString

  #print bestDiffString
  return ( bestDiff, bestDiffString )
      
def findBestXOREncodedString( strings ):
  best = ( ( 99999, "" ), "" )
  for string in strings:
    string = string.strip()
    decoded = decodeByteXOR(string)
    if ( best[0][0] > decoded[0] ):
      best = ( decoded, string )

  return best

def hexEncode( string ):
  return "".join( [hex(ord(x))[2:].rjust(2, '0') for x in string] )

def hexEncodeBA( ba ):
  return "".join( [hex(x)[2:].rjust(2, '0') for x in ba] )

def hexDecode( string ):
  result = ""
  for j in xrange( 0, len(string), 2 ):
    result += chr(int(string[j:j+2],16))
  return result

def encryptRepeatingKeyXOR3( string, key ):
  ba = bytearray( string )
  kba = bytearray(key)
  for i in xrange( 0, len(ba), len(kba) ):
    for j in xrange( 0, len(kba) ):
      index = i+j
      if ( index < len(ba) ):
        ba[index] ^= kba[j]
  return ba
