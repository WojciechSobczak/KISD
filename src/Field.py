'''
Created on 21 paź 2017

@author: Lama
'''
from math import floor
from cgitb import small
class SimpleField:
    def __init__(self, base):
        if base < 2:
            raise "Base of field has to be bigger than 2!"
        if self.isPrime(base) == False:
            raise "Base of field has to be prime number!";
        self.base = base;
    
    #Operations
    def add(self, elem1, elem2):
        params = [elem1, elem2];
        val = 0;
        for p in params:
            if p < 0:
                p = self.addInv(p);
            val += p;
        return val % self.base;
    def sub(self, elem1, elem2):
        return self.add(elem1, self.addInv(elem2));
    def addInv(self, num):
        if num < 0:
            return self.base + num;
        else:
            return self.base - num;
       
    def pow(self, base, power):
        if power == 0:
            return 1;
        result = base;
        for i in range(1, power):
            result = (result * power) % self.base;
        return result;
    def mul(self, num1, num2):
        return (num1*num2) % self.base;
    def div(self, num1, num2):
        return self.mul(num1, self.fastMulInverse(num2));
    
    
    #Utilities
    def findGenerators(self):
        outputList = [];
        for currentBase in range(2, self.base):
            #a^p-1 musi być 1
            if (self.pow(currentBase, self.base - 1) != 1):
                continue;
            generatedNumbers = set([currentBase]);
            for power in range(2, self.base):
                value = self.pow(currentBase, power);
                #jeżeli mod 1 lub -1, to sprawdzamy czy jesteśmy przed połową przedziału
                if (value == 1 and power <= self.base / 2):
                    break;
                else:
                    generatedNumbers.add(value);
                    
            if (len(generatedNumbers) == self.base - 1):
                outputList.append(currentBase);
        return outputList;
    def isPrime(self, number):
        number = abs(number);
        if number == 1:
            return False;
        if number % 2 == 0:
            return number == 2;
        for i in range(2, number):
            if number % i == 0:
                return False;
        return True;
    def naiveMulInverse(self, num):
        if num <= 0 or num > self.base or self.fastGcd(num, self.base) != 1:
            raise "Number has not inversed element"
        for i in range(2, self.base):
            if self.mul(num, i) == 1:
                return i;
    def gcd(self, num1, num2):
        while (num1 != num2):
            if (num1 > num2):
                num1 -= num2;
            else:
                num2 -= num1;
        return num1;
    def fastGcd(self, num1, num2):
        while num1 != num2:
            result = max(num1, num2);
            num2 = min(num1, num2);
            num1 = result;
            result = num1 - floor(num1/num2)*num2;
            if (result == 0):
                return num2;
            num1 = result;
        return 1;

    #Based on Bézout coefficients taken from Extended Euclidean Algorithm
    def fastMulInverse(self, num):
        if num < 0:
            num = self.addInv(num);
        if num == 0 or num > self.base or self.fastGcd(num, self.base) != 1:
            raise "Number has not inversed element"
        a = num;
        b = self.base;
        r = [a, b];
        s = [1, 0];
        t = [0, 1];
        q = []
        index = 2;
        while r[index - 1] != 0:
            q.append(floor(a / b));
            r.append(a % b);
            s.append(s[index - 2] - q[index - 2]*s[index - 1]);
            t.append(t[index - 2] - q[index - 2]*t[index - 1]);
            a = r[index - 1];
            b = r[index];
            index += 1;
        inv = s[index - 2];
        if inv < 0:
            inv += self.base;
        return inv;
         
         
    def checkPolynomials(self, *polies):
        length = len(polies[0]);
        for poly in polies:
            if type(poly) is not list:
                raise "Only vectors of factors are supported";
            if len(poly) != length:
                raise "Vectors have to have the same length";
            
    def polyToString(self, poly):
        output = "";
        for i in range(len(poly) - 1, -1, -1):
            if (poly[i] != 0):
                factor = poly[i];
                power = i;
                factorString = str(factor);
                powerString = "x^" + str(power);
                if (factor == 1):
                    factorString = "";
                if (power == 1):
                    powerString = "x";
                if (power == 0):
                    powerString = "";
                    if (factor == 1):
                        factorString = "1";
                if len(output) == 0:
                    output = factorString + powerString;
                else:
                    output = output + " + " + factorString + powerString;
        return output;
    
    def getBiggerAndSmallerPoly(self, poly1, poly2):
        #Kopiowianie zmiennych
        biggerPoly = [];
        smallerPoly = [];
        if len(poly1) > len(poly2):
            biggerPoly = list(poly1);
            smallerPoly = list(poly2);
        else:
            biggerPoly = list(poly2);
            smallerPoly = list(poly1);
        return [biggerPoly, smallerPoly];    
        
        
    def addPolynomials(self, poly1, poly2):
        bigSmall = self.getBiggerAndSmallerPoly(poly1, poly2);
        for i in range(0, len(bigSmall[1])):
            bigSmall[0][i] = self.add(bigSmall[0][i], bigSmall[1][i]);
        return bigSmall[0];
    
    def subPolynomials(self, poly1, poly2):
        bigSmall = self.getBiggerAndSmallerPoly(poly1, poly2);
        for i in range(0, len(bigSmall[1])):
            bigSmall[0][i] = self.sub(poly1[i], poly2[i]);
        return bigSmall[0];
    
    def mulPolynomials(self, poly1, poly2):
        maxPower1 = 0;
        maxPower2 = 0;
        for i in range(0, len(poly1)):
            if (poly1[i] != 0):
                if i > maxPower1:
                    maxPower1 = i;
        for i in range(0, len(poly2)):
            if (poly2[i] != 0):
                if i > maxPower2:
                    maxPower2 = i;
        
        maxPower = maxPower1 + maxPower2;
        
        result = self.getArray(maxPower + 1);
        for i in range(len(poly1) - 1, -1, -1):
            for j in range(len(poly2) - 1, -1, -1):
                factor = self.mul(poly1[i], poly2[j]);
                if factor > 0:
                    power = i + j;
                    result[power] = self.add(result[power], factor);
        return result;

    def invPolymonial(self, poly):
        result = [];
        if self.base == 2:
            for i in range(len(poly) - 1, -1, -1):
                result.append(poly[i]);
        return result;
    
    def polyToNumber(self, poly):
        val = 0;
        for i in range(0, len(poly)):
            val = val + 2**poly[len(poly) - 1 - i];
        return val;
    
    def isZero(self, poly):
        for i in range(0, poly):
            if poly[i] != 0:
                return False;
        return True;
    
    def getArray(self, size):
        result = [];
        for i in range(0, size):
            result.append(0);
        return result;
    
    def getBiggestPower(self, poly):
        for i in range(len(poly) - 1, -1, -1):
            if (poly[i] != 0):
                return i;
        return -1;
    
    def divPolynomials(self, dividend, divisor):
        #Znalezienie najwyższej potęgi dzielnej
        biggestDividendPower = 0;
        for i in range(len(dividend) - 1, -1, -1):
            if (dividend[i] != 0):
                biggestDividendPower = i;
                break;
                
        #Znalezienie najwyższej potęgi dzielnika
        biggestDivisorPower = 0;
        for i in range(len(divisor) - 1, -1, -1):
            if (divisor[i] != 0):
                biggestDivisorPower = i;
                break;
        
        if biggestDividendPower < biggestDivisorPower:
            raise "Polynomials are indivisible";
        
        maxPower = max(biggestDividendPower, biggestDivisorPower);
        result = [self.getArray(maxPower), self.getArray(maxPower)];
        remainder = result[1];
        newDividend = dividend;
        while True:
            i = len(newDividend) - 1;
            while (newDividend[i] == 0 and i > 0):
                i = i - 1;
            if i < 0:
                return result;
            #dzielenie przez najwyższą potęgę dzielnej
            actualPower = i - biggestDivisorPower;
            #jeżeli mniejsza niż zero, to już nie podzielimy, więc koniec dzielenia
            if actualPower < 0:
                if i == 0:
                    return [dividend, remainder];
                else:
                    return result;
            #Dzielimy aktualny największy wyraz dzielnej przez największy wyraz dzielnika
            divResult = self.getArray(actualPower + 1);
            divResult[actualPower] = self.div(newDividend[i], divisor[biggestDivisorPower]);
            #Dodajemy wynik tego dzielenia do wyniku
            result[0] = self.addPolynomials(result[0], divResult);
            #Mnożenie dzielnika przez wynik dzielenia
            subtrahend = self.mulPolynomials(divisor, divResult);
            #Odejmowanie wymnożonej wartości od aktualnej dzielnej
            newDividend = self.subPolynomials(newDividend, subtrahend);
            #Jeżeli można dzielić dalej, to dzielimy, jeżeli nie to koniec dzielenia i zwracamy wynik
            if self.getBiggestPower(newDividend) < biggestDivisorPower:
                result[1] = newDividend;
                return result;
            
    def searchForPrimals(self, ):
    
f = SimpleField(29);
#f.printPolynomial([1, 0, 1]);
#f.printPolynomial(f.addPolynomials([1, 0, 1], [1, 1, 1]));
#f.printPolynomial(f.subPolynomials([1, 0, 1], [1, 1, 1]));
divident = [1, 1, 1, 0, 1];
divisor = [1, 0, 1, 1];
result = f.divPolynomials(divident, divisor);
print(f.polyToString(result[0]));
print(f.polyToString(result[1]));
#f.printPolynomial();
#f.printPolynomial(f.mulPolynomials([1, 1, 1], f.invPolymonial([1, 1, 1])));
#f.printPolynomial(f.invPolymonial([1, 1, 0]))




