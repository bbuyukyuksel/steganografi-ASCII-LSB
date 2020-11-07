import numpy as np
import cv2
import argparse

def decode_ascii(ascii_value_array):
    decoded_message = ""
    for i in range(0, len(ascii_value_array)-3, 3):
        ascii = 100 * ascii_value_array[i] + 10 * ascii_value_array[i+1] + ascii_value_array[i+2]
        decoded_message += chr(int(ascii))
    return decoded_message


def main(inputfile):
    # Load Image
    org_image = cv2.imread(inputfile, cv2.IMREAD_COLOR)
    row, col, ch = org_image.shape

    # Flatten Image
    embedded = org_image.reshape(row * col * ch)

    # Decode
    raw_decoded_message = []
    for i, pixel in enumerate(embedded):
        decoded = 10 - (pixel % 10)
        decoded = 0 if decoded == 10 else decoded
        raw_decoded_message.append(decoded)

    decoded_message = decode_ascii(raw_decoded_message)
    print(decoded_message.split("<END>")[0])


if __name__ == '__main__':
    parser = argparse.ArgumentParser(prog='Decode ASCII')
    parser.add_argument('-i', '--inputfile', required=True,help='Input Filepath')
    args = parser.parse_args()
    
    main(args.inputfile)


