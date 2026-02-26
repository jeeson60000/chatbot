<<<<<<< HEAD
from flask import Flask, render_template, request, jsonify
import pandas as pd
import matplotlib.pyplot as plt
import os
import requests  # For Hugging Face API
import torch
import openpyxl

# Initialize Flask app
app = Flask(__name__)

# Get Hugging Face API token from environment or set a default value
HUGGINGFACE_API_TOKEN = os.getenv("HUGGINGFACEHUB_API_TOKEN", "your_huggingface_token")

# Hugging Face model setup
MODEL_NAME = "Salesforce/phi-3"
API_URL = f"https://api-inference.huggingface.co/models/{MODEL_NAME}"
HEADERS = {"Authorization": f"Bearer {HUGGINGFACE_API_TOKEN}"}

# Excel file path and student data loading
EXCEL_PATH = 'students_data.xlsx'
student_data = pd.read_excel(EXCEL_PATH) if os.path.exists(EXCEL_PATH) else None

@app.route('/')
def index():
    return render_template('index.html', excel_loaded=student_data is not None)

@app.route('/upload_excel', methods=['POST'])
def upload_excel():
    file = request.files['file']
    if file and file.filename.endswith('.xlsx'):
        file.save(EXCEL_PATH)
        global student_data
        student_data = pd.read_excel(EXCEL_PATH)
        return "File uploaded and data reloaded successfully!"
    return "Invalid file format. Please upload an Excel file."

@app.route('/academic_support', methods=['POST'])
def academic_support_handler():
    subject = request.form['subject']
    response = requests.post(API_URL, json={"inputs": f"Explain {subject}."}, headers=HEADERS)

    if response.status_code == 200:
        generated_text = response.json()[0]['generated_text']
        return jsonify({'response': generated_text})
    else:
        return jsonify({'response': f"Error: {response.status_code}. {response.json()}"}), 500

@app.route('/excel_query', methods=['POST'])
def excel_query_handler():
    if student_data is None:
        return jsonify({'response': 'No Excel file loaded.'})

    student_id = request.form['student_id']
    column = request.form['column']

    student_row = student_data[student_data['StudentID'] == int(student_id)]
    if not student_row.empty:
        answer = student_row.iloc[0][column]
        return jsonify({'response': f"{column} of student {student_id} is {answer}"})
    else:
        return jsonify({'response': f"No data found for Student ID {student_id}."})

@app.route('/generate_chart', methods=['POST'])
def generate_chart():
    if student_data is None:
        return jsonify({'response': 'No Excel file loaded.'})

    student_id = request.form['student_id']
    column = request.form['column']
    chart_type = request.form['chart_type']  # Chart type from user input

    try:
        student_value = student_data.loc[student_data['StudentID'] == int(student_id), column].values[0]

        plt.figure(figsize=(8, 5))

        # Generate the selected type of chart
        if chart_type == 'bar':
            plt.bar(student_data['StudentID'], student_data[column])
        elif chart_type == 'line':
            plt.plot(student_data['StudentID'], student_data[column], marker='o')
        elif chart_type == 'scatter':
            plt.scatter(student_data['StudentID'], student_data[column])
        else:
            return jsonify({'response': f"Invalid chart type: {chart_type}"})

        plt.axhline(y=student_value, color='r', linestyle='--', label=f'Student {student_id}')
        plt.xlabel('Student ID')
        plt.ylabel(column)
        plt.title(f'{column} Comparison of Student {student_id} with Others')
        plt.legend()

        chart_path = f'static/{student_id}_{column}_{chart_type}_chart.png'
        plt.savefig(chart_path)
        plt.close()

        return jsonify({'chart_url': f'/{chart_path}'})
    except Exception as e:
        return jsonify({'response': str(e)})

if __name__ == '__main__':
    app.run(debug=True)
=======
from flask import Flask, render_template, request, jsonify
import pandas as pd
import matplotlib.pyplot as plt
import os
import requests  # For Hugging Face API
import torch
import openpyxl

# Initialize Flask app
app = Flask(__name__)

# Get Hugging Face API token from environment or set a default value
HUGGINGFACE_API_TOKEN = os.getenv("HUGGINGFACEHUB_API_TOKEN", "your_huggingface_token")

# Hugging Face model setup
MODEL_NAME = "Salesforce/phi-3"
API_URL = f"https://api-inference.huggingface.co/models/{MODEL_NAME}"
HEADERS = {"Authorization": f"Bearer {HUGGINGFACE_API_TOKEN}"}

# Excel file path and student data loading
EXCEL_PATH = 'students_data.xlsx'
student_data = pd.read_excel(EXCEL_PATH) if os.path.exists(EXCEL_PATH) else None

@app.route('/')
def index():
    return render_template('index.html', excel_loaded=student_data is not None)

@app.route('/upload_excel', methods=['POST'])
def upload_excel():
    file = request.files['file']
    if file and file.filename.endswith('.xlsx'):
        file.save(EXCEL_PATH)
        global student_data
        student_data = pd.read_excel(EXCEL_PATH)
        return "File uploaded and data reloaded successfully!"
    return "Invalid file format. Please upload an Excel file."

@app.route('/academic_support', methods=['POST'])
def academic_support_handler():
    subject = request.form['subject']
    response = requests.post(API_URL, json={"inputs": f"Explain {subject}."}, headers=HEADERS)

    if response.status_code == 200:
        generated_text = response.json()[0]['generated_text']
        return jsonify({'response': generated_text})
    else:
        return jsonify({'response': f"Error: {response.status_code}. {response.json()}"}), 500

@app.route('/excel_query', methods=['POST'])
def excel_query_handler():
    if student_data is None:
        return jsonify({'response': 'No Excel file loaded.'})

    student_id = request.form['student_id']
    column = request.form['column']

    student_row = student_data[student_data['StudentID'] == int(student_id)]
    if not student_row.empty:
        answer = student_row.iloc[0][column]
        return jsonify({'response': f"{column} of student {student_id} is {answer}"})
    else:
        return jsonify({'response': f"No data found for Student ID {student_id}."})

@app.route('/generate_chart', methods=['POST'])
def generate_chart():
    if student_data is None:
        return jsonify({'response': 'No Excel file loaded.'})

    student_id = request.form['student_id']
    column = request.form['column']
    chart_type = request.form['chart_type']  # Chart type from user input

    try:
        student_value = student_data.loc[student_data['StudentID'] == int(student_id), column].values[0]

        plt.figure(figsize=(8, 5))

        # Generate the selected type of chart
        if chart_type == 'bar':
            plt.bar(student_data['StudentID'], student_data[column])
        elif chart_type == 'line':
            plt.plot(student_data['StudentID'], student_data[column], marker='o')
        elif chart_type == 'scatter':
            plt.scatter(student_data['StudentID'], student_data[column])
        else:
            return jsonify({'response': f"Invalid chart type: {chart_type}"})

        plt.axhline(y=student_value, color='r', linestyle='--', label=f'Student {student_id}')
        plt.xlabel('Student ID')
        plt.ylabel(column)
        plt.title(f'{column} Comparison of Student {student_id} with Others')
        plt.legend()

        chart_path = f'static/{student_id}_{column}_{chart_type}_chart.png'
        plt.savefig(chart_path)
        plt.close()

        return jsonify({'chart_url': f'/{chart_path}'})
    except Exception as e:
        return jsonify({'response': str(e)})

if __name__ == '__main__':
    app.run(debug=True)
>>>>>>> 28c429086b0dbad715fbefb4fd870fd1f9baacdc
