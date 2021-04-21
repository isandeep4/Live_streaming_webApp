# Live_streaming_webApp
A streaming web application developed with FLASK framework.
  - Template building 
  - Authentication with Sessions
  - Integrating with bootstrap
  - Interaction with MySql database
  - Face Detection and recognition
  - Motion detection
  - Email integration using smtp
 
 # How to Run
  - First install requirement.txt
  - Update the sender's email id and receivers's email id in line 15 - 17 in sendemail.py
  - Create a database in MySQL workbench and run the db.sql
  - Update the database information in line 29-32 in webstreaming.py
  - Edit the run configuration of webstreaming.py by providing --ip and --port in the parameter
  - Go to the app's directory and run webstreaming.py
  
 # Details about the web app
  - Please register first with your name, mail id and password
  - After successful registration, please refresh the page and login to the page with the same mail id and password
  - After successful login, you can see the home welcome page with live video showing
  - You can also visit the about and contact page.
  - After 20 movement detection one mail will be sent the the provided receivers email id. Please check the mail in the receiver's mail box
  
 # Train face_recognition model with new images
  - Put a clear image in the project folder.
  - Copy and paste line 40-41 in webstreaming.py to create an face  encoding object
  - Put the object in known_face_encodings array in line 56 of webstreaming.py
  - Put the person's name in the known_face_names array in line 62 of webstreaming.py
