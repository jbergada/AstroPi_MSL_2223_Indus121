"""
INS Escola Industrial de Sabadell
Indus121

"""

import time
from orbit import ISS # Geolocate the ISS
from skyfield.api import load # Geolocate the ISS
from picamera import PiCamera 
from datetime import datetime # Calendar time management
import csv
import os # Determine the path in which we are going to save data
from sense_hat import SenseHat

dir_path = os.path.dirname(os.path.realpath(__file__)) # Indicates the path where the file main.py is located (os.path.realpath("main.py"))
sense = SenseHat() # Creates the sense object of the SenseHat() class, sense can use the entire SenseHat() class.

# This function allows get trajectory data from ISS 
def getDataIss():
    t = load.timescale().now() # UTC time
    position = ISS.at(t) # We create the position object
    location = position.subpoint() # From the potition object, we obtain the subpoint() method.
    latitud = location.latitude.degrees
    longitud = location.longitude.degrees
    altura = location.elevation.km
    return latitud, longitud, altura

def getMagnetometer():
    north = sense.get_compass() # We obtain the deviation respect to magnetic north
    raw = sense.get_compass_raw() # Coordinates of the magnetic field vector in uT
    rawX = "{x}".format(**raw) # raw format, unprocessed data
    rawY = "{y}".format(**raw)
    rawZ = "{z}".format(**raw)
    return north, rawX,rawY, rawZ

# Create a csv file
def create_csv_file(data_file1):
    """Create a new CSV file and add the header row"""
    with open(data_file1, 'w') as f: # We use with open, which already closes the file automatically
        writer = csv.writer(f) # In this constructor, f is the path to the file where we write the data
        header = ("Latitude", "Longitude", "Height", "Magnetic North", "RawXMag", "RawYMag", "RawZMag", "TimeUTC")
        writer.writerow(header) 
        
# Fill in the csv with data
def add_csv_data(data_file2, data2):
    """Add a row of data to the data_file CSV"""
    with open(data_file2, 'a') as f:
        writer = csv.writer(f)
        writer.writerow(data2)

RASPCAM_HQRES = (4056,3040)
TMAX_EXPERIMENT = 10
DELAY_TIME = 2
PHOTO_INIT = 2 # We start numbering the photographs from number 2 onwards.
# Data in row n corresponds to photo n
# the first row of the data csv is the header

# Variable to call the camera
camera = PiCamera()
camera.resolution = RASPCAM_HQRES # Sensor resolution, maximum resolution
# timestamp to know how much time our script spends on time
print(datetime.now())

start_time = time.time() # Begin with a counter each second
seconds = TMAX_EXPERIMENT
delay = DELAY_TIME # Time of each data acquisition

time_finish = True
counter_photos = PHOTO_INIT # Counter for the name of the photos, the first picture starts with number 2

camera.start_preview() # Photo display launcher

# Create, open and write the csv file
data_file = dir_path + "/data.csv" # csv file name and path
create_csv_file(data_file) # We call the function to create the file data.csv
    
while time_finish:
    dataLat, dataLong, dataAlt = getDataIss() # Extraction of latitude and longitude data from the ISS
    camera.capture(f"{dir_path}/imagenoir%s.jpg" % counter_photos) # photo capture
    dataMag, dataMagRawX, dataMagRawY, dataMagRawZ = getMagnetometer()
    timeUTC = datetime.now()
    data = (dataLat,dataLong, dataAlt, dataMag, dataMagRawX, dataMagRawY, dataMagRawZ, timeUTC) # We save these 2 data in a variable to pass it to the CSV
    
    add_csv_data(data_file, data)
    # In this line , group all the data in a vector to save them in a csv file
    actually_time = time.time() # time stamp to take into account the number of seconds the device will work
    resume_time = actually_time - start_time
    # If I use time I must write time.sleep
    # If I use from time import sleep I must write --> sleep
    time.sleep(delay) # change depends quantity photos
    counter_photos += 1
    #print(resume_time)
    #print(seconds-delay)
    if(resume_time >= (seconds-delay)): # time stamp to end the script
        time_finish = False
             
camera.stop_preview() # stop the camera
print(datetime.now()) # time stamp to know how much time the scipt spent (approx. 3 hours)