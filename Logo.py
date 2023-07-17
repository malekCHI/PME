from dotenv import load_dotenv
from flask import Blueprint, request, jsonify,send_from_directory
from flask_jwt_extended import jwt_required,  get_jwt_identity
import os
from werkzeug.utils import secure_filename

load_dotenv()

ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}
upload = Blueprint("upload", __name__, url_prefix="/upload")

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
@upload.post('/')
@jwt_required()
def upload_file():
    f = request.files['file']
    user_id = get_jwt_identity()
    
    if f:
        
        filename = secure_filename(f.filename)
        #check if folder exist or create one
        if not os.path.exists(os.getenv("UPLOAD_FOLDER") +str(user_id)+'/'):
            os.makedirs(os.getenv("UPLOAD_FOLDER")+str(user_id)+'/')
        f.save(os.path.join(os.getenv("UPLOAD_FOLDER")+str(user_id)+'/', filename))
        return jsonify({"message": "File uploaded successfully",
                        "file_url": os.getenv("UPLOAD_FOLDER")+str(user_id)+'/'+filename,
                        "file_name":filename
                        })
    else:
        return jsonify({'error':'include your file!'}),400
    
    
@upload.get('/<string:name>')
@jwt_required()
def download_file(name):
    user_id = get_jwt_identity()
    return send_from_directory(os.getenv("UPLOAD_FOLDER")+str(user_id)+'/', name)
