import random
from PIL import Image
from Stegan import Encode, Decode
import math

def isPrime(nu) :
    if (nu <= 1) :
        return False
    if (nu <= 3) :
        return True
    if (nu % 2 == 0 or nu % 3 == 0) :
        return False
    i = 5
    while(i * i <= nu) :
        if (nu % i == 0 or nu % (i + 2) == 0) :
            return False
        i = i + 6
    return True

def egcd(a, b):
    if a == 0:
        return (b, 0, 1)
    else:
        g, y, x = egcd(b % a, a)
        return (g, x - (b // a) * y, y)

def modinv(a, m):
    g, x, _ = egcd(a, m)
    if g != 1:
        raise Exception('modular inverse does not exist')
    else:
        return x % m

def bezout(a, b):
    if a == 0 and b == 0: 
        return (0, 0, 0)
    if b == 0: 
        return (a/abs(a), 0, abs(a))
    (u, v, p) = bezout(b, a%b)
    return (v, (u - v*(a/b)), p)

def cipher(num,e):
    for i in range(len(num)):
        X.append((int(num[i])**e)%n)
        
def decipher(num,d):
    for i in range(len(num)):
        Y.append((int(num[i])**d)%n)

def DecryptText():
    global i,Y
    Y=[]
    encoded_image_file = (input("File to decrypt :"))
    img2 = Image.open(encoded_image_file)
    print(img2, img2.mode)
    hidden_text = Decode(img2, n)
    decipher(hidden_text,d)
    print("Number of Ciphertext blocks:", len(Y))
    numD=[]
    for i in range(len(Y)):
       numD.append(chr(Y[i]))
    for i in numD:
        print(i,end="")
    print("\n")   

def EncryptText():
    # encrypts a plaintext message using the current key
    global plaintext, numC, X
    X=[]
    plaintext = (input("Enter Text (Unicode):"))
    numC = []
    for i in range(len(plaintext)):
        unicode = ord(plaintext[i])
        if (unicode >= 32):
            numC.append(str(unicode))
    cipher(numC,e)
    print("Number of Ciphertext blocks:", len(X))
    original_image_file = (input("File to encrypt :"))
    img = Image.open(original_image_file)
    print(img, img.mode)
    encoded_image_file = "enc_" + original_image_file
    img_encoded = Encode(img, len(plaintext), X, n)
    if img_encoded:
        img_encoded.save(encoded_image_file)
        print("{} saved!".format(encoded_image_file))

def DecryptBinary():
    global i,Y
    Y=[]
    encoded_image_file = (input("File to decrypt :"))
    img2 = Image.open(encoded_image_file)
    print(img2, img2.mode)
    hidden = Decode(img2, 255)

    extracted_file = (input("New extracted filename :"))
    newfile=open(extracted_file,'wb')
    for i in range(len(hidden)):
        newfile.write(hidden[i].to_bytes(1, byteorder='big'))
    newfile.close
    print("Extract OK")   

def EncryptBinary():
    # encrypts a file using the current key
    global plaintext, numC, X
    X=[]
    numC = []
    index = 0
    file_to_hide = (input("File to hide:"))
    with open(file_to_hide, "rb") as f:
        while (bytes_read := f.read(1)):
            for b in bytes_read:
                numC.append(b)
                index+=1
    f.close
    original_image_file = (input("File to encrypt :"))
    img = Image.open(original_image_file)
    print(img, img.mode)    
    encoded_image_file = "enc_" + original_image_file
    img_encoded = Encode(img, index, numC, 255)
    if img_encoded:
        img_encoded.save(encoded_image_file)
        print("{} saved!".format(encoded_image_file))

def menu():
    print("To redefine p,q,e, type 'p','q',... etc.")
    print("To encrypt a unicode message with the current key, type 'EncryptText'")
    print("To decrypt a unicode message with the current key, type 'DecryptText'")
    print("Type quit to exit")
    print('\n')
    print('\n')

p = 347
q = 257
n = p * q
phi_n = (p - 1) * (q - 1)
e = 5721
d = 3561

menu()
mm = str()
mm = str()
while mm != 'quit':
    mm = input("Enter Command: ")
    if mm.lower() == 'encrypttext':
        EncryptText()
    elif mm.lower() == 'decrypttext':
        DecryptText()
    if mm.lower() == 'storefile':
        EncryptBinary()
    elif mm.lower() == 'extractfile':
        DecryptBinary()
    elif mm.lower() == 'p':
        try:
            print('current p = ', p)
            p1 = int(input(" Enter a value for p:"))
            if p1 != q and (isPrime(p1)):
                p=p1
                n = p * q
                phi_n = (p - 1) * (q - 1)
                print('p set to :', p)
                print('n set to :', n)
                print('phi(n) set to :', phi_n)
            else :
                print('Invalid input, p need to be prime and diffrent of q')
        except ValueError:
            print('please enter a number')
    elif mm.lower() == 'q':
        try:
            print('current q = ', q)
            q1 = int(input(" Enter a value for q:"))
            if q1 != p and (isPrime(q1)):
                q=q1
                n = p * q
                phi_n = (p - 1) * (q - 1)
                print('q set to :', q)
                print('n set to :', n)
                print('phi(n) set to :', phi_n)
            else :
                print('Invalid input, q need to be prime and different of p')
        except ValueError:
            print('please enter a number')
    elif mm.lower() == 'help':
        menu()
    elif mm.lower() == 'e':
        try:
            print('current e = ', e)
            e1 = int(input(" Enter a value for e :"))
            (u, _, p) = bezout(e1, phi_n)
            if p != 1: 
                print("%s and %s are not prime among themselves" % (e1, phi_n))
            else :
                e=e1
                d = modinv(e, phi_n)
                print('e set to :', e)
                print('d set to :', d)
        except ValueError:
            print('please enter a number')
    else:
        if mm != 'quit':
            ii = random.randint(0, 6)
            statements = ["This cannot be done", "Read the directions again", "Didnt say the magic word", "This input is UNACCEPTABLE!!","Was that even a word???", "Please follow thedirections","Just type 'help' if you are really that lost"]
            print(statements[ii])
