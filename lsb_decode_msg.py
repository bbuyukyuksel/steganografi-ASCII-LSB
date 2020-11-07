import numpy as np
import cv2
import argparse
import time

def decode_bit(value:int, grade:int) -> int:
    return (value & (1<<grade)) >> grade

def bits_to_byte(bits:list) -> int:
    resolved = 0
    for index, bit in enumerate(bits):
        resolved += (bit << (7-index))
    return resolved

def decode(message:list):
    '''
        @param[message]: bit array
        byte2    byte1    byte0
        00000000 00000011 00000010
        0        3        2
        numerical ascii value (0*100) + (3*10) + (2*1)
    '''
    decoded = ""
    for i in range(0, len(message)-24, 24):

        byte2 = bits_to_byte(message[i+0:i+8])
        byte1 = bits_to_byte(message[i+8:i+16])
        byte0 = bits_to_byte(message[i+16:i+24])
        
        byte = 100 * byte2 + 10 * byte1 + byte0
        decoded += chr(byte)
    return decoded

def main(inputfile, grade):
    # Load Image
    org_image = cv2.imread(inputfile, cv2.IMREAD_COLOR)
    row, col, ch = org_image.shape

    # Flatten Image
    embedded = org_image.reshape(row*col*ch)

    # Decode
    raw_decoded_message = []
    for i, pixel in enumerate(embedded):
        decoded = decode_bit(pixel, grade)
        raw_decoded_message.append(decoded)

    decoded = decode(raw_decoded_message)
    print(decoded.split("<END>")[0])


if __name__ == '__main__':
    parser = argparse.ArgumentParser(prog='Decode LSB')
    parser.add_argument('-i', '--inputfile', required=True,help='Input Filepath')
    parser.add_argument('-l', '--level', type=int, required=False,  default=0, help='LSB Bit Level [Default:0]')
    args = parser.parse_args()

    start_time = time.time()
    main(args.inputfile, grade=args.level)
    print("Process Time:", time.time() - start_time, "[secs]")
