from flask import Flask, render_template, request, redirect, url_for
import os, json
from utils import extract_resume_data, store_data_json, store_data_csv  # NEW

app = Flask(__name__)
# Use absolute paths for Docker
UPLOAD_FOLDER = '/app/resumes'
RESULTS_FOLDER = '/app/results'

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(RESULTS_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/', methods=['GET', 'POST'])
def index():
    data = None
    if request.method == 'POST':
        file = request.files['resume']
        if file and file.filename.endswith('.pdf'):
            path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(path)
            data = extract_resume_data(path)

            # Save per-resume result to separate JSON file (your current logic)
            result_path = os.path.join(RESULTS_FOLDER, file.filename + '.json')
            with open(result_path, 'w') as f:
                json.dump(data, f)

            # Append to long-term data stores
            store_data_json(data)  # appends to resumes_data.json
            store_data_csv(data)   # appends to resumes_data.csv

            return render_template('index.html', data=data, uploaded=True)
    return render_template('index.html', data=data)

@app.route('/results')
def results():
    all_results = []
    try:
        # Check if results directory exists
        if not os.path.exists(RESULTS_FOLDER):
            os.makedirs(RESULTS_FOLDER, exist_ok=True)
            return render_template('results.html', results=[])  # Return empty results if no directory

        # Process each JSON file in results directory
        for file in os.listdir(RESULTS_FOLDER):
            if file.endswith('.json'):
                try:
                    file_path = os.path.join(RESULTS_FOLDER, file)
                    with open(file_path) as f:
                        result = json.load(f)
                        if isinstance(result, dict):  # Ensure we have valid JSON
                            all_results.append(result)
                except (json.JSONDecodeError, IOError) as e:
                    print(f"Error reading {file}: {str(e)}")
                    continue  # Skip invalid files

        return render_template('results.html', results=all_results)
    except Exception as e:
        print(f"Error in results route: {str(e)}")
        return render_template('results.html', results=[], error=str(e))

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
