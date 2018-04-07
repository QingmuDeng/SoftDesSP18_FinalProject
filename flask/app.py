import os
from flask import Flask, request, redirect, url_for, render_template
from werkzeug.utils import secure_filename

app = Flask(__name__)

UPLOAD_FOLDER = os.path.basename('static/uploads/')
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route("/")
def main():
    return render_template('index.html')

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/upload', methods=['POST'])
def upload_file():
    # file = request.file['image']
    # f = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
    #
    # # add your custom code to check that the uploaded file is a valid image and not a malicious file (out-of-scope for this post)
    # file.save(f)
    #
    # return render_template('index.html')

    # if request.method == 'POST':
    #     print ("HELP US 2!!")
    #     # check if the post request has the file part
    #     if 'file' not in request.file:
    #         Flask.flash('No file part')
    #         print ("HELP  3!!")
    #         return redirect(request.url)
    #     file = request.file['btn-primary']
    #     # if user does not select file, browser also
    #     # submit a empty part without filename
    #     if file.filename == '':
    #         Flask.flash('No selected file')
    #         return redirect(request.url)
    #         print ("HELP US KILL US!!")
    #     if file and allowed_file(file.filename):
    #         print ("HELP!!")
    #         filename = Flask.secure_filename(file.filename)
    #         file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    #         return redirect(url_for('uploaded_file',
    #                                 filename=filename))
    # return "file uploaded successfully"
    return "file uploaded successfully"

    if request.method == 'POST':
        f = request.files['file']
        f.save(secure_filename(f.filename))
        return 'file uploaded successfully'


if __name__ == "__main__":
    app.run()