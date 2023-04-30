from flask import Flask, request, jsonify
import tabula
import pandas as pd
import json
import fitz
import pymongo
import os

app = Flask(__name__)

# Set up a MongoDB client and database
client = pymongo.MongoClient("mongodb+srv://mohan585:mohan585@results.5ofnlqg.mongodb.net/?retryWrites=true&w=majority")
db = client["Results"]

# Create a new collection
collection = db["1_2_Supply_2023"]

@app.route('/upload', methods=['POST'])
def upload_file():
    # Clean the upload folder
    if os.path.exists('uploads') and os.listdir('uploads'):
        # If there are files in the folder, delete them
        for filename in os.listdir('uploads'):
            file_path = os.path.join('uploads', filename)
            try:
                os.remove(file_path)
            except Exception as e:
                print(f'Error deleting {file_path}: {e}')
    
    # Check if a file was uploaded
    if 'file' not in request.files:
        return jsonify({'error': 'No file uploaded'})
    
    # Get the uploaded file
    file = request.files['file']
    print(file)
    
    # Check if the file has a PDF extension
    if file.filename.split('.')[-1].lower() != 'pdf':
        return jsonify({'error': 'File must be a PDF'})
    
    file_path = os.path.join('uploads', file.filename)
    file.save(file_path)

    # Open the PDF file using PyMuPDF
    with fitz.open(file_path) as doc:
        # Get the number of pages in the PDF file
        num_pages = doc.page_count
    
    # Set the page number(s) where your table appears
    pages = []
    for i in range(2,num_pages+1):
        pages.append(i)
    pages.append(1)

 

    # Use the read_pdf() method to read the table data from your PDF
    dfs = tabula.read_pdf(file_path, pages=pages, guess = True,stream=True)

    # Concatenate the list of DataFrames into a single DataFrame
    df = pd.concat(dfs)


    # Convert the DataFrame to a JSON string
    json_data = df.to_json(orient='records')

    # Parse the JSON string into a list of dictionaries
    records = json.loads(json_data)

    # Insert the list of records into the collection
    result = collection.insert_many(records)

    # Delete the uploaded file
    os.remove(file_path)
    
    inserted_ids = [str(id) for id in result.inserted_ids]
    return jsonify({'inserted_ids': inserted_ids})

if __name__ == '__main__':
    if not os.path.exists('uploads'):
        os.makedirs('uploads')
    app.run(host='0.0.0.0',debug=True)
