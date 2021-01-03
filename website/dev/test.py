from PyPDF2 import PdfFileWriter, PdfFileReader
from io import BytesIO
import re

# with open('testfile1.pdf', 'rb') as input_file:
#     pdf = PdfFileReader(input_file)
#     #number_of_pages = pdf.getNumPages()
#     #print("Number of pages: {0}".format(number_of_pages))


#open('testfile1.pdf', 'rb').read()

# with BytesIO(filebytes) as pdf_file_stream:
#     pdf_file = PdfFileReader(pdf_file_stream)

# pdf = PdfFileReader(input_file)
#     import pdb
#     pdb.set_trace()

pdf_file_stream = BytesIO(open('testfile1.pdf', 'rb').read())
pdf_file = PdfFileReader(pdf_file_stream)
pdf_file_page_count = pdf_file.getNumPages()

terminator_candidates = []

txt = pdf_file.getPage(0).extractText()
newline_terminated_strings = txt.split('\n')
for candidate in newline_terminated_strings:
    if len(candidate.strip()) > 0:
        terminator_candidates.append(candidate)

print(terminator_candidates)

# Some steps to allow user to select terminating text

selected_candidate = 'School Name: '
file_terminator = "{0}\n".format(selected_candidate)

# After we have the selected terminating text

start_new_file = True
profile_number = 1

for page_index in range(pdf_file_page_count):

    print("\nPage index: {0}".format(page_index))

    page = pdf_file.getPage(page_index)
    txt = page.extractText()
    print(txt)
    import pdb
    pdb.set_trace()

    print("start_new_file is: {0}".format(start_new_file))

    if start_new_file:
        start_new_file = False
        outfile = PdfFileWriter()

        # if txt.find(file_terminator) < 0:
        #     outfile.addPage(page)
        #     print("no terminator found - 1")
        # else:
        #     m = re.search("School Code: \n(.+) ", txt) # intentionally wrong should be school name
        #     student_id = profile_number
        #     if m is not None:
        #         student_id = m.groups()[0].strip()

    if txt.find(file_terminator) < 0:
        outfile.addPage(page)
        start_new_file = False
        print("no terminator found - 2") # and continue
    else:
        print("Terminator found; write to file") 
        # Add the page
        outfile.addPage(page)
        with open('%s.pdf' % (profile_number), 'wb') as f:
            outfile.write(f)
            start_new_file = True
            print("profile_number: {0}".format(profile_number))
            profile_number = profile_number + 1


print("END-OF-PROCESS")