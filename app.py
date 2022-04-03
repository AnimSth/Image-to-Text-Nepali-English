import json, cv2, os
from flask import Flask, request, render_template, flash
import numpy as np
import pytesseract as tess
#this is an environment variable
tess.pytesseract.tesseract_cmd = r'C:\Program Files\tesseract\tesseract'
from werkzeug.utils import secure_filename


app = Flask(__name__)
app.config['SECRET_KEY'] = "tobeornottobe"
client = pymongo.MongoClient()
db = client['langData']

box =[]
fox =[]

#function to read through the image

def text(data, box ,lan):#(data = image, box = empty list, lan = language)
    #image sharpening
    data = cv2.resize(data, None, fx=1.2, fy=1.2,interpolation=cv2.INTER_CUBIC)
    data = cv2.cvtColor(data, cv2.COLOR_BGR2GRAY)
    kernel = np.array([[0, -1, 0],
                   [-1, 5,-1],
                   [0, -1, 0]])         
    data = cv2.filter2D(data, -1, kernel)
    #Extracting text form image
    tex = tess.image_to_string(data, lang=lan)
    box.append(tex)
    
    #this loop rotates and extracts the text from the image and appends it to empty list
    for i in range(3):
        data = cv2.rotate(data, cv2.ROTATE_90_COUNTERCLOCKWISE)
        tex = tess.image_to_string(data, lang=lan)
        box.append(tex)



@app.route('/')
def home():
    #to open the local json file
    with open('database.json','r', encoding='utf-8') as fp:
        ldata = json.load(fp)   
    return render_template('uploads.html',ldata = ldata)



UPLOAD_FOLDER = 'static/front/'
UPLOAD_FOLDER1 = 'static/back/'

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['UPLOAD_FOLDER1'] = UPLOAD_FOLDER1

@app.route('/uploads', methods= ['POST','GET'])
def upload():
    if request.method =='POST':
        
        image = request.files['image']
        Backimage = request.files['image2']
        filename = secure_filename(image.filename)
        filename2 = secure_filename(Backimage.filename)
        image.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        Backimage.save(os.path.join(app.config['UPLOAD_FOLDER1'], filename2))
        if image and Backimage:
           
            data = cv2.imread(f'static/front/{image.filename}', 1)
            dataB = cv2.imread(f'static/back/{Backimage.filename}', 1)
            
            lan = 'nep'           #(lan = language set to nepali)
            lan1 = 'eng+nep'      #(lan1 = language set to english and  nepali)
            
            # calling the function
            text(data, box, lan)
            text(dataB, fox, lan1)
            tex = max(box, key=len)
            texB = max(fox, key=len)

            
            # this statements confirms whether the given image has characteristics of citizenship or not
            if 'नेपाली नागरिकताको' in tex and 'Citizenship Certificate' in texB:
                data={}
                data["front"]=tex
                data["back"]=texB

                prevdata=""
                
                # to append the data into local json file
                with open('database.json',encoding='utf-8') as f:
                    d = json.load(f)
                    prevdata=d
                    print(type(d))

                with open('database.json', 'w', encoding='utf-8') as f:
                    prevdata.append(data)
                    json.dump(prevdata, f, ensure_ascii=False, indent=4)
                    
                flash('Success!, Look at the table below to view the scraped data',category = 'success')

                return redirect(url_for('home'))

            else:
                flash('Please upload a clearer picture')
                return redirect(url_for('home'))
                
        else:
            flash('Please upload a clearer picture',category = 'error')
            return redirect(url_for('home'))
    else:
        return redirect(url_for('home'))
        

if __name__ == "__main__":
    app.debug = True
    app.run(host='0.0.0.0', port= '8000')
