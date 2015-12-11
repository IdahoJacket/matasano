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

def decode(string):
  bestDiff = 99999
  bestDiffString = 0

  for i in xrange( 0, 2**8 ):
    #print "i=",i
    hexDecodedString = ""
    for j in xrange( 0, len(string), 2 ):
      #print string[j:j+2], int(string[j:j+2],16)
      #print int(string[j:j+2],16)^i
      hexDecodedString += chr(int(string[j:j+2],16)^i  )
    #print hexDecodedString
    #decodedString = binascii.unhexlify( hexDecodedString[2:-1] )
    #print decodedString
    diff = getFrequencyDiff( hexDecodedString.upper() )
    if diff < bestDiff:
      bestDiff = diff
      bestDiffString = hexDecodedString

  print bestDiffString
  return bestDiffString
      
