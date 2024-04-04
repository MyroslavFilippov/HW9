import mysql.connector
import random
from datetime import datetime, timedelta
from flask import Flask

app = Flask(__name__)

# Function to generate random date of birth
def random_date_of_birth():
    start_date = datetime(1950, 1, 1)
    end_date = datetime(2005, 12, 31)
    random_date = start_date + timedelta(days=random.randint(0, (end_date - start_date).days))
    return random_date.strftime('%Y-%m-%d')

# Route to handle the request
@app.route('/insert')
def insert_user():
    cnx = mysql.connector.connect(user='root', password='example',
                                  host='localhost',
                                  database='Myroslav')
    cursor = cnx.cursor(buffered=True)
    user_id = random.randint(1, 1000000)
    user_name = 'User' + str(user_id)
    date_of_birth = random_date_of_birth()
    insert_query = "INSERT INTO test_users (user_id, user_name, date_of_birth) VALUES (%s, %s, %s)"
    insert_data = (user_id, user_name, date_of_birth)
    cursor.execute(insert_query, insert_data)
    cnx.commit()
    cursor.close()
    return "User inserted successfully."

@app.route('/get')
def get_users_count():
    cnx = mysql.connector.connect(user='root', password='example',
                                  host='localhost',
                                  database='Myroslav')
    cursor = cnx.cursor()

    # Define the query to count users
    count_query = "select count(1) from test_users where date_of_birth = '1998-04-27'"

    # Execute the query
    cursor.execute(count_query)

    # Fetch the result
    count = cursor.fetchone()[0]

    # Close cursor and connection
    cursor.close()
    cnx.close()

    return str(count), 200, {'Content-Type': 'text/plain'}

if __name__ == '__main__':
    app.run(debug=False, port=8000)