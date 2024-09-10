'''
    USAGE:
    1. Place this file into a folder
    2. Place multiple PDF files alongside it into the same folder
    3. Run this file
    
    It will take the desired pages (default 1 and 3), combine them all into a single, huge and ugly PDF file which allows
    for you to print X amount of pages all with one print job.
'''
# The specific PDF pages you want. You can add as many as you want, as long as they are separated by a comma.
pages_to_print = [1, 3]


import os
import shutil
import datetime
from PyPDF2 import PdfReader, PdfWriter

combined_pdf_name = "combined-files.pdf"
current_folder_path = os.path.dirname(os.path.abspath(__file__))  #golder where we work out of
printed_folder_path = os.path.join(current_folder_path, f"Printed {datetime.datetime.now().strftime('%d-%m-%Y')}")
auto_open = True
invalid_pages_variable_text = (
	"The 'pages_to_print' variable is incorrect. This program will not work beyond this point." 
	"\nIf you edit this file in notepad, you will see this setting near the top (about 11 lines down)" 
	"\n\nIf you wanted to print the first page, it would look like 'pages_to_print = [1]'" 
	"\nIf you wanted to print page 1 3 and 4, it would look like 'pages_to_print = [1, 3, 4]'" 
	"\n\nNotice there is never a comma after the LAST number, only the ones that come before it!"
)


if not os.path.exists(printed_folder_path):
    os.makedirs(printed_folder_path)
    
    
#opting to delete the old file on start just to remove any potential confusion between script uses
if os.path.exists(os.path.join(current_folder_path, combined_pdf_name)):
    os.remove(combined_pdf_name)
    
    
def combine_pdf_pages(pdf_files, pages_to_print):
    combined_writer = PdfWriter()

    for pdf_file in pdf_files:
        if pdf_file == combined_pdf_name:
            continue
            
        pdf_reader = PdfReader(pdf_file)

        #add the specified pages to our monstronsity-file
        for page in pages_to_print:
            if page - 1 < len(pdf_reader.pages):
                combined_writer.add_page(pdf_reader.pages[page - 1])

    #save the combined PDF to a temporary file
    combined_pdf_path = os.path.join(current_folder_path, combined_pdf_name)
    with open(combined_pdf_path, "wb") as combined_pdf:
        combined_writer.write(combined_pdf)

    return combined_pdf_path


def main():
    if not pages_to_print or not all(isinstance(x, (int, float)) for x in pages_to_print):
        print(invalid_pages_variable_text)
        return

    already_printed_files = []
    for existing_pdf in os.listdir(printed_folder_path):
        if existing_pdf.lower().endswith(".pdf"):
            already_printed_files.append(existing_pdf)

    pdf_files = []

    #add each pdf to our list, excluding our big ugly monstrosity
    for pdf in os.listdir(current_folder_path):
        if pdf.lower().endswith(".pdf") and pdf != combined_pdf_name:
            #skip if duplicate file
            if pdf in already_printed_files:
                print(f"Didn't print duplicate file: '{pdf}'")
                continue
                
            pdf_path = os.path.join(current_folder_path, pdf)
            pdf_files.append(pdf_path)

    if not pdf_files:
        print("No PDF files found to print.")
        return

    #combine the specified pages from all files into one
    combined_pdf_path = combine_pdf_pages(pdf_files, pages_to_print)
    
    print(f"Combined {len(pdf_files)} PDF's into {combined_pdf_name}")

    #move the old, individual files to a subfolder for organization
    for pdf in pdf_files:
        shutil.move(pdf, os.path.join(printed_folder_path, os.path.basename(pdf)))
        
    os.startfile(combined_pdf_path)


if __name__ == "__main__":
    main()


input("\n\nPress ENTER to exit")