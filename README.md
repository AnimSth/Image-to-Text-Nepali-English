# Image-to-Text-Nepali-English
This model requires pytesseract and a Nepali  language Model to read through citizenships and extract the data in the uploaded picture. 
To download pytesseract go to (https://github.com/UB-Mannheim/tesseract/wiki) and download tesseract-ocr setup according to your requirement.

After you download pytesseract, 
1. Go to the model folder and download the three folders(langdata-main, tessdata & tessdata-main) to the base folder of the tesseract( In most cases it is (C:\Program Files\tesseract\))
2. Make sure to set it as an environment variable to import it to your pyfile.

Rest required modules like openCV, numpy & flask can be easily be installed through pip or pip3. Also, change the upload folder according to your meets.



For more accuracy, adjust the image sharpening section in app.py according to the requirements of the desired image.
