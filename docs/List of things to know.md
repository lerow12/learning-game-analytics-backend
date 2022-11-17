# Things to note of change
 -The server is not https, needs to be HTTPS for security reasons and to implement certain features. 
 -IP address in the app needs to be changed to server IP, see TODO: Change address.

# How certain things run
Ensure the MySql engine is up and running (Ask OIT about this).
Run create_database.py x y, where x and y is the IP for the MySQL server and your MySQL user. The script will ask you for your password. 
Navigate to src folder, then run this command, replacing 0.0.0.0 with your IP.
<br> uwsgi --http 0.0.0.0:8000 --wsgi-file receiver.py --callable __hug_wsgi__

# What we could not get too
--These are taken from the backlog that did not have anyone assigned to them/ were not done/ did not have any flag next to them
    -Implement Game Collection by PlayerID
    -Create PlayerID
