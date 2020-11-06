import numpy as np
import cv2
import argparse
import os

def normalize_ascii(char):
    ascii_value = ord(char)
    # Eğer ki ascii value 2 haneli ise, 3 haneli yapmak için başa 0 ekle.
    return str(ascii_value) if int(ascii_value) > 99 else '0' + str(ascii_value)


def main(inputfile, embed_message, method_type, verbose=True):
    # Get Filename
    outputfilename = os.path.basename(inputfile).split('.')[0]
    # Set Output Filename
    OUTFILENAME = f"{outputfilename}-ASCII-{method_type.upper()}.png"
    
    # Get Message and Prepare to Embed
    message = f'{embed_message}<END>'
    embedded_message = "".join(list(map(normalize_ascii, message)))
    
    # Load Image
    org_image = cv2.imread(inputfile, cv2.IMREAD_COLOR)
    row, col, ch = org_image.shape
    
    # Split Channels if have one more than
    r,g,b = cv2.split(org_image)

    # Select Channel
    # One Channel
    image = r.copy()

    # Image Correction
    maskgt250 = (image > 250)
    imgcorrection = (maskgt250 * (image - 10)) + (~maskgt250 * image)

    # Flatten Image
    flattened = imgcorrection.flatten()

    assert row * col >= len(embedded_message), "Yetersiz pixel alanı!"

    embedded = flattened.copy()

    if verbose:
        print("Input  File          :", inputfile)
        print("Output File Name     :", OUTFILENAME)
        print("Method               :", method_type.upper())
        print("Image Row x Col x Ch :", row, col, ch)
        print("."*30)
        print("Message              :", embed_message, f"[{len(embed_message)}]")
        print("Prepared Message     :", message, f"[{len(message)}]")
        print("Embedded Message     :", "-".join(list(map(normalize_ascii, message))), f"[{len(embedded_message)}]")
        # Table 
        print("{:12} # {:12} # {:12} # {:12} -> : {}".format("Iterasyon","Message","PX-ORG","PX-REPLACED","Decoded"))

    for i, msg in enumerate(embedded_message):
        embedded[i] = ((flattened[i] // 10) * 10) + (10 - int(msg))
        decoded = 10 - (embedded[i] % 10)
        decoded = 0 if decoded == 10 else decoded
        if verbose: print("{:<12} # {:<12} # {:<12} # {:<12} -> : {}".format(i, msg, flattened[i], embedded[i], decoded))
    embedded.resize(row, col)

    if method_type.lower() == "gray":
        merged = cv2.merge([embedded, embedded, embedded])
    else:
        merged = cv2.merge([embedded, g, b])

    cv2.imwrite(OUTFILENAME, merged)
    

if __name__ == '__main__':
    parser = argparse.ArgumentParser(prog='Encode ASCII')
    parser.add_argument('-i', '--inputfile', required=True,help='Input Filepath')
    parser.add_argument('-m', '--message', required=True, help='Embed Message')
    parser.add_argument('-t', '--type', required=True, help='Options: [GRAY, RGB]')    
    args = parser.parse_args()
    
    assert args.type.lower() in ['gray', 'rgb'], "Incorrect method selection!"

    main(args.inputfile, args.message, args.type)

