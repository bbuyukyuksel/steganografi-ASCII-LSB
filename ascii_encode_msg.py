import numpy as np
import cv2
import argparse
import os

def normalize_ascii(char):
    # Get Ascii Value of Char
    ascii_value = ord(char)
    # Eğer ki ascii value 2 haneli ise, 3 haneli yapmak için başa 0 ekle.
    return str(ascii_value) if int(ascii_value) > 99 else '0' + str(ascii_value)


def main(inputfilepath, message, verbose=True):    
    # Get Filename
    outputfilename = os.path.basename(inputfilepath).split('.')[0] # lena
    # Set Output Filename
    OUTFILENAME = f"{outputfilename}-ASCII.png"
    
    # Get Message and Prepare to Embed
    embed_message = f'{message}<END>'
    # Her bir karakterin ascii kodunu tek bir string içerisinde topla
    embedded_message = "".join(list(map(normalize_ascii, embed_message)))
    
    # Load Image
    org_image = cv2.imread(inputfilepath, cv2.IMREAD_COLOR) # 3 Kanallı görüntüyü oku.
    row, col, ch = org_image.shape
    
    # Flatten
    image = org_image.reshape(row * col * ch)

    # Image Correction
    maskgt250 = (image >= 250)
    imgcorrection = (maskgt250 * (image - 10)) + (~maskgt250 * image)


    assert row * col * ch >= len(embedded_message), "Yetersiz pixel alanı!"

    embedded = image.copy()
    if verbose:
        print("Input  File          :", inputfilepath)
        print("Output File Name     :", OUTFILENAME)
        print("Image Row x Col x Ch :", row, col, ch)
        print("Capacity             :", row*col*ch)
        print("."*30)
        print("Message              :", message, f"[{len(message)}]")
        print("Prepared Message     :", embed_message, f"[{len(embed_message)}]")
        print("Embedded Message     :", "-".join(list(map(normalize_ascii, message))), f"[{len(embedded_message)}]")
        # Table 
        print("{:12} # {:12} # {:12} # {:12} -> : {}".format("Iterasyon","Message","PX-ORG","PX-REPLACED","Decoded"))

    for i, msg in enumerate(embedded_message):
        # Fotoğrafın düzleşmiş halini flattened
        # Encode
        embedded[i] = ((imgcorrection[i] // 10) * 10) + (10 - int(msg))
        # Decode
        decoded = 10 - (embedded[i] % 10)
        decoded = 0 if decoded == 10 else decoded
        if verbose: print("{:<12} # {:<12} # {:<12} # {:<12} -> : {}".format(i, msg, imgcorrection[i], embedded[i], decoded))
    embedded = embedded.reshape(row, col, ch)
    cv2.imwrite(OUTFILENAME, embedded)
    

if __name__ == '__main__':
    parser = argparse.ArgumentParser(prog='Encode ASCII')
    parser.add_argument('-i', '--inputfile', required=True,help='Input Filepath')
    parser.add_argument('-m', '--message', required=True, help='Embed Message')
    args = parser.parse_args()
    
    if "@file:" in args.message.lower():
        messagefilepath = args.message.split("@file:")[1]
        with open(messagefilepath, 'r') as f:
            args.message = f.read()
        
    main(args.inputfile, args.message)

