from flask import Flask, render_template, request, send_file, redirect, url_for, flash  # Import flask
from bs4 import BeautifulSoup
import daily_report as dr
import weekly_report as wr
import monthly_report as mr
import searcher as searcher 
import pdfkit
import os


app = Flask(__name__)  # Setup the flask app by creating an instance of Flask
file_name = ""
downloaded = False

@app.route('/')  # When someone goes to / on the server, execute the following function
def home():
    #delete_all_reports()
    return render_template('index.html')  # Return index.html from the static folder

@app.route('/create_report')
def report_page():
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
        stocks = result[2]
        out = render_template('output_monthly.html', stocks = stocks, context = context, industry = industry, file_name = file_name)
        mod_out = strip_unwanted_tags(out)
        # Build PDF from HTML 
        pdf = pdfkit.from_string(mod_out, file_name,options={"enable-local-file-access": ""})
        return render_template('output_monthly.html', stocks = stocks, context = context, industry = industry, file_name = file_name)
    elif period == 'week':
        result = wr.run(exchange, industry)
        context = result[0]
        file_name = result[1]
        winners = result[2]
        losers = result[3]
        out = render_template('output_weekly.html', winners = winners, num_winners = len(winners), losers = losers, context = context, industry = industry, file_name = file_name)
        mod_out = strip_unwanted_tags(out)
        # Build PDF from HTML 
        pdf = pdfkit.from_string(mod_out, file_name,options={"enable-local-file-access": ""})
        return render_template('output_weekly.html', winners = winners, num_winners = len(winners), losers = losers, context = context, industry = industry, file_name = file_name)
    else:
        result = dr.run(exchange, industry)
        context = result[0]
        file_name = result[1]
        winners = result[2]
        losers = result[3]
        out = render_template('output_daily.html', winners = winners, num_winners = len(winners), losers = losers, context = context, industry = industry, file_name = file_name)
        mod_out = strip_unwanted_tags(out)
        # Build PDF from HTML 
        pdf = pdfkit.from_string(mod_out, file_name,options={"enable-local-file-access": ""})
        return render_template('output_daily.html', winners = winners, num_winners = len(winners), losers = losers, context = context, industry = industry, file_name = file_name)


@app.route('/final_report/download/<filename>', methods=['GET'])
def download(filename):
    #global file_name
    # Download the PDF
    return send_file(filename, as_attachment = True)

@app.route('/stock_search')
def search_page():
    return render_template('search.html')

@app.route('/stock_search/', methods=['POST'])
def search():
    query = request.form['query']
    if '/' in query:
        return redirect(url_for('search_page'))
    return redirect(url_for('search_result', ticker = query))

@app.route('/stock_search/<ticker>')
def search_result(ticker):
    info = searcher.getInfo(ticker)
    if info == None:
        return redirect(url_for('search_page'))
    else:
        try:
            name = info['Long Name']
        except:
            name = ticker
        return render_template('search_output.html', info = info, name = name)

@app.route('/about')
def about():
    return render_template('about.html')

def delete_all_reports():
    files = os.listdir(os.getcwd())
    files = [f for f in files if os.path.isfile(os.getcwd()+'/'+f)] #Filtering only the files.
    for file in files:
        if file.endswith('.pdf'):
            os.remove(file)

def strip_unwanted_tags(html_content):
    # Parse the HTML content using BeautifulSoup
    soup = BeautifulSoup(html_content, 'html.parser')

    # Find and remove all <nav> tags
    nav_tags = soup.find_all('nav')
    for nav_tag in nav_tags:
        nav_tag.decompose()  # Remove the <nav> tag from the HTML

    # Find the last <a> tag and remove it along with its contents
    last_a_tag = soup.find_all('a')[-1]
    if last_a_tag:
        last_a_tag.decompose()

    # Get the modified HTML content without the unwanted tags
    modified_html = str(soup)

    return modified_html

if __name__ == '__main__':  # If the script that was run is this script (we have not been imported)
    app.run(host="0.0.0.0", port = 5000)  # Start the server
    #delete_all_reports()
    #app.run(debug = True, port = 5000)