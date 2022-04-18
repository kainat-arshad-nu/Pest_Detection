from flask import Flask, flash, request, redirect, url_for, render_template
import urllib.request
import os
from werkzeug.utils import secure_filename
import pickle

app = Flask(__name__)

UPLOAD_FOLDER = 'static/uploads/'

app.secret_key = "secret key"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/')
def home():
    return render_template('index.html')

@app.route('/', methods=['POST'])
def upload_image():
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
        #print('upload_image filename: ' + filename)
        flash('Image successfully uploaded and displayed below')

        import cv2 as cv
        from keras.preprocessing import image
        uploadedimagepath = "static/uploads/"+filename
        img = image.load_img(uploadedimagepath, target_size = (224,224))
        gray_image = cv.imread(uploadedimagepath)
        gray_image = gray_image / 255
        gray_image = cv.resize(gray_image, (224, 224))
        gray_image = gray_image.reshape(-1, 224, 224, 3)

        classes = ['aphids','armyworm','beetle','bollworm','grasshopper','mites','mosquito','sawfly','stem_borer']
        model = pickle.load(open("model.sav", "rb"))
        prediction=model.predict(gray_image)
        a=prediction.reshape(-1)
        list1 = a.tolist()
        list1.index(max(list1))
        #plt.xticks([])
        #plt.yticks([])
        #plt.imshow(img)
        # print(classes[list1.index(max(list1))])

        return render_template('index.html', filename=filename, output=classes[list1.index(max(list1))])
    else:
        flash('Allowed image types are - png, jpg, jpeg, gif')
        return redirect(request.url)

@app.route('/display/<filename>')
def display_image(filename):
    #print('display_image filename: ' + filename)
    return redirect(url_for('static', filename='uploads/' + filename), code=301)

if __name__ == "__main__":
    app.run()

# q = ""

# @app.route("/")
# def loadPage():
# 	return render_template('index.html', query="")


# @app.route("/predict", methods=['POST'])
# def predict():
    
#     inputQuery1 = request.form['img']
    
#     fn = os.path.basename(inputQuery1)
     
#    # open read and write the file into the server
#     open(fn, 'wb').write(inputQuery1.file.read())

#     output1=fn
#     print(fn)
#     model = pickle.load(open("model.sav", "rb"))
    
    
#     data = [[inputQuery1]]
#     uploadedimagepath = ''

#     img = image.load_img(uploadedimagepath, target_size = (224,224))
#     gray_image = cv.imread(uploadedimagepath)
#     gray_image = gray_image / 255
#     gray_image = cv.resize(gray_image, (224, 224))
#     gray_image = gray_image.reshape(-1, 224, 224, 3)

#     classes = ['aphids','armyworm','beetle','bollworm','grasshopper','mites','mosquito','sawfly','stem_borer']

#     prediction = model.predict(gray_image)
#     a=prediction.reshape(-1)
#     list1 = a.tolist()
#     list1.index(max(list1))
    
#     print()
        
#     return render_template('index.html', output1=classes[list1.index(max(list1))], query1 = inputQuery1)

# if __name__ == "__main__":
#     app.debug = True
#     app.run()