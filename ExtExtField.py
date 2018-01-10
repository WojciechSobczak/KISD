'''
Created on 21 paź 2017

@author: Lama
'''
import copy;
import Field;

class ExtExtField(Field.Field):
    def __init__(self, base, power):
        super().__init__(base);
        self.power = power;
        self.generator = self.searchForPrimalPoly(self.power);
        self.elements = self.extFieldElements(self.power);
        self.elemToPower = dict();
        for i in range(1, len(self.elements)):
            self.elemToPower[self.hash(self.elements[i])] = i - 1;
        #self.zechs = self.generateZechs();
        
    def generateZechs(self):
        mod = self.base**self.power - 1;
        zechs = self.getArray(self.base**self.power - 2); #0 i n^m-1 odrzucamy
        genCopy = copy.copy(self.generator);
        biggestPower = self.getBiggestPower(genCopy);
        genCopy[biggestPower] = 0;

        zechs[biggestPower - 1] = self.getBiggestPower(genCopy);
        
        nonZeroElements = 1;
        nextIndex = biggestPower*2 % mod;
        prevIndex = biggestPower;
        lastNonZero = nonZeroElements;
        emptyLoops = 0;
        try:
            while nonZeroElements != len(zechs):
                if (lastNonZero == nonZeroElements):
                    emptyLoops = emptyLoops + 1;
                else:
                    emptyLoops = 0;
                lastNonZero = nonZeroElements;
                if (emptyLoops > 5):
                    for i in range(0, len(zechs)):
                        if (zechs[i] == 0):
                            zechs[i] = i + 1;
                            nonZeroElements = nonZeroElements + 1;
                    if (nonZeroElements == len(zechs)):
                        raise StopIteration;
                for i in range(0, len(zechs)):
                    if (zechs[i] != 0 and zechs[zechs[i] - 1] == 0):
                        zechs[zechs[i] - 1] = i + 1;
                        nonZeroElements = nonZeroElements + 1;
                        if (nonZeroElements == len(zechs)):
                            raise StopIteration;
                
                while (zechs[nextIndex - 1] == 0):
                    zechs[nextIndex - 1] = zechs[prevIndex - 1]*self.base % mod;
                    nonZeroElements = nonZeroElements + 1;
                    if (nonZeroElements == len(zechs)):
                        raise StopIteration;
                    prevIndex = nextIndex;
                    nextIndex = nextIndex*self.base % mod;
                nextIndex = 0;
                try:
                    while True:
                        actualZechs = zechs[nextIndex];
                        revZechs = zechs[mod - (nextIndex + 2)];
                        if (actualZechs != 0 and revZechs == 0):
                            break;
                        nextIndex = nextIndex + 1;
                    minusX = mod - (nextIndex + 2);
                    zechs[minusX] = zechs[nextIndex] - (nextIndex + 1);
                    nonZeroElements = nonZeroElements + 1;
                    if (zechs[minusX] < 0):
                        zechs[minusX] = zechs[minusX] + mod;
                    if (nonZeroElements == len(zechs)):
                        raise StopIteration;
                    prevIndex = (minusX+1);
                    nextIndex = (minusX+1)*self.base % mod;
                except:
                    nextIndex = 0;
                    pass;
        except StopIteration:
            pass;
        
        zechsCheck = set();
        for i in range(0, len(zechs)):
            zechsCheck.add(zechs[i]);
        if (len(zechs) != len(zechsCheck)):
            raise "Bad zechs table!!!";
        return zechs;
        
    def hash(self, vec):
        output = "";
        for i in range(0, len(vec)):
            output = output + str(vec[i]);
        return output;
    
    def getElemToPower(self, elem):
        return self.elemToPower[self.hash(elem)];
        
    def addExt(self, elem1, elem2):
        return self.addPolynomials(elem1, elem2);
    
    def mulExt(self, elem1, elem2):
        if (self.isZero(elem1) or self.isZero(elem2)):
            return [0];
        alpha1 = self.getElemToPower(elem1);
        alpha2 = self.getElemToPower(elem2);
        return self.elements[((alpha1 + alpha2) + 1) % self.base**self.power]; 
    
    def subExt(self, elem1, elem2):
        return self.addExt(elem1, self.getExtInv(elem2));
    
    def divExt(self, elem1, elem2):
        if (self.isZero(elem1) or self.isZero(elem2)):
            return [0];
        alpha1 = self.getElemToPower(elem1);
        alpha2 = self.getElemToPower(elem2);
        alpha = (alpha1 - alpha2);
        if (alpha < 0):
            alpha = alpha + (self.base**self.power - 2);
        return self.elements[(alpha + 1) % self.base**self.power];
    
    def getExtInv(self, elem):
        for i in range(0, len(elem)):
            elem[i] = self.getInv(elem[i]);
            
    def getExtPolynomialInv(self, elem):
        for i in range(0, len(elem)):
            for j in range(0, len(elem[i])):
                elem[i][j] = self.getInv(elem[i][j]);
            
         
    def addExtPolynomials(self, poly1, poly2):
        bigSmall = self.getBiggerAndSmallerPoly(poly1, poly2);
        for i in range(0, len(bigSmall[1])):
            bigSmall[0][i] = self.addPolynomials(bigSmall[0][i], bigSmall[1][i]);
        return bigSmall[0];
    
    def getExtArray(self, length):
        output = [];
        for i in range(0, length):
            output.append([0]);
        return output;
    
    def subExtPolynomials(self, elem1, elem2):
        return self.addExtPolynomials(elem1, elem2);
            
    
    def mulExtPolynomials(self, poly1, poly2):
        maxPower1 = 0;
        maxPower2 = 0;
        for i in range(0, len(poly1)):
            if (self.isZero(poly1[i]) == False):
                if i > maxPower1:
                    maxPower1 = i;
        for i in range(0, len(poly2)):
            if (self.isZero(poly2[i]) == False):
                if i > maxPower2:
                    maxPower2 = i;
        
        maxPower = maxPower1 + maxPower2;
        
        result = [];
        for i in range(0, maxPower+2):
            result.append([0]);
        for i in range(len(poly1) - 1, -1, -1):
            for j in range(len(poly2) - 1, -1, -1):
                factor = self.mulExt(poly1[i], poly2[j]);
                power = i + j;
                result[power] = self.addExt(result[power], factor);
        return result;
    
    def getExtBiggestPower(self, poly):
        for i in range(len(poly) - 1, -1, -1):
            if (self.isZero(poly[i]) == False):
                return i;
        return 0;
    
    def reduceExtPolynomialsZeros(self, inpoly):
        poly = copy.copy(inpoly);
        toRem = 0;
        for i in range(len(poly) - 1, -1, -1):
            if (self.isZero(poly[i]) == True):
                toRem = toRem + 1;
            else:
                break;
        if (toRem == len(poly)):
            return [[0]];
        else:
            for i in range(0, toRem):
                del poly[len(poly) - 1];
        return poly;
        
    def divExtPolynomials(self, dividend, divisor):
        #Znalezienie najwyższej potęgi dzielnej
        biggestDividendPower = 0;
        for i in range(len(dividend) - 1, -1, -1):
            if (self.isZero(dividend[i]) == False):
                biggestDividendPower = i;
                break;
                
        #Znalezienie najwyższej potęgi dzielnika
        biggestDivisorPower = 0;
        for i in range(len(divisor) - 1, -1, -1):
            if (self.isZero(divisor[i]) == False):
                biggestDivisorPower = i;
                break;
        
        if biggestDividendPower < biggestDivisorPower or (biggestDividendPower >= 1 and biggestDivisorPower == 0):
            return [[[0]], copy.copy(dividend)];
        
        maxPower = max(biggestDividendPower, biggestDivisorPower);
        result = [self.getExtArray(maxPower), self.getExtArray(maxPower)];
        remainder = result[1];
        newDividend = list(dividend);
        try:
            while True:
                i = len(newDividend) - 1;
                while (self.isZero(newDividend[i]) and i > 0):
                    i = i - 1;
                if i < 0:
                    raise StopIteration;
                #dzielenie przez najwyższą potęgę dzielnej
                actualPower = i - biggestDivisorPower;
                #jeżeli mniejsza niż zero, to już nie podzielimy, więc koniec dzielenia
                if actualPower < 0:
                    if i == 0:
                        result[0] = dividend;
                        result[1] = remainder;
                        raise StopIteration;
                    else:
                        raise StopIteration;
                #Dzielimy aktualny największy wyraz dzielnej przez największy wyraz dzielnika
                divResult = self.getExtArray(actualPower + 1);
                divResult[actualPower] = self.divExt(newDividend[i], divisor[biggestDivisorPower]);
                #Dodajemy wynik tego dzielenia do wyniku
                result[0] = self.addExtPolynomials(result[0], divResult);
                #Mnożenie dzielnika przez wynik dzielenia
                subtrahend = self.mulExtPolynomials(divisor, divResult);
                #Odejmowanie wymnożonej wartości od aktualnej dzielnej
                newDividend = self.subExtPolynomials(newDividend, subtrahend);
                #Jeżeli można dzielić dalej, to dzielimy, jeżeli nie to koniec dzielenia i zwracamy wynik
                if self.getExtBiggestPower(newDividend) < biggestDivisorPower:
                    result[1] = newDividend;
                    raise StopIteration;
        except StopIteration:
            result[0] = self.reduceExtPolynomialsZeros(result[0]);
            result[1] = self.reduceExtPolynomialsZeros(result[1]);
        return result;
    
    
    
