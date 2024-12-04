import pandas  as pd
from sqlalchemy import create_engine, text
from urllib.parse import quote_plus

# Define your PostgreSQL database credentials
username = 'consultants'
password = 'WelcomeItc@2022'  # password with special character '@'
host = '18.132.73.146'
port = '5432'
database = 'testdb'

# URL-encode the password
encoded_password = quote_plus(password)

# Create the connection string with the encoded password
connection_string = f'postgresql+psycopg2://{username}:{encoded_password}@{host}:{port}/{database}'

# Create the engine
engine = create_engine(connection_string)
#read data from csv load to postgress
#read from postgress load to csv

# Test the connection by executing a simple query
"""with engine.connect() as connection:
    # Use sqlalchemy.text() to wrap the SQL query
    result = connection.execute(text("select * from customer;"))
    # Print the type of the result object
    print(type(result))  # This will show the data type of the result object
    for row in result:
        
        # Print the row and the data types of its columns
        print(row)  # This prints the row itself
        print([type(value) for value in row])  # This prints the data types of each value in the row"""

cust_df=pd.read_sql_query('select * from customer',con=engine) 
print(cust_df)