from flask import Flask, render_template, request, redirect, url_for
from werkzeug.utils import secure_filename
import os
from model import generate_sql_query, perform_data_analysis
from utils.data_loader import load_data

app = Flask(__name__)

# Path to store uploaded data files
UPLOAD_FOLDER = 'data'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# Load sample dataset at start
data = load_data(os.path.join(app.config['UPLOAD_FOLDER'], 'sample_data.csv'))

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return redirect(request.url)
    
    file = request.files['file']
    if file.filename == '':
        return redirect(request.url)

    # Save the uploaded CSV file
    filename = secure_filename(file.filename)
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(file_path)

    # Reload the data
    global data
    data = load_data(file_path)

    return render_template('index.html', message="File uploaded successfully!")

@app.route('/query', methods=['POST'])
def ask_query():
    if 'question' not in request.form:
        return redirect(request.url)

    question = request.form['question']
    
    # Generate the SQL query from the natural language question
    sql_query = generate_sql_query(question, data.columns)
    
    # Perform data analysis and generate visualizations
    result, plot_path = perform_data_analysis(sql_query, data)
    
    return render_template('index.html', query=question, result=result, plot_url=plot_path)

if __name__ == '__main__':
    app.run(debug=True)
