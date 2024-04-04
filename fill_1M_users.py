import mysql.connector
import random
from datetime import datetime, timedelta
import threading

# Function to generate random date of birth
def random_date_of_birth():
    start_date = datetime(1950, 1, 1)
    end_date = datetime(2005, 12, 31)
    random_date = start_date + timedelta(days=random.randint(0, (end_date - start_date).days))
    return random_date.strftime('%Y-%m-%d')

# Function to insert users into the database
def insert_users(thread_id, num_users_per_thread):
    cnx = mysql.connector.connect(user='root', password='example',
                                  host='localhost',
                                  database='Myroslav')
    cursor = cnx.cursor()
    for id in range(num_users_per_thread):
        user_id = thread_id * num_users_per_thread + id
        user_name = 'User' + str(user_id)
        date_of_birth = random_date_of_birth()
        insert_query = "INSERT INTO test_users (user_id, user_name, date_of_birth) VALUES (%s, %s, %s)"
        insert_data = (user_id, user_name, date_of_birth)
        cursor.execute(insert_query, insert_data)

    cnx.commit()
    cursor.close()
    cnx.close()
    print(f"Thread {thread_id} finished inserting {num_users_per_thread} users.")

# Number of users to insert per thread
total_users = 1000000
num_threads = 100
users_per_thread = total_users // num_threads

# Create and start threads
threads = []
for i in range(num_threads):
    thread = threading.Thread(target=insert_users, args=(i+1, users_per_thread))
    threads.append(thread)
    thread.start()

# Wait for all threads to finish
for thread in threads:
    thread.join()


