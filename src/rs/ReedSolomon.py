from Field import Field;

class ReedSolomon:
    
    SYMBOL_LENGTH = 8;
    
    def __init__(self, wordLength, errorsToCorrect):
        
        self.n = wordLength + (errorsToCorrect * 2);
        self.k = wordLength;
        
        # n -> długość bloku wysyłanego
        # k -> długość informacji
        # n - k -> długość bloku nadmiarowego
        # m -> długość symbolu -> 8
        # 
        self.errorsToCorrect = errorsToCorrect;
        self.wordLength = wordLength;
        self.field = Field(256);
        self.generator = self.findGenerator();
        
        
    def binToDec(self, binVec):
        output = 0;
        for i in range(0, len(binVec)):
            output = self.field.add(output, binVec[i] * 2**i);
        return output;
        
        
    def findGenerator(self):
        output = [1];
        twoField = Field(2);
        elements = twoField.extFieldElements(8);
        
        for i in range(0, self.errorsToCorrect * 2):
            nextMin = [self.binToDec(elements[i + 1]), 1];
            output = self.field.mulPolynomials(output, nextMin);
        return output;    
            
    def bytesToList(self, _bytes):
        output = [];
        for byte in _bytes:   
            output.append(byte);
        return output;
        
    def code(self, message):
        message = message.encode("ascii");
        if (len(message) > self.wordLength):
            raise "Message lenght is bigger than given code word!"
        message = self.bytesToList(message);
        while (len(message) != self.n):
            message.insert(0, 0);
        
        divResult = self.field.divPolynomials(message, self.generator);
        print(divResult);
       # print(list(reversed(message)))
       # print(list(reversed(self.generator)))
      #  print(self.field.mulPolynomials(self.generator, divResult[0]));
        
        r = divResult[1];
        message = self.field.addPolynomials(message, r);
        print(message);
        return message;
    
    def simpleDecode(self, message):
        return message;
    
    def checkCode(self):
        code = rs.code("AAAAAAAAAAA");
        print(rs.code("AAAAAAAAAAA"));
        res = self.field.divPolynomials(code, self.generator);
        print(res);

    

rs = ReedSolomon(11, 2);
rs.checkCode();
