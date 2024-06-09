How to run the project

Make a virtual environment of a chosen name
python3 -m venv 'name of virtual env'

Activate it
source 'name of virtual env'/bin/activate

Install requirements
python3 install -r requirements.txt

Create a new database in pgAdmin (preferably named dikureads) and add the following to your .env file (normally
.env should be a private file containing user secrets, in this case we have kept it inside the project files for easy
access for the TAs):
SECRET_KEY=<secret_key>
DB_USERNAME=postgres || <postgres_user_name>
DB_PASSWORD=<postgres_user_password>
DB_NAME=dikureads || <postgres_db_name>

Or use our .env file by creating a database named 'dikureads',
with the user 'brugeren' and the password '12talspigerne'

Run the project:
python3 utils/init_db.py
flask run

The user 'admin' with the password 'admin' will be logged in automatically.
You can review books and add them to book shelves after creating them.
You can search for books on the front page using the search bar.
You can also log 'admin' out and create your own user.
Note new users should be created with a ku-mail as username, i.e xxx###@alumni.ku.dk