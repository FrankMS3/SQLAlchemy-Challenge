# SQLAlchemy-Challenge

To begin the analysis of climate data from Honolulu, Hawaii:  
First, open and run the script contained within the "climate_starter.ipynb" file (within the SurfsUp folder). This will analyse the dataset files contained within the Resources folder, and output two figures.  
Next, open and run the Flask API contained within the "app.py" file. Check the terminal if you're unsure what address this API is running on. The homepage of this API will contain a list of the available routes, as well as what each route contains. This will run until you use CTRL+C within the app.py file to stop it.  
  
  
The available routes within the app.py API are:  
/api/v1.0/precipitation  
  - Displays precipitation in millimetres for the year leading up to the most recent recorded date (2017-08-23).  
  
/api/v1.0/stations  
  - Displays a list of all stations.  
  
/api/v1.0/tobs  
  - Displays temperatures recorded at the most active station (USC00519281) for the year leading up to the most recent recorded date.  
  
/api/v1.0/<start><end>  
  - Set a start and end date to determine the minimum, average, and maximum temperatures within the chosen timeframe.  
  - Enter start and end dates in the following format:  
    - If only entering a start date: yyyy-mm-dd  
    - If entering both a start and end date: yyyy-mm-dd/yyyy-mm-dd  
  - If an end date is not given, the date range will be from the chosen start date through to the most recent date.  
