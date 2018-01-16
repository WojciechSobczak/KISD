from ExtExtField import ExtExtField
import copy;
from galois import *;

class ReedSolomon:
    
    
    def __init__(self, bitsPerSymbol, errorsToCorrect):
        
        # n -> długość bloku wysyłanego
        # k -> długość informacji
        # n - k -> długość bloku nadmiarowego
        # m -> długość symbolu -> 8
        # 
        self.n = 2**bitsPerSymbol - 1;
        self.k = self.n - errorsToCorrect * 2;
        self.bitsPerSymbol = bitsPerSymbol;
        self.errorsToCorrect = errorsToCorrect;
        
        #self.field = GF(2**self.bit)
        
        self.extField = ExtExtField(2, bitsPerSymbol);
        self.generator = self.findGenerator();
        self.mod = self.n + 1;
        print("----------------------------------------------------")
        print("RS Coder/Decoder 2**" + str(self.bitsPerSymbol) + ":")
        print(" - n = " + str(self.n));
        print(" - k = " + str(self.k));
        print(" - n - k = " + str(self.n - self.k));
        print(" - t = " + str(self.errorsToCorrect));
        print(" - g = " + str(self.generator));
        print("----------------------------------------------------")
        print();        
            
        
        
    def binToDec(self, binVec):
        output = 0;
        for i in range(0, len(binVec)):
            output = output + binVec[i] * 2**i;
        return output;
    
    def extPolyToDecVec(self, poly):
        output = self.extField.getArray(len(poly));
        for i in range(0, len(poly)):
            if (self.extField.isZero(poly[i])):
                output[i] = 0;
            else:
                output[i] = self.binToDec(poly[i]);
        return output;
    
    def decToPoly(self, dec):
        binVec = "{0:b}".format(dec);
        output = self.extField.getArray(self.bitsPerSymbol);
        lenght = len(output);
        if (lenght > len(binVec)):
            lenght = len(binVec);
        
        for i in range(0, lenght):
            if (binVec[i] == '1'):
                output[i] = 1;
            else:
                output[i] = 0;
        list.reverse(output);
        return output;
        
        
    def findGenerator(self):
        oneVec = self.extField.getArray(self.bitsPerSymbol);
        oneVec[0] = 1;
        
        output = [copy.copy(oneVec)];
        for i in range(0, self.errorsToCorrect * 2):
            nextMin = [self.extField.elements[i + 1], oneVec];
            output = self.extField.mulExtPolynomials(output, nextMin);
        return output;    
            
    def bytesToList(self, _bytes):
        output = [];
        for byte in _bytes:   
            output.append(byte);
        return output;
        
    def code(self, message):
        if (len(message) != self.k):
            raise "Message must have " + str(self.k) + " symbols!";
        for e in message:
            if (e.bit_length() > self.bitsPerSymbol):
                raise "Message element must have " + str(self.bitsPerSymbol) + " bits of length!";
            
        #Logika
        #Mnożenie wielomianu razy x^n-k
        while (len(message) != self.n):
            message.insert(0, 0);
            
        #Zamiana na postać wielomianową
        for i in range(0, len(message)):
            message[i] = self.decToPoly(message[i]);
        
        #Dzielenie przez generator przesuniętego wielomianu
        divResult = self.extField.divExtPolynomials(message, self.generator);
        
        r = divResult[1];
        #Dodanie reszty do wiadomości, koniec kodowania
        message = self.extField.addExtPolynomials(message, r);
        print(self.extPolyToDecVec(message));
        return message;
    
    
    def weightOfExtPoly(self, poly):
        weight = 0;
        for i in range(0, len(poly)):
            if self.extField.isZero(poly[i]) == False:
                weight += 1;
        return weight;
    
    def shiftExtPolyRight(self, poly, times):
        result = self.extField.getExtArray(len(poly));
        times %= len(poly);
        for i in range(len(result)):
            result[i] = poly[(i + times) % len(poly)];
        return result;
    
    def shiftExtPolyLeft(self, poly, times):
        result = self.extField.getExtArray(len(poly));
        times %= len(poly);
        for i in range(len(result)):
            newPosition = i - times;
            if (newPosition < 0):
                newPosition += len(poly);
            result[newPosition] = poly[i];
        return result;
    
    def simpleDecode(self, messagePoly):
        correctedPoly = copy.copy(messagePoly);
        shifts = 0;
        while True:
            divResu = self.extField.divExtPolynomials(correctedPoly, self.generator);
            print(self.extPolyToDecVec(self.extField.addExtPolynomials(self.extField.mulExtPolynomials(divResu[0], self.generator), divResu[1])));
            syndrom = divResu[1];
            weight = self.weightOfExtPoly(syndrom);
            if (self.extField.isZeroExtPolynomial(syndrom)):
                return correctedPoly;
            #jeżeli waga większa niż zdolność to sprawdzamy czy jest szansa na korekcję
            if (weight > self.errorsToCorrect):
                if (shifts == self.k):
                    #nic się nie da zrobić :(
                    raise "Non correctable error!";
                else:
                    shifts += 1;
                    correctedPoly = self.shiftExtPolyLeft(correctedPoly, 1);
            else:
                #da radę skorygować
                correctedPoly = self.extField.addExtPolynomials(correctedPoly, syndrom);
                #przesunięcie w kierunku części korekcyjnej
                correctedPoly = self.shiftExtPolyRight(correctedPoly, shifts);
        
    
    def checkCode(self):
        message = list(reversed([1,  2,  3,  4,  5,  6,  7,  8,  9,  10,  11]));#, 12, 13]));
        code = rs.code(message);
        print("Original: " + str(self.extPolyToDecVec(code)));
        
        for i in range(0, len(code)):
            corruptedCode = copy.copy(code);
            corruptedCode[i] = [0, 0, 0, 0];
            print ("    Uszkodzony: " + str(self.extPolyToDecVec(corruptedCode)));
            try:
                decoded = self.simpleDecode(corruptedCode);
                print ("    Odkodowany: " + str(self.extPolyToDecVec(decoded)));
            except:
                print("    Błąd na pozycji (" + str(i) + ") niekorygowalny.");
                pass;
            print("-------------------------------")
        
       

    

rs = ReedSolomon(4, 2);
rs.checkCode();
