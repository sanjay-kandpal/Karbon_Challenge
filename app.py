from flask import Flask, render_template, request, redirect, url_for, jsonify
import json
from rules import latest_financial_index, iscr_flag, total_revenue_5cr_flag, borrowing_to_revenue_flag

app = Flask(__name__)
results = {}  # To store the results between pages


# Page 1 - Upload JSON and get results
@app.route('/', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        file = request.files['datafile']
        if file and file.filename.endswith('.json'):
            data = json.load(file)
            financial_index = latest_financial_index(data)
            iscr = iscr_flag(data, financial_index)
            revenue_flag = total_revenue_5cr_flag(data, financial_index)
            borrowing_flag = borrowing_to_revenue_flag(data, financial_index)

    
            global results
            results = {
                'financial_index': financial_index,
                
                'iscr_flag': iscr,
                'revenue_flag': revenue_flag,
                'borrowing_flag': borrowing_flag
            }
            return redirect(url_for('results_page'))

    return render_template('upload.html')

# Page 2 - Display results
@app.route('/results', methods=['GET'])
def results_page():
    global results
    return render_template('results.html', results=results)

if __name__ == '__main__':
    app.run(debug=True)
