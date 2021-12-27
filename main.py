import mysql.connector
from mysql.connector import Error
import pandas as pd
from datetime import datetime

# SERVER INFORMATION
host = '34.65.198.237'
database = 'store'
user = 'root'
password = 'BrokeBack133'
# -------------------------- #

# connect to database and catch any errors
connection = mysql.connector.connect(host=host, database=database, user=user, password=password)
cursor = connection.cursor()
print("successfully connected to server")


# pushes given data to google cloud SQL server
# humidity: float
# temp: float
# air_quality: float
# light: float
# other: float
def send_sensor_data_to_sensor(humidity, temp, air_quality, light, other):
    query = (
                "INSERT INTO sensor (humidity, temp, air_quality, light, other, entrytime) VALUES (%d, %d, %d, %d, %d, '%s')"
                % (humidity, temp, air_quality, light, other, datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
    try:
        cursor.execute(query)
        connection.commit()
        print("successfully inserted sensor data")
    except mysql.connector.Error as error:
        print("Failed to insert sensor data into database - ERROR: {}".format(error))


# image: path to image (e.g. /Users/jakenoar/Downloads/example.jpeg)
def send_picture_to_images(imagepath):
    query = ("INSERT INTO images (time, picture) VALUES ('%s', LOAD_FILE('%s'))" % (datetime.now().strftime('%Y-%m-%d %H:%M:%S'), imagepath))
    try:
        cursor.execute(query)
        connection.commit()
    except mysql.connector.Error as error:
        print("Failed to insert image into database - ERROR: {}".format(error))


def table_to_dataframe(tablename):
    query = ("select * from %s" % tablename)
    cursor.execute(query)
    frame = pd.DataFrame(cursor.fetchall())
    return frame




# DO SHIT HERE

send_sensor_data_to_sensor(12, 43, 7, 31, 0)
sensorFrame = table_to_dataframe("sensor")
print(sensorFrame)

image = '/Users/jakenoar/PycharmProjects/FoodWaste/fridge-waste images db schema.jpeg'
send_picture_to_images(image)
imageFrame = table_to_dataframe("images")
print(imageFrame)


# STOP DOING SHIT HERE



# after executing query close the connection
if connection.is_connected():
    cursor.close()
    connection.close()

