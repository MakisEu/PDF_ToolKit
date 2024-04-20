from pdf2image import pdfinfo_from_path,convert_from_path
import tempfile
import os


def resolveFileExtension(format):
    if   (format=="JPEG"):
        return ".jpg"
    elif (format=="PNG"):
        return ".png"
class converter():

    def __init__(self,file_path,converTo="JPEG"):
        self.pages=None
        self.pdf_path=file_path
        self.pages_accessed=0
        info = pdfinfo_from_path(file_path, userpw=None, poppler_path=None)
        self.max_pages=info["Pages"]
        self.format=converTo
        self.file_name = os.path.basename(file_path)[:-4]
        self.defaultOutputPath=file_path[:-4]

    def convertPageChunck(self,page_file_name,pdf_path=None,output_folder=None,first_page=1,last_page=None,quality=200):
        if (last_page==None):
            last_page=self.max_pages
        if (pdf_path==None):
            pdf_path=self.pdf_path
        
        cnt=first_page-1;
        for page in convert_from_path(pdf_path,output_folder=output_folder,first_page=first_page, last_page=last_page,dpi=quality):
            page_name=page_file_name+str(cnt)+resolveFileExtension(self.format)
            page.save(page_name, self.format)
            cnt+=1

    def writePDF(self,folder_path=None,format=None): 
        if (format!=None):
            self.format=format
        if (folder_path==None):
            folder_path=self.defaultOutputPath
        print(folder_path)
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)
            with tempfile.TemporaryDirectory() as path:
                for i in range(1,self.max_pages+1,10):
                    last_page = min(i+10-1,self.max_pages)
                    page_name=folder_path+os.sep+self.file_name+"_page_"
                    self.convertPageChunck(page_file_name=page_name,pdf_path=self.pdf_path,output_folder=path,first_page=i, last_page=last_page)
                    self.pages_accessed=i


if (__name__=="__main__"):
    filename=input("Give pdf file path: ")
    format=input("Convert file to (PNG, JPEG): ")
    converter(filename,format).writePDF()

