from flask import Flask, render_template, request
import csv
from datetime import datetime

app = Flask(__name__)

valuesToBeStored = {}  # Dictionary to store data

def load_data_from_csv():
    with open("data/data.csv", mode='r', encoding='utf-8-sig') as file:
        reader = csv.DictReader(file)
        for row in reader:
            Student_Roll_no = int(row['Student_Roll_no'])
            valuesToBeStored[Student_Roll_no] = {
                "Student_Roll_no": Student_Roll_no,
                "Name": row['Name'],
                "Gender": row['Gender'],
                "DOB": datetime.strptime(row['DOB'], '%d-%m-%Y'),
                "Father's_Name": row["Father's_Name"],
                "Mother's_Name": row["Mother's_Name"],
                "School_code": int(row['School_code']),
                "English": int(row['English']),
                "English_Grade": row['English_Grade'],
                "Mathematics": int(row['Mathematics']),
                "Mathematics_Grade": row['Mathematics_Grade'],
                "Social_Science": int(row['Social_Science']),
                "Social_Science_Grade": row['Social_Science_Grade'],
                "Hindi": int(row['Hindi']),
                "Hindi_Grade": row['Hindi_Grade'],
                "Science": int(row['Science']),
                "Science_Grade": row['Science_Grade']
            }

load_data_from_csv() 

def search_in_csv(query):
    results = []
    for key, value in valuesToBeStored.items():
        if str(query).lower() == str(value["Student_Roll_no"]).lower():
            results.append(value)
    return results

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search', methods=['GET', 'POST'])
def search():
    if request.method == 'POST':
        query = request.form['query']
        results = search_in_csv(query)
        
        # Split the search results into basic information and subject grades
        basic_info = [{k: v for k, v in result.items() if k in ["Student_Roll_no", "Name", "Gender", "DOB", "Father's_Name", "Mother's_Name", "School_code"]} for result in results]
        subject_grades = [{k: v for k, v in result.items() if k not in ["Student_Roll_no", "Name", "Gender", "DOB", "Father's_Name", "Mother's_Name", "School_code"]} for result in results]

        return render_template('search_results.html', basic_info=basic_info, subject_grades=subject_grades, query=query)
    else:
        return render_template('search_form.html')


if __name__ == '__main__':
    app.run(debug=True)
