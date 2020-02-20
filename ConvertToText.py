import PyPDF2 
import os

def read_pdf_file(filename):

    count = 0
    house_text = ""
    senate_text = ""
    try:
        pdfFileObj = open(filename,'rb')
        pdfReader = PyPDF2.PdfFileReader(pdfFileObj)
        num_pages = pdfReader.numPages
        while count < num_pages:
            pageObj = pdfReader.getPage(count)
            count += 1
            page = pageObj.extractText() 
            page = page[:page.rfind("VerDate")]
            if count == 1:
                page = page[ page.find("House of Representatives") + 25 :]
                house_text += page
                continue
            else:
                if(page[21]=='H'):
                    page = get_end_of_intro(page)
                    house_text += page
                    continue
                else:
                    page = get_end_of_intro(page)
                    senate_text += page
    except Exception as e:
        if type(e) == KeyboardInterrupt:
            raise e
        print(f"File {filename} is not in valid format.")
    return house_text, senate_text

def get_end_of_intro(page):
    if page.find("2019") == -1:
        return page[page.find("2020")+5:]
    if page.find("2020") == -1:
        return page[page.find("2019")+5:]
    return page[min(page.find("2019"),page.find("2020"))+5:]
    

directory = r'transcripts-pdf/'
for filename in os.listdir(directory):
    house_text, senate_text = read_pdf_file(str(directory)+filename)
    open(f"transcripts-txt/house-{filename[:len(filename)-4]}.txt","w+").write(house_text)
    open(f"transcripts-txt/senate-{filename[:len(filename)-4]}.txt","w+").write(senate_text)
    print(f"converted {filename} to text.")