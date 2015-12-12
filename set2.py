from set1 import *
import binascii

byteMax = 2**8 - 1

# modifies ba
def padBlock(ba,blocksize):
  assert len(ba) <= blocksize
  padNeeded = blocksize - len(ba)
  assert padNeeded <= byteMax
  for i in xrange( 0, padNeeded ):
    ba.append( padNeeded )
  return ba

def pad(ba,blocksize):
  lastBlockStart = ( ( len(ba) - 1 )/ blocksize ) * blocksize
  return ba[:lastBlockStart] + padBlock(ba[lastBlockStart:],blocksize)

def padString(s,blocksize):
  return str(pad(bytearray(s),blocksize))

def xorStrings( s1, s2 ):
  assert len(s1) == len(s2)
  b1 = bytearray(s1)
  b2 = bytearray(s2)
  r = bytearray()
  for i in xrange( 0, len(s1) ):
    r.append( b1[i] ^ b2[i] )
  return str(r)

def encryptAES( pt, key ):
  c = AES.new(key, AES.MODE_ECB)
  return c.encrypt( pt )

def encryptAES_CBC( pt, key, iv ):
  p = iv
  assert len(iv) == 16
  result = ""
  pt = padString(pt,16)
  for block in getECBBlocks(pt):
    x = xorStrings( block, p )
    p = encryptAES(x,key)
    result += p
  return result

def decryptAES_CBC( ct, key, iv ):
  p = iv
  assert len(iv) == 16
  result = ""
  for block in getECBBlocks(ct):
    x = decryptAES( block, key )
    a = xorStrings( x, p )
    p = block
    result += a
  return result

def challenge9():
  s = "YELLOW SUBMARINE"
  p =  padBlock( bytearray(s), 20 )
  assert len(p) == 20
  assert p[16] == 4 and p[17] == 4 and p[18] == 4 and p[19] == 4

def challenge10():
  k = padString("YELLOW SUBMARINE", 16)
  print len(k)
  #s = "TEST TEST 123456aaa"*20
  s = binascii.a2b_base64( open('10.in').read() )
  iv = chr(0)*16
  #e = encryptAES_CBC(s,k,iv)
  d = decryptAES_CBC(s,k,iv)
  print len(s),s
  print len(d),d
