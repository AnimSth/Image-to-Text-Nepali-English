import pymongo,json
from flask import Flask, request, render_template, flash
import cv2, os
import numpy as np
import pytesseract as tess
tess.pytesseract.tesseract_cmd = r'C:\Program Files\tesseract\tesseract'
from werkzeug.utils import secure_filename


app = Flask(__name__)
app.config['SECRET_KEY'] = "tobeornottobe"
client = pymongo.MongoClient()
db = client['langData']

box =[]
fox =[]

def text(data, box ,lan):
    data = cv2.resize(data, None, fx=1.2, fy=1.2,interpolation=cv2.INTER_CUBIC)
    data = cv2.cvtColor(data, cv2.COLOR_BGR2GRAY)
    kernel = np.array([[0, -1, 0],
                   [-1, 5,-1],
                   [0, -1, 0]])         
    data = cv2.filter2D(data, -1, kernel)
    tex = tess.image_to_string(data, lang=lan)
    box.append(tex)

    for i in range(3):
        data = cv2.rotate(data, cv2.ROTATE_90_COUNTERCLOCKWISE)
        tex = tess.image_to_string(data, lang=lan)
        box.append(tex)

with open('database.json','r', encoding='utf-8') as fp:
    ldata = json.load(fp)

@app.route('/')
def home():
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
            lan = 'nep'
            lan1 = 'eng+nep'
            text(data, box, lan)
            text(dataB, fox, lan1)
            tex = max(box, key=len)
            texB = max(fox, key=len)

            if 'नेपाली नागरिकताको' in tex and 'Citizenship Certificate' in texB:
                data={}
                data["front"]=tex
                data["back"]=texB

                prevdata=""
                with open('database.json',encoding='utf-8') as f:
                    d = json.load(f)
                    prevdata=d
                    print(type(d))

                with open('database.json', 'w', encoding='utf-8') as f:
                    prevdata.append(data)
                    json.dump(prevdata, f, ensure_ascii=False, indent=4)
                text= {'front':tex, 'back':texB}

                return render_template('uploads.html',)
            else:
                flash('Please upload a clearer picture')
                return render_template('uploads.html',texB = texB, tex = tex)
        else:
            flash('Please Post first')
            return render_template('uploads.html')
    else:
        return render_template('uploads.html')

if __name__ == "__main__":
    app.debug = True
    app.run(host='0.0.0.0', port= '8000')