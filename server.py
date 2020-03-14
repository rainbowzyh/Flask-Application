import os
from flask import Flask, request, redirect, url_for, send_from_directory
from werkzeug.utils import secure_filename
from pymongo import MongoClient
import gridfs
import os

UPLOAD_FOLDER = os.getcwd()c  
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

def connect(name):
    client = MongoClient("127.0.0.1:27017")
    db=client.images
    fs = gridfs.GridFS( db )
    fileID = fs.put( open( name, 'rb')  )
    out = fs.get(fileID)
    print(fileID)
    print(out)


@app.route('/save', methods=['GET', 'POST'])
def upload_file():

	if request.method == 'POST':
        # check if the post request has the file part
		if 'file' not in request.files:
			print('no file')
			return redirect(request.url)
		file = request.files['file']
		if file.filename == '':
			print('no filename')
			return redirect(request.url)
		if file and allowed_file(file.filename):
			filename = secure_filename(file.filename)
			print(1, file)
			print(2, filename)
			# print(os.path.join(app.config['UPLOAD_FOLDER'], filename))
			
			file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
			connect(filename)

			return redirect(url_for('uploaded_file',
                                    filename=filename))
	return '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form action="" method=post enctype=multipart/form-data>
      <p><input type=file name=file>
         <input type=submit value=Upload>
    </form>
    '''


@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'],
                               filename)


if __name__ == "__main__":
    app.run(debug=True)