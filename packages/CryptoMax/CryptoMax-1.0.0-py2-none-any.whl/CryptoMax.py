import math
import numpy as np
from sympy import Matrix
from Crypto.Cipher import DES
from Crypto.Cipher import AES
from Crypto.Hash import SHA1
from Crypto.Hash import SHA256
from Crypto.PublicKey import ECC
from Crypto.Signature import DSS


class Cryptomax:
    class DSS:
        def __init__(self):
            self.signature = None
            key = ECC.generate(curve='P-256')
            f = open('privkey.pem', 'w')
            f.write(key.export_key(format='PEM'))
            f.close()
            f = open('pubkey.pem', 'w')
            f.write(key.public_key().export_key(format='PEM'))
            f.close()

        def sign(self, message):
            key = ECC.import_key(open('privkey.pem').read())
            hash = SHA256.new(message)
            signer = DSS.new(key, 'fips-186-3')
            self.signature = signer.sign(hash)

        def check(self, message):
            key = ECC.import_key(open('pubkey.pem').read())
            h = SHA256.new(message)
            verifier = DSS.new(key, 'fips-186-3')
            try:
                verifier.verify(h, self.signature)
                print("The message is authentic.")
            except ValueError:
                print("The message is not authentic.")

    class SHA:
        def __init__(self, file1Path, file2Path):
            self.h1 = SHA1.new()
            self.h2 = SHA1.new()
            self.file1Contents = open(file1Path, 'r').read()
            print('\t\t\t--- FILE 1 CONTENTS ---\n{}\n'.format(self.file1Contents))
            self.file2Contents = open(file2Path, 'r').read()
            print('\t\t\t--- FILE 2 CONTENTS ---\n{}\n'.format(self.file2Contents))
            self.h1.update(self.file1Contents.encode('utf-8'))
            self.h2.update(self.file2Contents.encode('utf-8'))
            if self.h1.hexdigest() == self.h2.hexdigest():
                print("The files match")
            else:
                print("The files do not match")

    class DiffieHellman:
        def __init__(self, prime, otherGenerator, othersecretKey, selfSecretKey):
            self.prime = prime
            self.generator = otherGenerator
            self.secretKey = othersecretKey
            self.otherUserKey = otherGenerator ** othersecretKey % prime
            self.selfSecretKey = selfSecretKey

        def commonKey(self):
            return self.otherUserKey ** self.selfSecretKey % self.prime

    class RSA:
        def __init__(self, path):
            with open(path, 'w') as f:
                f.write('''
                <html>
   <head>
      <title>RSA Encryption</title>
      <meta name="viewport" content="width=device-width, initial-scale=1.0">
   </head>
   <body>
      <center>
         <h1>RSA Algorithm</h1>

         <hr>
         <table>
            <tr>
               <td>Enter First Prime Number:</td>
               <td><input type="number" value="29" id="p"></td>
            </tr>
            <tr>
               <td>Enter Second Prime Number:</td>
               <td><input type="number" value="31" id="q"></p></td>
            </tr>
	   <tr>
               <td>Enter Public Key:</td>
               <td><input type="number" value="3" id="publickey"></p></td>
            </tr>
            <tr>
               <td>Enter the Text</td>
               <td><input type="number" value="89" id="msg"></p></td>
            </tr>
            <tr>
               <td>Composite Number:</td>
               <td>
                  <p id="composite"></p>
               </td>
            </tr>

            <tr>
               <td>Private Key:</td>
               <td>
                  <p id="privatekey"></p>
               </td>
            </tr>
            <tr>
               <td><button onclick="RSA(1);">Encrypt</button></td>
               <td>
                  <p id="ciphertext"></p>
               </td>
            </tr>
            <tr>
               <td><button onclick="RSA(2);">Decrypt</button></td>
               <td>
                  <p id="plaintext"></p>
               </td>
            </tr>
         </table>
      </center>
   </body>
   <script type="text/javascript">
      function RSA(choice) {
      var gcd, p, q, msg, n, t, e,d,i;
      gcd = function (a, b) { return (b!=0) ? gcd(b, a % b) :a ; };
      p = document.getElementById('p').value;
      q = document.getElementById('q').value;
      msg = document.getElementById('msg').value;
      e = document.getElementById('publickey').value;
      n = p * q;
      t = (p - 1) * (q - 1);

      for (d = 2; d < t; d++) {
      if ( (e*d)%t == 1) {
      break;
      }
      }


      var ct=msg;
      for(i=2;i<=e;i++)
      ct=(ct*msg)%n;

      var pt=msg;
      for(i=2;i<=d;i++)
      pt=(pt*msg)%n;

      document.getElementById('composite').innerHTML = n;
      document.getElementById('privatekey').innerHTML = d;
      if(choice==1)
      document.getElementById('ciphertext').innerHTML = ct;
      else
      document.getElementById('plaintext').innerHTML = pt;
      }
   </script>
</html>
                ''')

    class AES:
        @staticmethod
        def Encrypt(plainText, key):
            cipher = AES.new(key, AES.MODE_CBC)
            return cipher.encrypt(plainText), cipher.iv

        @staticmethod
        def Decrypt(cipherText, key, iv):
            cipher_decrypt = AES.new(key, AES.MODE_CBC, iv=iv)
            return cipher_decrypt.decrypt(cipherText)

    class DES:
        @staticmethod
        def pad(text):
            n = len(text) % 8
            return text + (b' ' * n)

        @staticmethod
        def Encrypt(plainText, key):
            plainText = Cryptomax.DES.pad(plainText)
            cipher = DES.new(key, DES.MODE_CBC)
            return cipher.encrypt(plainText), cipher.iv

        @staticmethod
        def Decrypt(cipherText, key, iv):
            cipher_decrypt = DES.new(key, DES.MODE_CBC, iv=iv)
            return cipher_decrypt.decrypt(cipherText)

    class ColumnarTransposition:
        @staticmethod
        def Encrypt(plainText, key):
            n = len(plainText)
            col = len(key)
            plainText += 'x' * ((-(n % col)) % col)
            n = len(plainText)
            row = (n // col)
            cmat = [['' for j in range(col)] for i in range(row)]
            k = 0
            for i in range(row):
                for j in range(col):
                    cmat[i][j] = plainText[k]
                    k += 1
            sort_key = sorted(list(key))
            ctext = ""
            for i in range(col):
                curr_col = key.find(sort_key[i])
                ctext += ''.join([cmat[i][curr_col] for i in range(row)])
            return ctext

        @staticmethod
        def Decrypt(cipherText, key):
            n = len(cipherText)
            col = len(key)
            row = (n // col)

            cmat = [['' for j in range(col)] for i in range(row)]
            k = 0
            sort_key = sorted(list(key))
            for i in range(col):
                curr_col = key.find(sort_key[i])
                for j in range(row):
                    cmat[j][curr_col] = cipherText[k]
                    k += 1
            ptext = ""
            for i in range(row):
                for j in range(col):
                    ptext += cmat[i][j]
            return ptext

    class RailFence:
        @staticmethod
        def Encrypt(plainText, depth):
            n = len(plainText)
            row = depth
            plainText += 'x' * ((-(n % row)) % row)
            n = len(plainText)
            col = (n // row)
            cmat = [['' for j in range(col)] for i in range(row)]
            k = 0
            for i in range(col):
                for j in range(row):
                    cmat[j][i] = plainText[k]
                    k += 1
            ctext = ""
            for i in range(row):
                for j in range(col):
                    ctext += cmat[i][j]
            return ctext

        @staticmethod
        def Decrypt(text, depth):
            n = len(text)
            row = depth
            col = (n // row)

            cmat = [['' for j in range(col)] for i in range(row)]
            k = 0
            for i in range(row):
                for j in range(col):
                    cmat[i][j] = text[k]
                    k += 1
            ptext = ""
            for i in range(col):
                for j in range(row):
                    ptext += cmat[j][i]
            return ptext

    class HillCipher:

        aton = lambda x: ord(x) - 97

        @staticmethod
        def normalize(text, bl):
            text += "x" * ((-(len(text) % bl)) % bl)
            return text

        @staticmethod
        def Encrypt(plainText, key):
            bl = int(math.sqrt(len(key)))
            text = Cryptomax.HillCipher.normalize(plainText, bl)
            key = np.array(list(map(Cryptomax.HillCipher.aton, list(key)))).reshape(bl, bl)
            ct = ""
            for i in range(0, len(text) // bl, bl):
                l = list(map(Cryptomax.HillCipher.aton, text[i:i + bl:1]))
                l = np.array(l).reshape(bl, 1)
                l = np.dot(key, l)
                l = l % 26
                for j in range(bl):
                    ct += chr(l[j][0] + 97)
            return ct

        @staticmethod
        def Decrypt(cipherText, key):
            bl = int(math.sqrt(len(key)))
            key = np.array(list(map(Cryptomax.HillCipher.aton, list(key)))).reshape(bl, bl)
            key = np.array(Matrix(key).inv_mod(26))
            pt = ""
            for i in range(0, len(cipherText) // bl, bl):
                l = list(map(Cryptomax.HillCipher.aton, cipherText[i:i + bl:1]))
                l = np.array(l).reshape(bl, 1)
                l = np.dot(key, l)
                l = l % 26
                for j in range(bl):
                    pt += chr(l[j][0] + 97)

            return pt

    class Vignere:
        @staticmethod
        def generateKey(plainText, key):
            key = list(key.strip().upper())
            if len(plainText) == len(key):
                return (key)
            else:
                for i in range(len(plainText) -
                               len(key)):
                    key.append(key[i % len(key)])
                return "".join(key)

        @staticmethod
        def Encrypt(plaintext, key):
            plainText = plaintext.strip().upper()
            key = Cryptomax.Vignere.generateKey(plainText, key)
            cipher_text = []
            for i in range(len(plainText)):
                x = (ord(plainText[i]) +
                     ord(key[i])) % 26
                x += ord('A')
                cipher_text.append(chr(x))
            return "".join(cipher_text)

        @staticmethod
        def Decrypt(ciphertext, key):
            cipherText = ciphertext.strip().upper()
            key = Cryptomax.Vignere.generateKey(cipherText, key)
            orig_text = []
            for i in range(len(cipherText)):
                x = (ord(cipherText[i]) -
                     ord(key[i]) + 26) % 26
                x += ord('A')
                orig_text.append(chr(x))
            return "".join(orig_text)

    class Caesar:
        @staticmethod
        def transform(letter, shift):
            return chr((((ord(letter) - 97) + shift) % 26) + 97)

        @staticmethod
        def Encrypt(plainText, shift):
            return ''.join([Cryptomax.Caesar.transform(letter, shift) for letter in plainText])

        @staticmethod
        def Decrypt(plainText, shift):
            return ''.join([Cryptomax.Caesar.transform(letter, -shift) for letter in plainText])

    class Playfair:

        conv = lambda x: ord(x) - 97
        matrix = [['*' for i in range(5)] for j in range(5)]

        @staticmethod
        def construct_matrix(k):
            temp_arr = [False] * 26
            val = 0
            for iter in k + ''.join(list(map(chr, range(97, 123)))):
                if not temp_arr[Cryptomax.Playfair.conv(iter)]:
                    temp_arr[Cryptomax.Playfair.conv(iter)] = True
                    if iter in ('i', 'j'):
                        temp_arr[Cryptomax.Playfair.conv('i')] = True
                        temp_arr[Cryptomax.Playfair.conv('j')] = True
                    Cryptomax.Playfair.matrix[val // 5][val % 5] = 'i' if iter == 'j' else iter
                    val += 1

        @staticmethod
        def find_position(letter):
            for i in range(5):
                for j in range(5):
                    if Cryptomax.Playfair.matrix[i][j] == letter:
                        return i, j
            return -1, -1

        @staticmethod
        def check(pair, option):
            r1, c1 = Cryptomax.Playfair.find_position(pair[0])
            r2, c2 = Cryptomax.Playfair.find_position(pair[1])
            if r1 == r2:
                return Cryptomax.Playfair.matrix[r1][(c1 + option) % 5] + Cryptomax.Playfair.matrix[r2][
                    (c2 + option) % 5]
            elif c1 == c2:
                return Cryptomax.Playfair.matrix[(r1 + option) % 5][c1] + Cryptomax.Playfair.matrix[(r2 + option) % 5][
                    c2]
            else:
                return Cryptomax.Playfair.matrix[r1][c2] + Cryptomax.Playfair.matrix[r2][c1]

        @staticmethod
        def Encrypt(plaintext, key):
            Cryptomax.Playfair.construct_matrix(str(key).strip().lower())
            i = 0
            lst = []
            while i < len(plaintext):
                if i + 1 >= len(plaintext):
                    plaintext += 'x'
                elif plaintext[i] != plaintext[i + 1]:
                    lst.append(plaintext[i: i + 2])
                    i += 2
                else:
                    lst.append(plaintext[i] + 'x')
                    i += 1
            return ''.join([Cryptomax.Playfair.check(j, 1) for j in lst])

        @staticmethod
        def Decrypt(cipher):
            return ''.join(
                [Cryptomax.Playfair.check(pair, -1) for pair in [cipher[i:i + 2] for i in range(0, len(cipher), 2)]])
