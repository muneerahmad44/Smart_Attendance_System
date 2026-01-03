1.Run this command "PYTHONPATH=. python3 vector_dbs/create_vector_db.py" to create a vector store and a collection
    Run this commmand PYTHONPATH=. python3 vector_dbs/add_members.py from the smartattendancesystem2 directory to add faculty members 
   -but first update the add_members file according to ur needs 
     - change image path
     - change faculty_id
     - change faculty_meta_data
     - must remembre that ur meta data has to have name,role,deptt and all keys having exact same names as "name","deptt" and "role"
     -then run the command given and you will see a message like "[SUCCESS] Faculty '3' added successfully."
     -remember that same id to be used when add person to the sql database to store attendance data of faculty members 


2.cd to database directory 
  - you must have xampp installed and activated 
    -if linux user use these commands
      - cd  /opt/lampp
      - sudo ./lampp start
  - run the command python3 database.py to create the data base and necssary tables 
  - then to add persons you can run python3 add_faculty_member_to_db.py but ensure you add necessary details inside the script 

3. Run this command from smartattendancesystem2 directory "PYTHONPATH=. streamlit run main.py" 
4. then in the browser click on start camera 
