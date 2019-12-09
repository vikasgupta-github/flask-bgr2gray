import os
from flask import Flask, render_template, request, send_from_directory, send_file
from flask_bootstrap import Bootstrap
#import cv2
from PIL import Image

__author__ = 'ibininja'

app = Flask(__name__)
Bootstrap(app)

APP_ROOT = os.path.dirname(os.path.abspath(__file__))

@app.route("/")
def index():
    return render_template("upload.html")

@app.route("/upload", methods=['POST'])
def upload():
    target = os.path.join('static', 'images')
    print(target)

    if not os.path.isdir(target):
        os.mkdir(target)

    for file in request.files.getlist("file"):
        print(file)
        filename = file.filename

        destination = "/".join([target, filename])
        print(destination)
        file.save(destination)
        absPath = os.path.join(APP_ROOT,destination)
        print(absPath)
        # Read image at absPath
        im = Image.open(absPath)
        #im = cv2.imread(absPath)
        # Convert to grayscale
        gray = im.convert('LA')
        #gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)

        outputFile = "/".join([target, 'out_{}'.format(filename) ])
        # Save grayscale image
        gray.save(outputFile)
        #cv2.imwrite(outputFile,gray)

    # return send_from_directory("images", filename, as_attachment=True)
    return render_template("complete.html", input=filename , output=outputFile)

@app.route('/<filename>')
def send_image(filename):
    print(filename)
    return send_from_directory("static/images", filename)

if __name__ == "__main__":
    app.run(port=4555, debug=True)
