# from flask_jwt_extended import jwt_required
from flask import Blueprint, request, jsonify,send_from_directory
import os
from werkzeug.utils import secure_filename

upload = Blueprint("upload", __name__, url_prefix="/upload")


# UPLOAD_FOLDER = '/path/to/the/uploads'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
@upload.post('/')
def upload_file():
    f = request.files['file']

    if f:
        filename = secure_filename(f.filename) # type: ignore
        #check if folder exist or create one
       
        f.save(os.path.join('./static/', filename))
        return jsonify({"message": "File uploaded successfully",
                        "file_url": './static/'+filename,
                        "file_name":filename
                        })
    else:
        return jsonify({'error':'include your file!'}),400
    
    
@upload.get('/<string:name>')
def download_file(name):
    return send_from_directory('./static/', name)