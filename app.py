from flask import Flask, flash, request, redirect, url_for, render_template
import urllib.request
import os
from werkzeug.utils import secure_filename
import cv2
import numpy as np
import glob


app = Flask(__name__)
 
UPLOAD_FOLDER = 'static/uploads'
PROCESSED_FOLDER ='static/processed'
 
app.secret_key = "secret key"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
 
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])
 


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
     


def check_horizontal_and_vertical(image):
    print(image)
    input_image = cv2.imread(image)

    height, width , _ = input_image.shape
    print("height is {} and width is {}".format(height, width))

    if height > width:
        image_orientation = "Potrait"
        return input_image
    
    elif height == width:
        
        image_orientation = "Sqaure"
        return input_image
    
    else:
        image_orientation= "landescape"
        img_rotate_90_clockwise = cv2.rotate(input_image, cv2.ROTATE_90_CLOCKWISE)
        return img_rotate_90_clockwise



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
        from os.path import join, dirname, realpath
        filename = secure_filename(file.filename)
        print(filename)
        
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        filepath = url_for('static', filename='uploads/' + filename)
        
        path_is = dirname(realpath(__file__))+filepath
        processed_image_path = dirname(realpath(__file__)) + "/static/processed/" + filename
        print("processed", processed_image_path)
        
     
        print("path", path_is)
        image_is = check_horizontal_and_vertical(path_is)
        gray = cv2.cvtColor(image_is, cv2.COLOR_BGR2GRAY)
        gray = cv2.bitwise_not(gray)
        thresh = cv2.threshold(gray, 0, 255,
            cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
        coords = np.column_stack(np.where(thresh > 0))
        angle = cv2.minAreaRect(coords)[-1]
        print("computed angle" , angle)
        if angle >-45 and angle<1:
            print("choosen 1st")
            angle = angle
        elif angle > 45:
            angle = 90-angle
            print("choosen 2nd")
        else:
            angle = - angle
            print("chossen 3rd")
        print("choosen angle to rotate" , angle)
        (h, w) = image_is.shape[:2]
        center = (w/2 , h/2 )
        Image_rotation = cv2.getRotationMatrix2D(center, angle, 1.0)

        rotated = cv2.warpAffine(image_is, Image_rotation, (w, h),
            flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)
        cv2.imwrite(processed_image_path, rotated)
       
        flash('Image successfully uploaded and displayed below')
        print("filename is", filename)
     

        return render_template('index.html', filename=filename)
    else:
        flash('Allowed image types are - png, jpg, jpeg, gif')
        return redirect(request.url)
 


@app.route('/display/<filename>')
def display_image(filename):

    return redirect(url_for('static', filename='uploads/' + filename), code=301)


@app.route('/processed/<filename>')
def processed_image(filename):
    url_is = url_for('static', filename='processed/' + filename)
    return render_template('processed.html', filename = filename, url_is = url_is)

if __name__ == "__main__":
    app.run()