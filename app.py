from flask import Flask, flash, request, redirect, url_for, render_template
import os
from werkzeug.utils import secure_filename
from tensorflow import keras
import cv2 as cv
from keras.preprocessing import image

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

UPLOAD_FOLDER = "static/uploads/"

app.secret_key = "secret key"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/upload', methods=['POST'])
def upload():
    if 'file' not in request.files:
        flash('No file part')
        return redirect(request.url)
    file = request.files['file']
    if file.filename == '':
        flash('No image selected for uploading')
        return redirect(request.url)
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        
        model = keras.models.load_model('finalized_model')
        
        #img = image.load_img(os.path.join(app.config['UPLOAD_FOLDER'], filename), target_size = (224,224))
        gray_image = cv.imread(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        gray_image = gray_image / 255
        gray_image = cv.resize(gray_image, (224, 224))
        gray_image = gray_image.reshape(-1, 224, 224, 3)

        classes = ['aphids','armyworm','beetle','bollworm','grasshopper','mites','mosquito','sawfly','stem_borer']
        prediction=model.predict(gray_image)
        a=prediction.reshape(-1)
        list1 = a.tolist()
        list1.index(max(list1))

        return render_template('index.html', filename=filename, output=classes[list1.index(max(list1))])
    else:
        flash('Allowed image types are - png, jpg, jpeg, gif')
        return redirect(request.url)

@app.route('/display/<filename>')
def display_image(filename):
    return redirect(url_for('static', filename='/uploads/' + filename), code=301)

@app.route('/api/upload', methods=['POST'])
def upload_api():
    if 'file' not in request.files:
        flash('No file part')
        return redirect(request.url)
    file = request.files['file']
    if file.filename == '':
        flash('No image selected for uploading')
        return redirect(request.url)
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        
        model = keras.models.load_model('finalized_model')
        
        gray_image = cv.imread(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        gray_image = gray_image / 255
        gray_image = cv.resize(gray_image, (224, 224))
        gray_image = gray_image.reshape(-1, 224, 224, 3)

        classes = ['aphids','armyworm','beetle','bollworm','grasshopper','mites','mosquito','sawfly','stem_borer']
        prediction=model.predict(gray_image)
        a=prediction.reshape(-1)
        list1 = a.tolist()
        list1.index(max(list1))
    else:
        return "INVALID FORMAT"
        
    return classes[list1.index(max(list1))]

if __name__ == "__main__":
    app.run()
