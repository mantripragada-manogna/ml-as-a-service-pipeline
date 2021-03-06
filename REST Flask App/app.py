from flask import Flask, render_template, request ,jsonify
import keras, json
import tensorflow as tf
import tensorflow_hub as hub
import os
import h5py as h5
from tensorflow import keras
import ssl
ssl._create_default_https_context = ssl._create_unverified_context
import boto3
import s3fs



#Authenticate the AWS Credentials
s3_client = boto3.client('s3') 



s3_resource = boto3.resource('s3')

s3_fs = s3fs.core.S3FileSystem(anon=False)



model = keras.models.load_model(s3_fs.open(' Output Bucket from ML Pipeline  ', mode='rb'),custom_objects={'KerasLayer':hub.KerasLayer})

app = Flask(__name__)




@app.route('/') # default route
def new():
	result = ""
	return render_template('index.html', result = result) # renders template: index.html with argument result = ""

@app.route('/result', methods = ['POST', 'GET']) # /result route, allowed request methods; POST, and GET
def predict():
	if request.method == 'POST': 
		text = request.get_data(as_text=True)
		result=model.predict([text])
		final =  (result[0][0])
		if final >= 0.5:
			final = 1
		else:
			final = -1
			
		final1 = json.dumps(final)
		return jsonify ({'Sentiment ': final1})
		
	else:
		return render_template('index.html')	
		


if __name__ == '__main__':
	app.run(debug=True, host='0.0.0.0')
    