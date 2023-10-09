from flask import Flask, request, jsonify
from flask_cors import CORS
from PIL import Image
from sentence_transformers import SentenceTransformer, util
from transformers import BlipProcessor, BlipForConditionalGeneration
import os
from pymongo import MongoClient
import argparse
import configparser
from werkzeug.utils import secure_filename
app = Flask(__name__)

CORS(app)
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
processorBlipImageCaptioning = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-large")
modelBlipImageCaptioning = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-large")
config_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'config.ini')
config = configparser.ConfigParser()
config.read(config_path)
modelSentenceTransformer = SentenceTransformer("clip-ViT-L-14")
app.config['UPLOAD_FOLDER'] =config.get('General', 'UPLOAD_FOLDER')

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/match', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)),app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
        # Pro   cess the uploaded image
        #raw_image = Image.open(file_path).convert('RGB')
        #encodingsImage = modelSentenceTransformer.encode(raw_image).tolist()
        fileMetaData=process_file(app.config['UPLOAD_FOLDER'], filename)
        ##fileMetaData["claim"]["_id"]=str(fileMetaData["claim"]["_id"])
        return jsonify([{"claim":{"_id":str(fileMetaData["claim"]["_id"]),"filename":filename,"caption":fileMetaData["claim"]["caption"]}}])

    return jsonify({"error": "Invalid file type"}), 400

def find_closest_matches(encoding):
    # This function should perform the aggregation in MongoDB and find claims that have close image encodings

    # Initialize MongoDB
    client = MongoClient(config.get('MongoDB', 'URI'))
    db = client[config.get('MongoDB', 'DATABASE')]
    collection = db[config.get('MongoDB', 'COLLECTION')]
    matched_docs = collection.find({"imageEncodings": {"$near": encoding}}).limit(10)
    # Convert to a list of matched claims for JSON serialization
    return [doc for doc in matched_docs]
def saveEncoding(fileMetaData):
    # Initialize MongoDB
    client = MongoClient(config.get('MongoDB', 'URI'))
    db = client[config.get('MongoDB', 'DATABASE')]
    collection = db[config.get('MongoDB', 'COLLECTION')]    
    collection.insert_one(fileMetaData["claim"])   
    
def process_file(path,filename):
    if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
        full_path = os.path.join(os.path.dirname(os.path.abspath(__file__)),path, filename)
        raw_image = Image.open(full_path).convert('RGB')
        encodingsImage = modelSentenceTransformer.encode(raw_image).tolist()            

        # Use AI to describe Image
        inputs = processorBlipImageCaptioning(raw_image, return_tensors="pt", max_length=60)             
        encodings = modelBlipImageCaptioning.generate(**inputs,max_length= 60)
        generatedCaption = processorBlipImageCaptioning.decode(encodings[0], skip_special_tokens=True)                        
        encodingsCaption = modelSentenceTransformer.encode(generatedCaption).tolist()
        # Convert encodings tensor to a list for storage
        fileMetaData={ "claim":{                             
            "filename": filename,
            "caption": generatedCaption,
            "imageEncodings": encodingsImage,
            "captionEncodings": encodingsCaption
        } }  
    # Store in MongoDB    
    saveEncoding(fileMetaData)
    return fileMetaData

def process_image_directory(path):    
    # Check if path exists and is a directory
    if not os.path.exists(path) or not os.path.isdir(path):
        return "Invalid path"
    for filename in os.listdir(path):
        process_file(path,filename)

@app.route('/process-images', methods=['POST'])
def process_images():
    path = request.json.get('path')
    result = process_image_directory(path)
    if result == "Invalid path":
        return jsonify({"error": "Invalid path"}), 400
    return jsonify({"message": result})


if __name__ == '__main__':    
    parser = argparse.ArgumentParser(description="Process images and store data in MongoDB")
    parser.add_argument('--path', type=str, help="Path to the directory containing images")
    parser.add_argument('--server', action='store_true', help="Run the Flask server")
    args = parser.parse_args()

    if args.path:
        print(process_image_directory(args.path))
    elif args.server:
        app.run(debug=False)
    else:
        print("Please provide either --path or --server argument.")