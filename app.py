from flask import Flask, request, render_template
import pickle
#import cv2 as cv
#from keras.preprocessing import image

app = Flask("__name__")

q = ""

@app.route("/")
def loadPage():
	return render_template('index.html', query="")


@app.route("/predict", methods=['POST'])
def predict():
    
    inputQuery1 = int(request.form['img'])

    model = pickle.load(open("model.sav", "rb"))
    
    
    data = [[inputQuery1]]
    uploadedimagepath = ''

    img = image.load_img(uploadedimagepath, target_size = (224,224))
    gray_image = cv.imread(uploadedimagepath)
    gray_image = gray_image / 255
    gray_image = cv.resize(gray_image, (224, 224))
    gray_image = gray_image.reshape(-1, 224, 224, 3)

    classes = ['aphids','armyworm','beetle','bollworm','grasshopper','mites','mosquito','sawfly','stem_borer']

    prediction = model.predict(gray_image)
    a=prediction.reshape(-1)
    list1 = a.tolist()
    list1.index(max(list1))
    
    print()
        
    return render_template('index.html', output1=classes[list1.index(max(list1))], query1 = inputQuery1)

if __name__ == "__main__":
    app.debug = True
    app.run()