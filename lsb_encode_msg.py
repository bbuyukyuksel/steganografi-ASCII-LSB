import numpy as np
import cv2
import argparse
import os

def set_bit(value:int, grade:int) -> int:
        return value | (1<<grade)


def clear_bit(value:int, grade:int) -> int:
    return value & ~(1<<grade)


def decode_bit(value:int, grade:int) -> int:
    return (value & (1<<grade)) >> grade


def process_bit(value:int, bit:int, grade:int) -> int:
    if bit == 0:
        return clear_bit(value, grade)
    elif bit == 1:
        return set_bit(value, grade) 


def normalize_ascii(char:str) -> str:
    # Get Ascii Value
    ascii_value = ord(char)
    # Eğer ki ascii value 2 haneli ise, 3 haneli yapmak için başa 0 ekle.
    return str(ascii_value) if int(ascii_value) > 99 else '0' + str(ascii_value)

def main(inputfile, embed_message, method_type, grade, verbose=True):
    # Get Filename
    outputfilename = os.path.basename(inputfile).split('.')[0]
    # Set Output Filename
    OUTFILENAME = f"{outputfilename}-LSB_LEVEL_{grade}-{method_type.upper()}.png"

    # Prepare Message
    ## Append indicator '<END>' to decode message
    message = f'{embed_message}<END>'

    embedded_message = "".join(list(map(normalize_ascii, message)))
    list_embedded_bit_message = []
    for index, character in enumerate(embedded_message):
        # Example 
        # 3: 0b11 - string içerisinden 0b'yi silmeliyiz ve 8 bit olucak şekilde 0'larla stringi doldurmalıyız
        bin_str = bin(int(character)).split('0b')[1].rjust(8, '0')
        list_embedded_bit_message.append(bin_str)
    str_embedded_bit_message = "".join(list_embedded_bit_message)

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

    assert row * col >= len(embedded_message), "Not enough pixel space!"

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
        print("Embedded Bit Message :", "-".join(list_embedded_bit_message), f"[{len(str_embedded_bit_message)}]")
        # Table 
        print("{:12} # {:12} # {:12} # {:12} -> : {}".format("Iterasyon","Message","PX-ORG","PX-REPLACED","Decoded"))

    # Embed Message to Image
    for i, bit in enumerate(str_embedded_bit_message):
        # Encode Message
        embedded[i] = process_bit(flattened[i], int(bit), grade=grade)
        # Decode Message to Print
        decoded = decode_bit(embedded[i], grade)
        if verbose: print("{:<12} # {:<12} # {:<12} # {:<12} -> : {}".format(i, bit, flattened[i], embedded[i], decoded))

    embedded.resize(row, col)

    if method_type.lower() == "gray":
        merged = cv2.merge([embedded, embedded, embedded])
    else:
        merged = cv2.merge([embedded, g, b])

    cv2.imwrite(OUTFILENAME, merged)
    
if __name__ == '__main__':
    parser = argparse.ArgumentParser(prog='Encode LSB')
    parser.add_argument('-i', '--inputfile', required=True,help='Input Filepath')
    parser.add_argument('-m', '--message', required=True, help='Embed Message')
    parser.add_argument('-t', '--type', required=True, help='Options: [GRAY, RGB]')
    parser.add_argument('-l', '--level', type=int, required=False,  default=0, help='LSB Bit Level [Default:0]')
    args = parser.parse_args()

    assert args.type.lower() in ['gray', 'rgb'], "Incorrect method selection!"

    main(args.inputfile, args.message, args.type, args.level)

    
    


    
    
  


        
