import cv2
import os
import argparse

if __name__ == '__main__': 
    parser = argparse.ArgumentParser(prog='Image Encode')
    parser.add_argument('-f', '--filepath', required=True,help='Filepath')
    parser.add_argument('-s', '--size', required=True,type=int, help='Method Type')
    args = parser.parse_args()

    filename = os.path.basename(args.filepath)
    img = cv2.imread(args.filepath, cv2.IMREAD_UNCHANGED)
    dim = (args.size, args.size)
    # resize image
    resized = cv2.resize(img, dim, interpolation = cv2.INTER_AREA)
    
    outpath = "Resized"
    os.makedirs(outpath, exist_ok=True)
    outfile = os.path.join(outpath,f"{filename}-{args.size}x{args.size}.png")
    print("+ Success: ", outfile)
    cv2.imwrite(outfile, resized)
