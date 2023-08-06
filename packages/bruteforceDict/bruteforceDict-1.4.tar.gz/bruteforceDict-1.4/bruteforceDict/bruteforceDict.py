from itertools import chain, product
class bruteforceDict:
    def __init__(self, size=0, chars='', fileName=""):
        self.size = size
        self.chars = chars
        self.fileName = fileName
    def bruteforce(self):
        return (''.join(candidate)
            for candidate in chain.from_iterable(product(self.chars, repeat=i)
            for i in range(1, self.size + 1)))

    def toFile(self):
        chars = self.chars
        count = self.size
        fileName = self.fileName
        f = open(fileName, "w")
        l = self.bruteforce()
        for i in list(l):
            f.write(f"{i}\n")
        f.close()
