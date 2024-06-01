import cv2
import os
from pyfiglet import Figlet
from functions import *

# Fauzanil Zaki, 2017
# feel free to use

if __name__ == '__main__':
    # Cool boi
    f = Figlet(font='slant')
    print(f.renderText("CCVS"))
    print("CaesarCipherVideoSteganography\n")

    print("Menu :")
    print("(a) Encypt & Merge into Video")
    print("(b) Decrypt & Get the plain text")
    print("-----------------------")
    choice = input("(!) Choose option : ")

    if choice == "a":
        print(f.renderText("Encrypt"))
        print("----------------------------------------")
        file_name = input("(1) Video file name in the data folder  ? : ")

        try:
            caesarn = int(input("(2) Caesar cypher n value  ? : "))
        except ValueError:
            print("-----------------------")
            print("(!) n is not an integer ")
            exit()

        try:
            open("data/" + file_name)
        except IOError:
            print("-----------------------")
            print("(!) File not found ")
            exit()

        print("-----------------------")
        print("(-) Extracting Frame(s)")
        frame_extract(str(file_name))
        print("(-) Extracting audio")
        os.system(f'ffmpeg -i data/{file_name} -q:a 0 -map a temp/audio.mp3 -y')
        print("(-) Reading text-to-hide.txt")
        print("(-) Encrypting & appending string into frame(s) ")
        encode_frame("temp", "data/text-to-hide.txt", caesarn)
        print("(-) Merging frame(s) ")
        os.system("ffmpeg -i temp/%d.png -vcodec png temp/video.mov -y")
        print("(-) Optimizing encode & Merging audio ")
        os.system(f'ffmpeg -i temp/video.mov -i temp/audio.mp3 -codec copy data/enc-{file_name} -y')
        print("(!) Success, output: enc-" + file_name)

    elif choice == "b":
        print(f.renderText("Decrypt"))
        print("----------------------------------------")
        file_name = input("(1) Video file name in the data folder  ? : ")

        try:
            caesarn = int(input("(2) Caesar cypher n value  ? : "))
        except ValueError:
            print("-----------------------")
            print("(!) n is not an integer ")
            exit()

        try:
            open("data/" + file_name)
        except IOError:
            print("-----------------------")
            print("(!) File not found ")
            exit()

        print("-----------------------")
        print("(-) Extracting Frame(s)")
        frame_extract(str(file_name))
        print("(-) Decrypting Frame(s)")
        decode_frame("temp", caesarn)
        print("(!) Success")

    else:
        exit()
