#!/usr/local/bin/python3
import os
import sys
from PyPDF2 import PdfFileMerger

merger = PdfFileMerger()

if len(sys.argv[1:]) > 0:
    dir = sys.argv[1]
    contents = os.listdir(dir)
else:
    dir = os.getcwd()
    contents = os.listdir()

print("Contents of folder: \n\n", contents)

sorted_contents = sorted(list(map(lambda x: os.path.join(dir, x), contents)), key=os.path.getctime)
contents = [s.split(os.path.sep)[-1] for s in sorted_contents]
pdfs = list(filter(lambda x: x.endswith('.pdf'), contents))

confirmation = 'n'

while confirmation not in ['y', 'Y']:
    confirmation = input(f"\nThe final list of PDFs to be merged: \n\n{pdfs}\n\nTotal: {len(pdfs)}\n\nCONTINUE? ['y'/'Y'] or ADD ANY MORE EXCEPTIONS? ['n'/'N']\n> ")

    if confirmation in ['y', 'Y']:
        file_name = input("\nEnter the name of the merged pdf:\n> ")
        
        while file_name in os.listdir():
            file_name = input("\nThe file name already exists in this folder! Please give a unique name!\n> ")

        for file in pdfs:
            merger.append(os.path.join(dir, file))

        if len(pdfs) > 0:
            merger.write(file_name)
        else:
            exit(f"\nNo PDFs to merge... 🙃 Nice try!")

        print("\nThe PDFs have been succesfully merged as/in: ", os.path.abspath(file_name), " ✅")
    
    else:
        pdf_exceptions = input("\nEnter the PDF file names which should be excluded from the list separated by comma:\n> ").split(',')

        final_exceptions = []

        for exception in pdf_exceptions:
            if exception not in pdfs:
                print(f"\n❗️ {exception} does not exist in this directory! Skipping it...\n")
            else:
                print(f"\n❌ Removing '{exception}' from merger...")
                final_exceptions.append(exception)
        
        for exception in final_exceptions:
            pdfs = list(filter(lambda x: x != exception, pdfs))
            

