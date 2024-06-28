from flask import Flask, request, jsonify, send_file
from werkzeug.utils import secure_filename
import os
from flask_cors import CORS, cross_origin
from subprocess import call

from src.pipeline.predict_pipeline import FetchData
from src.pipeline.download_pipeline import Download

app = Flask(__name__)
CORS(app)

# Allowed file extensions for upload
ALLOWED_EXTENSIONS = {'csv'}

# Function to check if a file has an allowed extension
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Route to handle file upload
@app.route('/upload', methods=['POST'])
@cross_origin()
def upload():
    if 'file' not in request.files:
        return {'error': 'No file part'}, 400
    
    file = request.files['file']

    if file.filename == '':
        return {'error': 'No selected file'}, 400

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        new_filename = 'StudentDataset.csv'
        file.save(os.path.join('notebook/data', new_filename))
        
        return {'message': 'Uploaded successfully'}, 200
    else:
        return {'error': 'Invalid file type'}, 400

# Route to receive enrollment number and trigger data processing pipeline
@app.route('/data', methods=['POST'])
@cross_origin()
def datapoint():
    global enr
    data = request.get_json()
    enr = data.get('enrollment')
    if enr is not None:
        call(["python", "src/components/data_ingestion.py", str(enr)])
        call(["python", "src/components/data_preparation.py"])
        call(["python", "src/components/data_transformation.py"])
        call(["python", "src/components/model_trainer.py"])
        return {'message': 'Received successfully'}, 200
    else:
        return {'error': 'Invalid enrollment number'}, 400

# Route to fetch processed data based on enrollment number
@app.route('/fetch_data', methods=['GET'])
@cross_origin()
def fetchdata():
    df, feature_, feature, clusters_, clusters_math, clusters_science, clusters_english = FetchData.fetch()
    
    # Filter data based on enrollment number
    data = df[df["Id"] == float(enr)].to_dict(orient="list")
    for i in feature:
        data[i] = feature[i]

    data["feature_"] = feature_
    data["clusters_"] = clusters_.to_dict(orient="list")
    data["clusters_math"] = clusters_math.to_dict(orient="list")
    data["clusters_science"] = clusters_science.to_dict(orient="list")
    data["clusters_english"] = clusters_english.to_dict(orient="list")

    return jsonify(data)

# Route to download processed data
@app.route('/download_data', methods=['GET'])
@cross_origin()
def download():
    Download.download_data()
    return send_file("artifacts/final_data.xlsx", as_attachment=True)

if __name__ == "__main__":
    app.run(debug=True, port=5000)
