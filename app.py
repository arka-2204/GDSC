from flask import Flask, render_template, request
from keras.models import load_model
from keras.preprocessing import image
import numpy as np

app = Flask(__name__)

dic = {0 : 'Cat', 1 : 'Dog'}

model = load_model('mymodel (1).h5')

model.make_predict_function()

def predict_label(img_path):
	i = image.load_img(img_path, target_size=(256,256))
	i = image.img_to_array(i)/255.0
	i = i.reshape(1, 256,256,3)
	p= (model.predict(i) > 0.5).astype("int32")
	#p=model.predict(i) 
	#label=np.argmax(p[0])
	#print(p[0][0])
	return dic[p[0][0]]
#predict_label(img_path)

# routes
@app.route("/", methods=['GET', 'POST'])
def main():
	return render_template("index.html")

@app.route("/submit", methods = ['GET', 'POST'])
def get_output():
	if request.method == 'POST':
		img = request.files['my_image']

		img_path = "static/" + img.filename	
		img.save(img_path)

		p = predict_label(img_path)

	return render_template("index.html", prediction = p, img_path = img_path)


if __name__ =='__main__':
	#app.debug = True
	app.run(debug = True)

