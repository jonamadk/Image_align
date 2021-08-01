from flask import Flask, flash, request, redirect, url_for, render_template
import urllib.request
import os
from werkzeug.utils import secure_filename
from algorithm import *


app = Flask(__name__)
 
UPLOAD_FOLDER = 'static/uploads'
PROCESSED_FOLDER ='static/processed'
 
app.secret_key = "secret key"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
 
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])
 


def allowed_file(filename):
    '''
    specifying allowed filenmae
    '''
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
     

@app.route('/')
def home():
    
    '''
    Homepage route
    
    '''
    return render_template('index.html')
 
@app.route('/', methods=['POST'])
def upload_image():
    '''
    POST request for uploading image file
    
    '''
    if 'file' not in request.files:
        flash('No file part')
        return redirect(request.url)
    file = request.files['file']
    
    if file.filename == '':
        flash('No image selected for uploading')
        return redirect(request.url)
    
    if file and allowed_file(file.filename):
        from os.path import join, dirname, realpath
        filename = secure_filename(file.filename)
        
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        filepath = url_for('static', filename='uploads/' + filename)
        
        path_is = dirname(realpath(__file__))+filepath
        processed_image_path = dirname(realpath(__file__)) + "/static/processed/" + filename
        
        try:
            image_is = correct_image_alignment(path_is)
            cv2.imwrite(processed_image_path, image_is)
            flash('Image successfully uploaded and displayed below')
        
        except:
            print("Error in image translation module")

        return render_template('index.html', filename=filename)
    else:
        flash('Allowed image types are - png, jpg, jpeg, gif')
        return redirect(request.url)
 


@app.route('/display/<filename>')
def display_image(filename):
    
    '''
    Route to display uploaded image
    '''

    return redirect(url_for('static', filename='uploads/' + filename), code=301)


@app.route('/processed/<filename>')
def processed_image(filename):
    
    '''
    Route to display processed image
    '''
    url_is = url_for('static', filename='processed/' + filename)
    return render_template('processed.html', filename = filename, url_is = url_is)

if __name__ == "__main__":
    app.run()