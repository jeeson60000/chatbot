<<<<<<< HEAD
from flask import Flask, render_template, request, jsonify, url_for
import pandas as pd
import matplotlib.pyplot as plt
import os
import requests

app = Flask(__name__)

# Hugging Face API configuration
HUGGINGFACE_API_TOKEN = "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"
MODEL_NAME = "Salesforce/phi-3"
API_URL = f"https://api-inference.huggingface.co/models/{MODEL_NAME}"
HEADERS = {"Authorization": f"Bearer {HUGGINGFACE_API_TOKEN}"}

# Load Excel data
EXCEL_PATH = 'students_data.xlsx'
student_data = pd.read_excel(EXCEL_PATH) if os.path.exists(EXCEL_PATH) else None

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/academic_support', methods=['GET', 'POST'])
def academic_support():
    if request.method == 'POST':
        subject = request.form.get('subject', '').strip()
        if not subject:
            return jsonify({'response': "Subject cannot be empty."}), 400
        
        response = requests.post(API_URL, json={"inputs": f"Explain {subject}."}, headers=HEADERS)
        if response.status_code == 200:
            return jsonify({'response': response.json()[0]['generated_text']})
        return jsonify({'response': f"Error: {response.status_code}"}), 500
    return render_template('academic_support.html')

@app.route('/excel_query', methods=['GET', 'POST'])
def excel_query():
    if request.method == 'POST':
        student_id = request.form.get('student_id', '').strip()
        column = request.form.get('column', '').strip()

        if student_data is None:
            return jsonify({'response': 'No Excel file loaded.'}), 400

        # Validate student ID and column
        if not student_id.isdigit() or column not in student_data.columns:
            return jsonify({'response': 'Invalid Student ID or Column.'}), 400
        
        student_id = int(student_id)
        student_row = student_data[student_data['StudentID'] == student_id]

        if not student_row.empty:
            answer = student_row.iloc[0][column]
            return jsonify({'response': f"{column} of student {student_id} is {answer}."})
        else:
            return jsonify({'response': f"No data found for Student ID {student_id}."}), 404
    return render_template('excel_query.html')

@app.route('/generate_chart', methods=['GET', 'POST'])
def generate_chart():
    if request.method == 'POST':
        student_id = request.form['student_id']
        column = request.form['column']
        chart_type = request.form['chart_type']

        if student_data is None:
            return jsonify({'response': 'No Excel file loaded.'})

        try:
            # Extract data for plotting
            student_value = student_data.loc[student_data['StudentID'] == int(student_id), column].values[0]
            plt.figure(figsize=(8, 5))

            # Generate the selected type of chart
            if chart_type == 'bar':
                plt.bar(student_data['StudentID'], student_data[column])
            elif chart_type == 'line':
                plt.plot(student_data['StudentID'], student_data[column], marker='o')
            elif chart_type == 'scatter':
                plt.scatter(student_data['StudentID'], student_data[column])
            elif chart_type == 'pie':
                data_values = student_data[column].value_counts()
                labels = data_values.index
                plt.pie(data_values, labels=labels, autopct='%1.1f%%')

            # Add labels and titles where applicable
            if chart_type != 'pie':
                plt.axhline(y=student_value, color='r', linestyle='--', label=f'Student {student_id}')
                plt.xlabel('Student ID')
                plt.ylabel(column)
                plt.title(f'{column} Comparison of Student {student_id} with Others')
                plt.legend()

            # Save the chart to a static path
            chart_path = f'static/{student_id}_{column}_{chart_type}_chart.png'
            plt.savefig(chart_path)
            plt.close()

            return render_template('generate_chart.html', chart_url=f'/{chart_path}', columns=student_data.columns)
        except Exception as e:
            return jsonify({'response': str(e)}), 500

    # On GET request, pass the columns to the template
    columns = student_data.columns if student_data is not None else []
    return render_template('generate_chart.html', columns=columns)

if __name__ == '__main__':
    app.run(debug=True)
=======
from flask import Flask, render_template, request, jsonify, url_for
import pandas as pd
import matplotlib.pyplot as plt
import os
import requests

app = Flask(__name__)

# Hugging Face API configuration
HUGGINGFACE_API_TOKEN = "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"
MODEL_NAME = "Salesforce/phi-3"
API_URL = f"https://api-inference.huggingface.co/models/{MODEL_NAME}"
HEADERS = {"Authorization": f"Bearer {HUGGINGFACE_API_TOKEN}"}

# Load Excel data
EXCEL_PATH = 'students_data.xlsx'
student_data = pd.read_excel(EXCEL_PATH) if os.path.exists(EXCEL_PATH) else None

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/academic_support', methods=['GET', 'POST'])
def academic_support():
    if request.method == 'POST':
        subject = request.form.get('subject', '').strip()
        if not subject:
            return jsonify({'response': "Subject cannot be empty."}), 400
        
        response = requests.post(API_URL, json={"inputs": f"Explain {subject}."}, headers=HEADERS)
        if response.status_code == 200:
            return jsonify({'response': response.json()[0]['generated_text']})
        return jsonify({'response': f"Error: {response.status_code}"}), 500
    return render_template('academic_support.html')

@app.route('/excel_query', methods=['GET', 'POST'])
def excel_query():
    if request.method == 'POST':
        student_id = request.form.get('student_id', '').strip()
        column = request.form.get('column', '').strip()

        if student_data is None:
            return jsonify({'response': 'No Excel file loaded.'}), 400

        # Validate student ID and column
        if not student_id.isdigit() or column not in student_data.columns:
            return jsonify({'response': 'Invalid Student ID or Column.'}), 400
        
        student_id = int(student_id)
        student_row = student_data[student_data['StudentID'] == student_id]

        if not student_row.empty:
            answer = student_row.iloc[0][column]
            return jsonify({'response': f"{column} of student {student_id} is {answer}."})
        else:
            return jsonify({'response': f"No data found for Student ID {student_id}."}), 404
    return render_template('excel_query.html')

@app.route('/generate_chart', methods=['GET', 'POST'])
def generate_chart():
    if request.method == 'POST':
        student_id = request.form['student_id']
        column = request.form['column']
        chart_type = request.form['chart_type']

        if student_data is None:
            return jsonify({'response': 'No Excel file loaded.'})

        try:
            # Extract data for plotting
            student_value = student_data.loc[student_data['StudentID'] == int(student_id), column].values[0]
            plt.figure(figsize=(8, 5))

            # Generate the selected type of chart
            if chart_type == 'bar':
                plt.bar(student_data['StudentID'], student_data[column])
            elif chart_type == 'line':
                plt.plot(student_data['StudentID'], student_data[column], marker='o')
            elif chart_type == 'scatter':
                plt.scatter(student_data['StudentID'], student_data[column])
            elif chart_type == 'pie':
                data_values = student_data[column].value_counts()
                labels = data_values.index
                plt.pie(data_values, labels=labels, autopct='%1.1f%%')

            # Add labels and titles where applicable
            if chart_type != 'pie':
                plt.axhline(y=student_value, color='r', linestyle='--', label=f'Student {student_id}')
                plt.xlabel('Student ID')
                plt.ylabel(column)
                plt.title(f'{column} Comparison of Student {student_id} with Others')
                plt.legend()

            # Save the chart to a static path
            chart_path = f'static/{student_id}_{column}_{chart_type}_chart.png'
            plt.savefig(chart_path)
            plt.close()

            return render_template('generate_chart.html', chart_url=f'/{chart_path}', columns=student_data.columns)
        except Exception as e:
            return jsonify({'response': str(e)}), 500

    # On GET request, pass the columns to the template
    columns = student_data.columns if student_data is not None else []
    return render_template('generate_chart.html', columns=columns)

if __name__ == '__main__':
    app.run(debug=True)
>>>>>>> 28c429086b0dbad715fbefb4fd870fd1f9baacdc
