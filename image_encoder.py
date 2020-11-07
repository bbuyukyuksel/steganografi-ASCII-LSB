import cv2
import base64
import argparse

def image_encode(inputfile):
    with open(inputfile, "rb") as image_file:
        content = image_file.read()
        print(base64.b64encode(content).decode('utf-8'))

def image_decode(filepath):
    with open(filepath, 'r') as f:
        content = base64.b64decode(f.read())
    with open('image-recov.png', 'wb') as f:
        f.write(content)

def main(filepath, methodtype):
    if methodtype == 'encode':
       image_encode(filepath)
    elif methodtype == 'decode':
        image_decode(filepath) 

if __name__ == '__main__':
    parser = argparse.ArgumentParser(prog='Image Encode')
    parser.add_argument('-f', '--filepath', required=True,help='Filepath')
    parser.add_argument('-t', '--methodtype', required=True,help='Method Type')
    args = parser.parse_args()

    assert args.methodtype.lower() in ['encode', 'decode'], "Exception Type"
    
    main(args.filepath, args.methodtype)

