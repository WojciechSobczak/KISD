from ExtExtField import ExtExtField
import copy;

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
        self.extField = ExtExtField(2, bitsPerSymbol);
        self.generator = self.findGenerator();
            
        
        
    def binToDec(self, binVec):
        output = 0;
        for i in range(0, len(binVec)):
            output = output + binVec[i] * 2**i;
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
        print(divResult);
       # print(list(reversed(message)))
       # print(list(reversed(self.generator)))
      #  print(self.extField.mulPolynomials(self.generator, divResult[0]));
        
        r = divResult[1];
        #Dodanie reszty do wiadomości, koniec kodowania
        message = self.extField.addPolynomials(message, r);
        print(message);
        return message;
    
    def simpleDecode(self, message):
        return message;
    
    def checkCode(self):
        code = rs.code(list(reversed([1,  2,  3,  4,  5,  6,  7,  8,  9,  10,  11])));
        res = self.extField.divExtPolynomials(code, self.generator);
        print(res);

    

rs = ReedSolomon(4, 2);
rs.checkCode();
