import datetime
import os
import psycopg2

from flask import Flask, render_template

app = Flask(__name__)
app.secret_key = os.environ['APP_SECRET_KEY']

@app.route("/", methods=('GET', 'POST'))
def index():
    # Connect to database
    conn = psycopg2.connect(host='db', database=os.environ['POSTGRES_DB'], user=os.environ['POSTGRES_USER'], password=os.environ['POSTGRES_PASSWORD'])
    cur = conn.cursor()

    print('Connected to data base')

    # Get number of all GET requests
    sql_all = """SELECT COUNT(*) FROM weblogs;"""
    cur.execute(sql_all)
    all = cur.fetchone()[0]

    print('count of all GET requests:', all)


    # Get number of all succesful requests
    sql_success = """SELECT COUNT(*) FROM weblogs WHERE status LIKE \'2__\';"""
    cur.execute(sql_success)
    success = cur.fetchone()[0]

    print('count success requests:', success)

    # Get number of all succesful local requests
    sql_success_local = """SELECT COUNT(*) FROM weblogs WHERE status LIKE \'2__\' AND source = 'local';"""
    cur.execute(sql_success_local)
    success_local = cur.fetchone()[0]

    print('count success requests for local:', success_local)

    # Determine rate if there was at least one request
    rate_external = "No entries yet!"
    rate_local = "No entries yet!"
    rate = "No entries yet!"
    if all != 0 :
        rate_external = str(((success-success_local) / (all))*100)
        rate_local = str(((success_local) / all)*100)
        rate = str(((success) / all)*100)

    return render_template('index.html', rate = rate, rate_external = rate_external, rate_local = rate_local)

if __name__ == '__main__':
    app.run(host='0.0.0.0')
