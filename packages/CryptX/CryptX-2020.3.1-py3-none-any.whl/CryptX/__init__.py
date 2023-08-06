import base64
def Encrypter(message, key):
    enc=[]
    for i in range(len(message)):
        key_c = key[i % len(key)]
        enc.append(chr((ord(message[i]) + ord(key_c)) % 256))
    mlen = len(message)
    klen = len(key)
    mlen = len(message)*3
    if klen >= mlen:
        return base64.urlsafe_b64encode("".join(enc).encode()).decode()
    else:
        return "Key should be 3 times of message in lenth."

def Decrypter(message, key):
    dec=[]
    message = base64.urlsafe_b64decode(message).decode()
    for i in range(len(message)):
        key_c = key[i % len(key)]
        dec.append(chr((256 + ord(message[i])- ord(key_c)) % 256))
    return "".join(dec)

def main():
    a = input("What do you want to do ?['e'ncrypt, 'd'ecrypt]: ")

    if a == "e":
        message = input("Please Enter the Message: ")
        password = input("Please Enter the Password for Protection: ")
        out = Encrypter(message, password)
        print(f'Super Secret Code: {out}')
    elif a == "d":
        code = input("Please Enter the Super Secret Key: ")
        password = input("Please Enter the Password: ")
        out = Decrypter(code, password)
        print(f'Message: {out}')

if __name__=="__main__":
    main()