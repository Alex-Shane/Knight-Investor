from flask import Flask, render_template, request, send_file  # Import flask
import daily_report as dr
import weekly_report as wr
import monthly_report as mr
import os


app = Flask(__name__)  # Setup the flask app by creating an instance of Flask
file_name = ""
downloaded = False

@app.route('/')  # When someone goes to / on the server, execute the following function
def home():
    global downloaded
    if downloaded == True:
        delete_and_handle_pdf()
    return render_template('index.html')  # Return index.html from the static folder

@app.route('/create_report')
def report_page():
    global downloaded
    if downloaded == True:
        delete_and_handle_pdf()
    return render_template('report_page.html')

@app.route('/final_report', methods=['POST'])
def report():
    period = request.form['period']
    exchange = request.form['exchange']
    industry = request.form['industry']
    global file_name
    if period == 'month':
        result = mr.run(exchange, industry)
        context = result[0]
        file_name = result[1]
        return render_template('output_monthly.html', **context)
    elif period == 'week':
        result = wr.run(exchange, industry)
        context = result[0]
        file_name = result[1]
        return render_template('output_weekly.html', **context)
    else:
        result = dr.run(exchange, industry)
        context = result[0]
        file_name = result[1]
        print(file_name)
        return render_template('output_daily.html', **context)

@app.route('/final_report/download', methods=['POST'])
def download():
    global file_name
    temp = File(file_name)
    return send_file(file_name, as_attachment = True)

@app.route('/about')
def about():
    global downloaded 
    if downloaded == True:
        delete_and_handle_pdf()
    return render_template('about.html')

def delete_and_handle_pdf():
    global file_name
    os.remove(file_name)
    global downloaded
    downloaded = False
    file_name = ""

if __name__ == '__main__':  # If the script that was run is this script (we have not been imported)
    app.debug = True
    app.run()  # Start the server