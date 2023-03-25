import random
import math

## implementation of the rabin karp algorithm
class RabinKarp:
    def __init__(self):
        self.pat = ""         # the pattern
        self.patHash = 0      # pattern hash value
        self.patlen = 0       # pattern length
        self.randomprime = 0  # a large prime, small enough to avoid long overflow
        self.ibase = 0
        self.RM = 0
        self.timeCount = 0
        
    # Compute hash for key[0..M-1] ie pattern.
    def hash(self, key, M):
        h = 0
        for j in range(M):
            h = (self.ibase * h + ord(key[j])) % self.randomprime
            self.timeCount += 1
        return h
    
    # does pat[] match txt[i..i-M+1] ?
    def check(self, txt, pattern, i):
        p = pattern
        for j in range(self.patlen):
            self.timeCount += 1
            if p[j] != txt[i+j]:
                return False
        return True
    
    # check for exact match
    def search(self, pat, txt):
        pattern = pat  # save pattern
        numberOfMatches = 0
        self.ibase = 256
        self.patlen = len(pattern)
        self.randomprime = self.longRandomPrime()
        
        # precompute R^(M-1) % Q for use in removing leading digit
        self.RM = 1
        for i in range(1, self.patlen):
            self.RM = (self.ibase * self.RM) % self.randomprime
            self.timeCount += 1
        
        self.patHash = self.hash(pattern, self.patlen)
        N = len(txt)
        
        txtHash = self.hash(txt, self.patlen)
        
        # check for match at offset 0
        if self.patHash == txtHash and self.check(txt, pattern, 0):
            numberOfMatches += 1
        
        # check for hash match; if hash match, check for exact match
        for i in range(self.patlen, N):
            self.timeCount += 1
            # Remove leading digit
            txtHash = (txtHash + self.randomprime - self.RM * ord(txt[i-self.patlen]) % self.randomprime) % self.randomprime
            # add trailing digit
            txtHash = (txtHash * self.ibase + ord(txt[i])) % self.randomprime
            
            # check for match
            offset = i - self.patlen + 1
            if self.patHash == txtHash and self.check(txt, pattern, offset):
                numberOfMatches += 1
        
        return numberOfMatches
    
    # a random 31-bit prime
    def longRandomPrime(self):
        prime = random.getrandbits(31)
        while not self.isPrime(prime):
            prime = random.getrandbits(31)
        return prime
    
    def isPrime(self, n):
        if n <= 1:
            return False
        if n <= 3:
            return True
        if n % 2 == 0 or n % 3 == 0:
            return False
        for i in range(5, int(math.sqrt(n))+1, 6):
            if n % i == 0 or n % (i+2) == 0:
                return False
        return True
    
    def getTimeCount(self):
        return self.timeCount

