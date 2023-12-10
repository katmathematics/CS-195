# # # #
# Description: Handles the Flask front-end
# # # #

import sys
import inspect
from flask import Flask, redirect, url_for, request, render_template, session
import os
import secrets

import left_brain, right_brain

app = Flask(__name__)
app.secret_key = secrets.token_bytes(32)

@app.route('/', methods=['POST', 'GET'])
def homepage():
    model_output = "Hello user! I am Sesarma. Need any help with anything today?"
    img_filename = os.path.join(app.config['UPLOAD_FOLDER'], right_brain.Emotion(model_output))
    if request.method == 'POST':
        user_input = request.form['nm']
        model_output = left_brain.query(user_input)
        img_filename = os.path.join(app.config['UPLOAD_FOLDER'], right_brain.Emotion(model_output))#right_brain.Feel_Emotion(model_output)
        return render_template("main.html", user_image = img_filename, sesarma_output = model_output)
    return render_template("main.html", user_image = img_filename, sesarma_output = model_output)

PEOPLE_FOLDER = os.path.join('static', 'icons')
app.config['UPLOAD_FOLDER'] = PEOPLE_FOLDER

@app.route('/img')
def show_image():
    img_filename = os.path.join(app.config['UPLOAD_FOLDER'], right_brain.Random_Emotion_From_Dir())
    return render_template("index.html", user_image = img_filename)

if __name__ == "__main__":
    app.run(debug=True)
    