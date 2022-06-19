from PyPDF2 import PdfFileReader, PdfFileWriter
from PyQt5.QtCore import QThread, pyqtSignal
import os

class Pdf_manager(QThread):
    _signal = pyqtSignal(int)

    def __init__(self, frontpage_path, backpage_path, output_path, remove_blank_pages):
        super(Pdf_manager, self).__init__()
        self.frontpage_path = frontpage_path
        self.backpage_path = backpage_path
        self.remove_blank_pages = remove_blank_pages
        self.output_path = output_path

    # If a page is smaller than 80kB it is pobaply empty
    def __ispageempty(self, page):
        pdf_writer = PdfFileWriter()
        pdf_writer.addPage(page)
        with open("pdfduplex.tmp", 'wb') as out:
            pdf_writer.write(out)
        size = os.path.getsize("pdfduplex.tmp")
        os.remove("pdfduplex.tmp")
        if(size < 80000):
            print(page)
            return True
        return False
    
    def mergepdf(self):
        self._signal.emit(0)
        pdf_writer = PdfFileWriter()

        try:
            front = PdfFileReader(self.frontpage_path)
        except Exception as e:
            return(e.__str__())

        try:  
            back = PdfFileReader(self.backpage_path)
        except Exception as e:
            return(e.__str__())
    
        if front.getNumPages() != back.getNumPages():
            return("Front- and backpages have to have the same amount of pages")
        
        for page in range(front.getNumPages()):
            percent = page / front.getNumPages()
            self._signal.emit((int)(50*percent))
            if not self.remove_blank_pages:
                pdf_writer.addPage(front.getPage(page))
                pdf_writer.addPage(back.getPage(back.getNumPages() - page -1))
            else:
                if not self.__ispageempty(front.getPage(page)):
                    pdf_writer.addPage(front.getPage(page))
                if not self.__ispageempty(back.getPage(back.getNumPages() - page -1)):
                    pdf_writer.addPage(back.getPage(back.getNumPages() - page -1))

        self._signal.emit(50)

        try:
            with open(self.output_path, 'wb') as out:
                pdf_writer.write(out)
        except Exception as e:
            return(e.__str__())

        self._signal.emit(100)