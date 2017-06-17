#!/usr/bin/python3
#
#Notebook2PDF - a scanning tool. This is intended for a fixed-sized document that needs
#to be scanned, datestamped, and appended to on a regular basis (eg, a notebook) on
#a flatbed scanner without an automatic document feeder.
#
#Written by David Faour June 16-17, 2017
#
#Requirements:
# tiff2pdf (on openSUSE, run 'zypper in tiff')
# ImageMagick ('zypper in ImageMagick')
# pdfunite (from the poppler package; 'zypper in poppler-tools')
# sane ('zypper in sane-backends')

import os
import sys
import time

#Set size of scan in "x" dimension (mm):
xmm = "80"

#Set size of scan in "y" dimension (mm):
ymm = "120"

#Scanning resolution
res = "300"

try:
    outputFile = sys.argv[1]
except:
    print("Usage: ./scan2pdf /path/to/pdf")
    exit()

choice = ""
exist = 0


#First let's test to see if file already exists. If it does, should we overwrite or append?
if (os.path.isfile(outputFile) == True):
    exist = 1
    choice = input(outputFile + " already exists. Should I [O]verwrite or [A]ppend (default)? ")
    if (choice == "O") or (choice == "o"):
        yn = input("Are you sure? " + outputFile + " will be deleted! (y/N) ")
        if (yn != "y") and (yn != "Y"):
            print("Exiting. Goodbye!")
            exit()

def overwrite(outputFile):
    os.system("rm " + outputFile)
    os.system("mv /tmp/tempscan.pdf " + outputFile)
    print(outputFile + " overwritten.")
    return

def append(outputFile):
    os.system("pdfunite " + outputFile + " /tmp/tempscan.pdf /tmp/tempscan2.pdf")
    os.system("rm " + outputFile)
    os.system("mv /tmp/tempscan2.pdf " + outputFile)
    os.system("rm /tmp/tempscan.pdf")   
    print("Appended to " + outputFile)

def scanImage():
    date = time.strftime("%Y-%m-%d %H:%M:%S")
    print("Scanning file...")
    #Scan
    os.system("scanimage --format tiff -x " + xmm + " -y " + ymm + " --resolution " + res + " > /tmp/tempscan.tiff")
    print("Processing...")
    #Date stamp
    os.system("convert -pointsize 20 -fill red -gravity SouthEast -draw 'text 50,30 \"" + date + "\"' /tmp/tempscan.tiff /tmp/tempscan2.tiff 2>/dev/null")
    os.system("tiff2pdf -o /tmp/tempscan.pdf /tmp/tempscan2.tiff")


scanImage()

#Determine what to do based on whether file is new or already exists; if it already exists are we appending or overwriting?
if (choice == "o") or (choice == "O") and (exist == 1):
    overwrite(outputFile)
elif (choice == "a") or (choice == "A") and (exist == 1):
    append(outputFile)
else:
    os.system("mv /tmp/tempscan.pdf " + outputFile)
    print(outputFile + " created.")


#For multipage documents, we want to scan repeatedly
again = "y"
while (again == "y") or (again == "Y"):
    os.system("rm /tmp/tempscan.tiff")
    os.system("rm /tmp/tempscan2.tiff")
    again = input("Would you like to scan and append another page to file " + outputFile + "? (y/N) ")
    if (again == "y") or (again == "Y"):
        scanImage()
        append(outputFile)
    else:
        print("Goodbye!")
        exit()

