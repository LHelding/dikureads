How to køre projektet

lav et virutal env på maskinen et sted
python3 -m venv 'path til env'

aktiver det
source 'path til env'/bin/activate

installér requirements
python3 install -r requirements.txt

Create a new database in pgAdmin (preferably named dikureads) and add the following to your .env file (normally
.env should be a private file containing user secrets, in this case we have kept it inside the project files for easy
access for the TAs):
SECRET_KEY=<secret_key>
DB_USERNAME=postgres || <postgres_user_name>
DB_PASSWORD=<postgres_user_password>
DB_NAME=dikureads || <postgres_db_name>

køre 
flask run
