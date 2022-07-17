# Heroku / Flask / PostGres app template

## What is this template for?

As part of our course, we want to build a location-based web application. We know we will need a database to store some data, and that we want special support for geospatial data (latitude and longitude storage, searches based on distance, etc). Eventually we want to deploy our app somewhere!

This teamplate is a guide on how to setup your application. All steps are described on this Readme file.
You can clone / fork this repo to get the contents of some of the files, but otherwise, you will not build directly on top of this, as part of the guide you will create your own Github repo from scratch.

Also, through this guide:

- You setup a Heroku account and can deploy your project there, also from the start.
- You will create a Postgres DB within Heroku, so you do not need to run a DB engine locally on your machine.
- The template includes sample code to show an Esri/ArcGIS Map and some markers in it
- The template also includes a sample model with some prestored locations, just to test out the map functionality and make sure PostGis extension works too.

The idea is you use this to get a first working version of these basic functionalities, and then start changing things to build your own app.

## Disclaimer

The instructions and the commands below were run on an Ubuntu WSL inside Windows 10/11. Then I added the commands for Windows (ran those on Windows 11 Home)
If you are a Windows user, I totally recommend going the WSL route, altough it can be a little messy to setup.
If you are running on a Mac or some different setup, some stuff might be slightly different!

## Prerequisites

Prerequisites
A GitHub account and a personal access token so you can commit stuff from the command line
Git installed in your machine so you can execute git commands
Python installed in your machine so you can execute Python commands and run Pyton scripts. Make sure you have version 3.6 or superior. You also need to use pip, can't remember if that needed to be installed separately.

An Esri Maps API Key (You can get one here: https://developers.arcgis.com/javascript/latest/get-started/#2-get-an-api-key)
Might be needed: A local installation of Postgres: The instructions given here will allow you to connect to the DB hosted in Heroku, even when you are running locally. Regardless, there are a few steps that may not work if you have no local Postgres installed. These are:
the install of dependency psycopg2 (you can workaround this one by installing psycopg2-binary instead)
Connecting to the Heroku db by using heroku pg:psql. To ensure this step will work fine, try executing the command psql from your command line. If the command is found, even when you see some error in connection to server or similar, you are OK. Only if the command is not found / recognized, then you might need to install Postgres / add this to your PATH.


## Initializing the Project

Start by creating a new directory for your new app. You can do it by running these commands:
(I will use 'web-201-heroku-flask-template' as my app name)

**Mac / Linux / Windows**
```
mkdir web-201-heroku-flask-template
cd web-201-heroku-flask-template
```

Create a Python virtual environment:

**Mac / Linux**
```
python3 -m venv venv
source venv/bin/activate
```

**Windows**
You need to figure out [where is your Python executable](https://mothergeo-py.readthedocs.io/en/latest/development/how-to/venv-win.html#where-is-python) first, that for me is (you will at least have to put your own username there instead of mduha): 
```
virtualenv --python C:\Users\mduha\AppData\Local\Programs\Python\Python39\python.exe venv
.\venv\Scripts\activate
```

## Installing Dependencies

We want to get a bunch of libraries to get us started:
(execute these commands one by one in case some error / warning comes)

**Mac / Linux / Windows**
```
pip3 install Flask
pip3 install gunicorn
pip3 install psycopg2 (or: pip3 install psycopg2-binary)
pip3 install Flask-SQLAlchemy
pip3 install Geoalchemy2
pip3 install shapely
pip3 install flask_cors
pip3 install flask_wtf
```

More info about installing Flask can be found on their installation guide: https://flask.palletsprojects.com/en/2.0.x/installation/

We need a way to tell Heroku what are our app dependencies so they get also installed there.
We will use a requirements.txt file for that:

Once we got all the dependencies in our local, we put them into our requirements file:
(we need to be on the root directory of our project so the file gets created there)

**Mac / Linux**
```
python3 -m pip freeze > requirements.txt
```

**Windows**
```
pip freeze > requirements.txt
```

Verify that requirements.txt is created.

:eight_pointed_black_star: If later on you install more libraries on your local virtual env, remember to generate the requirements.txt file again and push that change so the next time you deploy to Heroku it gets installed there as well.

## Writing the initial Application Code

You can copy the code from this template into your project. Files and folders to copy:
(Also at this point it might be easier to open your project folder from VSCode, and start creating and editing files from there)

- static/
- templates/
- app.py
- forms.py
- models.py
- Procfile

## Sync your changes to Github

The best is to setup a git repo and start commiting changes there from the beginning. You will be able to go back to previous versions if needed, and also we will deploy to Heroku what is on the git repo at any given time.

To sync your app project with Github:

1. From the GitHub site / console, create a new empty repository (+ sign next to your uername > New Repository). Note down / copy your repo URL, it will look like *https://github.com/your-username/your-repo-name.git*
2. From your command line, run:

(replace 'https://github.com/mduhagon/web-201-heroku-flask-template.git' with YOUR repo URL from 1.)
(running the commands one by one makes it easier to follow in case something fails)

**Mac / Linux / Windows**
```
git init
echo venv > .gitignore
echo __pycache__ >> .gitignore
git add .gitignore app.py forms.py models.py requirements.txt Procfile
git add static
git add templates
git commit -m "first commit"
git branch -M main
git remote add origin https://github.com/mduhagon/web-201-heroku-flask-template.git <<< replace this
git push -u origin main
```

At this point, if you browse your Git repo via your browser, you will see something like this:

![First version of your repo](/_readme_assets/Repo-first-version.png)

## Setting up the Heroku cli and creating a Heroku app with a Posgres DB

[Setup a Heroku account](https://signup.heroku.com/) if you don't have one already.

The Heroku command-line interface (CLI) is a tool that allows you to create and manage Heroku applications from the terminal. It’s the quickest and the most convenient way to deploy your application.To install the Heroku CLI:

**Mac / Linux**
```
curl https://cli-assets.heroku.com/install.sh | sh 
```
Added notes: Because I get a permission denied error trying to read or change/write/execute a file in my local filesystem, I needed to run the same command with the sudo prefix.The rationale here is that sudo gives me administrator / super user powers to be able to modify all files in my computer. 

**Windows**
Download the cli executable from here: https://devcenter.heroku.com/articles/heroku-cli#install-the-heroku-cli
Install the CLI following the setup steps of the .exe file you downloaded (you can leave all default options suggested).

Next, you have to log in by running the following command:

**Mac / Linux**
(for me the 'heroku' command always needs to be run with sudo, otherwise it fails. You may not need sudo on your local env)
```
sudo heroku login
```

**Windows**
```
heroku login
```

This command promots you to press any key to go login on the browser. Do that.
This opens a website with a button to complete the login process. Click Log In to complete the authentication process and start using the Heroku CLI:

![heroku login browser window](/_readme_assets/Heroku-login.png)

If you were not already logged in Heroku's website, then you will have to enter username and password instead to login now. Once you do either of these,
in your command line interface, the heroku cli should say something like:

```
Logging in... done
Logged in as mduhagon@gmail.com <<< here you see your username, course
```

In order to run any command with the heroku cli to control your apps, deploy, etc, you first need to do the above login step. After a while the authentication expires, so if at some point you run a heroku client command and it starts asking for username / pass, rerun the login command and you should be back in business.

Now we will create a new app inside your Heroku account. For that you need a unique name. I chose 'mduhagon-web-201-heroku-flask' for mine. Wherever you see this name in my commands, replace it with **your app name**.

To create the app, run:

**Mac / Linux / Windows**
(might need to add sudo for Mac/Linux)
```
heroku create mduhagon-web-201-heroku-flask
```

if it works, you will see an output like this:

```
Creating ⬢ mduhagon-web-201-heroku-flask... done
https://mduhagon-web-201-heroku-flask.herokuapp.com/ | https://git.heroku.com/mduhagon-web-201-heroku-flask.git
```

Now, we want to add a PostGres database to our app (hobby-dev is the free version):

**Mac / Linux / Windows**
(might need to add sudo for Mac/Linux)
```
heroku addons:create heroku-postgresql:hobby-dev
```


You should see an output similar to this:

```
Creating heroku-postgresql:hobby-dev on ⬢ mduhagon-web-201-heroku-flask... free
Database has been created and is available
 ! This database is empty. If upgrading, you can transfer
 ! data from another database with pg:copy
Created postgresql-parallel-63698 as DATABASE_URL
Use heroku addons:docs heroku-postgresql to view documentation
```

As the last step in setting up our database, we want to install PostGis, the extendion library to deal with geolocated data.
To be able to do this we need our database name, in my example that is 'postgresql-parallel-63698' (notice that is mentioned on the output when we created the db, otherwise you can see the db name from the Heroku web console)

**Mac / Linux / Windows**
(might need to add sudo for Mac/Linux)
```
heroku pg:psql postgresql-parallel-63698  <<< replace with your db name
```

If you see this error, you will need to install / troubleshoot installation for Postgres:

```
--> Connecting to postgresql-trapezoidal-55663
 !    The local psql command could not be located. For help installing psql, see
 !    https://devcenter.heroku.com/articles/heroku-postgresql#local-setup
```
For windows: 
- [Install Postgress via executable](https://www.enterprisedb.com/downloads/postgres-postgresql-downloads) The latest version / 14.x is OK.
- If you re-open your Porwershell window, type `psql`, and still see an error that says `psql : The term 'psql' is not recognized as ....` you need to add this to your PATH by running this command (Assuming you installed Postgres version 14):

```
$env:Path += ";C:\Program Files\PostgreSQL\14\bin"
```
Now you should be ready to try again:
```
heroku pg:psql postgresql-parallel-63698  <<< replace with your db name
```

Added note: my database name =  postgresql-shallow-84563

Once the `pg:sql` command works, you will find yourself 'inside' a psql command line where you can run commands against your database. Run the following:

```
CREATE EXTENSION postgis;
```

You should see the following output if the install went fine:

```
CREATE EXTENSION
```

Use 'exit' to get out of the db command line.

At this point you have an app, and a database in Heroku, but they are empty. You can look a bit around what you have created by using the [Heroku dashboard](https://devcenter.heroku.com/articles/heroku-dashboard):

https://dashboard.heroku.com/

Next steps are making sure your app runs locally, then deploying it for the first time to Heroku:

## Running the app locally

First, you want to get the app running locally, because if something did not work, it is easier to see what the issue is on your own machine than it is to do many Heroku deploys for each problem. This will continue to be true as you make changes and develop new features, you first run them locally and when they work, you will deploy an update to Heroku.

To run the sample code you copied from this template, two environment variables need to be set:

- DATABASE_URL: this is the connection string for the PostGres database. Because the DB is hosted by Heroku, it also defines the user / password / etc for us. And these are 'ephemeral' credentials that heroku will rotate periodically to make your db more secure. We don't know how often the credentials change, but we should assume they will, so no hardcoding these anywhere. To get the proper value you can use the heroku cli, and below you get a bit of command line magic to directly put that into a local env variable.
- MAPS_API_KEY: You need to get this for yourself (via the Esri developer console). It will be sent to the Maps API to render the map on the initial page of the sample app and any place where a map is used.


To get the data you need to set DATABASE_URL, run:

**Mac / Linux / Windows**
```
heroku pg:credentials:url postgresql-parallel-63698 <<<< replace this with YOUR database name from previous steps
```
Added note: my database name = postgresql-shallow-84563

This will output something like this:

```
Connection information for default credential.
Connection info string:
   "dbname=xxxxxxxxxxxxxx host=ec2-XXX-XXX-XXX-XXX.compute-X.amazonaws.com port=XXXX user=XXXXXXX password=XXXXXXXXXXXXXX sslmode=XXXXXX"
Connection URL:
   postgres://XXXXXXX:YYYYYYYYYYYYYYYYYYYYYYY@ec2-XXX-XXX-XXX-XXX.compute-X.amazonaws.com:XXXX/XXXXXXXXXXXXXXX
```

    #####
Added note: Output in my terminal:

Connection information for default credential.
Connection info string:
   "dbname=d3l0e2vbigq9mf host=ec2-34-233-115-14.compute-1.amazonaws.com port=5432 user=vbmiemmukbxdln password=79dceec5c1ffdebe87534fd8d9d22df925e3ed27e42f616f1ef73312604f31f6 sslmode=require"
Connection URL:
   postgres://vbmiemmukbxdln:79dceec5c1ffdebe87534fd8d9d22df925e3ed27e42f616f1ef73312604f31f6@ec2-34-233-115-14.compute-1.amazonaws.com:5432/d3l0e2vbigq9mf

   ###

What we want to set as `DATABASE_URL` is the value shown as Connection URL, that starts with 'postgres://'
You can copy that value from the output and use it to set the variable. 

To set the environment variables run:

**Mac / Linux**
```
export DATABASE_URL=postgres://XXXXXXX:YYYYYYYYYYYYYYYYYYYYYYY@ec2-XXX-XXX-XXX-XXX.compute-X.amazonaws.com:XXXX/XXXXXXXXXXXXXXX <<< replace this with your string from above
export MAPS_API_KEY=ssdfsdfsAAqfdfsuincswdfgcxhmmjzdfgsevfh  <<<<< replace this with your API key
```
Added note: I don't need to do these 2 steps anymore, because I added the DATABASE_URL and MAPS_API_KEY in the luanch.json file 

Windows / Option 1

SET DATABASE_URL=postgres://XXXXXXX:YYYYYYYYYYYYYYYYYYYYYYY@ec2-XXX-XXX-XXX-XXX.compute-X.amazonaws.com:XXXX/XXXXXXXXXXXXXXX <<< replace this with your string from above
SET MAPS_API_KEY=ssdfsdfsAAqfdfsuincswdfgcxhmmjzdfgsevfh  <<<<< replace this with your API key
Windows / Option 2 (In the PowerShell the above commands were not really working, echo %DATABASE_URL% returned just %DATABASE_URL% which is not OK, and the bellow commands worked )

$env:DATABASE_URL = "postgres://XXXXXXX:YYYYYYYYYYYYYYYYYYYYYYY@ec2-XXX-XXX-XXX-XXX.compute-X.amazonaws.com:XXXX/XXXXXXXXXXXXXXX" <<< replace this with your string from above
$env:MAPS_API_KEY = "ssdfsdfsAAqfdfsuincswdfgcxhmmjzdfgsevfh" <<<<< replace this with your API key
✴️ The environment variables you are setting now only 'exist' for as long as you keep the terminal / Powershell session open. When you close it and start again, the variables are gone, and you have to set them again! So you will do this step every time you start working on your app.

!!!!!! The value for MAPS_API_KEY in my sample is just a dummy value, you need to get the real api key value from your Esri developer console and use that value instead. Remember never to commit this API key to your repo because that is public and the key could get exploited / used by other people. --> DON'T ADD KEY TO README.md OR ANY OTHER FILE IN TEH REPO!!!!!!!

If you want to verify the values of the env variables, use:

Mac / Linux

echo $DATABASE_URL / heroku config:get DATABASE_URL -a mahu4-myfirstapp-heroku-flask
echo $MAPS_API_KEY
Windows / Option 1

echo %DATABASE_URL%
echo %MAPS_API_KEY%
Windows / Option 2

$env:DATABASE_URL
$env:MAPS_API_KEY
Finally, to run the app:

**Mac / Linux / Windows **

flask run
You should see something like this on the output of the console:

 * Environment: production
   WARNING: This is a development server. Do not use it in a production deployment.
   Use a production WSGI server instead.
 * Debug mode: off
 * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
If you access http://127.0.0.1:5000/ or http://localhost:5000/ you should see:

sample app

Bonus: during development, you normally want to reload your application automatically whenever you make a change to it. You can do this by passing an environment variable, FLASK_ENV=development, to flask run:

FLASK_ENV=development flask run
You can also run your app locally from VSCode in debug mode, following the setup steps we did in https://github.com/FrauenLoop-Berlin/web201-summer2022-helloFlask

Use Ctrl+C to quit / shut down the flask app.

Deploying the app to Heroku
Now that you verified the app runs locally, you can deploy it to Heroku!

Make sure you do not have any local changes not commited to main branch at this point:

**Mac / Linux / Windows **

git status
Should only show local files that are not meant to be commited like __pycache__/ (you do not need to commit this directory ever, you can add it to .gitignore later)

On branch main
Your branch is ahead of 'origin/main' by 1 commit.
  (use "git push" to publish your local commits)

Untracked files:
  (use "git add <file>..." to include in what will be committed)
        __pycache__/

nothing added to commit but untracked files present (use "git add" to track)
If there are other things, add them and push them to main.

git add XXXXX
git commit -m "Some more changes"
git push
Now all your code is up-to-date with GitHub. This is important because you push to Heroku whatever is in the main branch of your repo.

Before deploy, a small extra step. Remember we need 2 environment variables for the sample code to work. DATABASE_URL is by default provided by Heroku because we have a DB attached to our app. The second env variable is something we define, so we need to set it manually as a Heroku config variable:

Mac / Linux / Windows

heroku config:set MAPS_API_KEY=ssdfsdfsAAqfdfsuincswdfgcxhmmjzdfgsevfh <<<<< replace this with your API key
Now all is ready. To deploy that current state of your main branch into your Heroku app, run:

**Mac / Linux / Window **

git push heroku main
This will output a lot of things as heroku installs all components. By the end if all is OK you will see the URL of your launched app:

remote: -----> Launching...
remote:        Released v5
remote:        https://mduhagon-web-201-heroku-delete.herokuapp.com/ deployed to Heroku
remote:
remote: Verifying deploy... done.
If all went well, your sample app is now running in Heroku as well! Check the provided URL to verify.


Added note: installation worked until here. There is a notification to upgrade the stack from Heroku-18 to Heroku-20. The instructions to do that:  https://devcenter.heroku.com/articles/upgrading-to-the-latest-stack . Still not done. 

What now?
The sample code has some useful functionality: it is taking the database connection string from the already set Heroku env variable, it is using another config variable for the Esri Maps key so that is not hardcoded in your source code (because the API key cannot be commited to GitHub!). It is also storing some sample data with lat / long and querying for it when you zoom / reposition the map. You can take a closer look at all this, so you then decide how to extend it.

You will keep making changes to the app, adding the functionality of your project. Everything in the template is just a sample, you can change / remove things as you wish. Each time you have some new functionality working commit it to GitHub, and then to Heroku, so you make sure it works there as well.

In a nutshell, this process will look like this:

Use git status to see all the files you added or changed:
git status
Use git add to stage all the above changes that should go to your repo (you may need to do this for multiple paths or you can also list many together)
git add xxxxx
Commit the changes and push to GitHub
git commit -m "a short description of your changes so others know what you did / is also a future reference for yourself"
git push
Deploy the changes to Heroku:
heroku login
git push heroku main
Happy coding!

Footer
© 2022 GitHub, Inc.
Footer navigation
Terms
Privacy
Security
Status
Docs
Contact GitHub
Pricing
API
Training
Blog
About

### END OF MENTOR'S INSTRUCTION ###

## ADDITIONAL INSTRUCTIONS:
# How to run your app using a VSCode launch configuration 
# Adding API key to launch.json file

You probably started creating your project and executing the commands in the tutorial / template readme in a command line window. At some point, it is very useful to open the project folder you created in VSCode, so you can start editing all files from there.
In VSCode you have a terminal, so you can still execute commands from there as you were doing before. For example flask run  to start the app.
There might be some issues with this method:
- You want to start the app in debug / developer mode so the changes you make to code are picked up while the app is running
- You want to quickly / more easily set up your environment variables and activate your virtual environment
- You want to be able to put breakpoints on the python code of your app to do debugging

For all these things, setting up a launch configuration helps:
Open your project folder in VSCode (File > Open Folder...) I chose C:\Users\mduha\esri-project-windows because that is the folder I created for my latest app.

The project already contains a venv folder (I created it via the commands in the readme) If you do not have one yet go check those commands in the readme and execute them inside your folder (you can use the terminal in VSCode if you like)

On the File explorer column on the left, select / click the app.py file. This is the 'entry point' to our app so when we select it VSCode will pick up that on launch, this is the file that should be used (Image 1 for ref)
Then on the left sidebar you click on the Button for 'Run & Debug' (it has a play symbol and a bug on top). This will change what you see on the left nav bar, and there you get a link to 'create a launch.json file'. Click on that. A dropdown with app types appears in the center, choose Flask there.
The file will be created inside a folder called .vscode, search for that using the file explorer in VSCode

The content of the json might be different depending on your OS. What we want to do there is to add our environment variables to a 'section' called 'env' (if you do not have it you can add env to the json). These are the vars I added (you need to set your own database url and api keys and if you use Google maps the 2nd variable is called GOOGLE_MAPS_API_KEY):

"DATABASE_URL": "postgres://gvxxvvxcjouzqd:ac317aff5d58a9c1b3878ef2cc78878a3ff464e954b629026d4e4191a5ed9636@ec2-23-23-151-191.compute-1.amazonaws.com:5432/du55etnidh3mg", 

"MAPS_API_KEY": "AAPK0825debdbc3346ea9e40eda283343c6dX8eO4LmGV3COs9-HVKnd7srzQqXIETVun2s1eIRqBMfWdILRx9TieRgHk6O81a7R"

Once you added these lines to launch.json and saved the file you can run / start your app using the green run/play button on VSCode 'Run & Debug' panel.


CODE SNIPPETS FOR REGISTRATION AND LOGIN OF USERS (steps 1 to 5)

Whats the goal?
to implement user registration and login functionalities for our app! As a prerequisite, you have your app running at least locally. If it runs on Heroku even better, that's the ideal, but if you got stuck there somehow you can still get started with this part.

High level overview of what we want to do
If we are going to have users in our app, we need to store them somewhere. We are using our Postgres Database (DB) instance to store our map locations, and we can also store our users there. We need to create a model class that will represent the user, this is:

will hold all data attributes that a user should have:

name
email (We use this one usually because it is unique, names can repeat so they aren't unique)
password (to log in)
address? (let's not ask for user data if we do not need it later for something in our app)
other attributes that make sense for your app use case! (you can add these to the user class structure provided)
the user class might also have some logic: methods that perform some task that makes sense to be done by the user class. For example:

validations
storing the user to the DB, etc.
Once we have a User model class, we will implement two forms:

Registration (it allows to create new users in the DB)
Login (it allows to start a session for an existing usre in the DB)
Finally, we will make the 'New location' functionality that comes in the template be only possible for logged-in users, and when a new location is created we will 'link it' or relate it to the user that created it. So we can say each location now 'belongs' to a user of the site.

For all this, we will use a Flask extension called flask_login. It will take care of some of the heavy lifting involved with maintaining a user session on our app

Step 1 - Install new flask_login dependency
remember to do this within your venv / while your venv is activated:

pip3 install flask_login
pip3 install email_validator
Update your requirements.txt file (you can use pip freeze or add this dependency by hand):

Mac / Linux

python3 -m pip freeze > requirements.txt
Windows

pip freeze > requirements.txt
In the end the lines added to requirements.txt should be:

Flask-Login==0.6.1
dnspython==2.2.1
email-validator==1.2.1
idna==3.3
(actual version numbers might change over time)

Step 2 - Create the User class
The class is added to your models.py file:

class User(UserMixin, db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(200), nullable=False) # i.e Hanna Barbera
    display_name = db.Column(db.String(20), unique=True, nullable=False) # i.e hanna_25
    email = db.Column(db.String(120), unique=True, nullable=False) # i.e hanna@hanna-barbera.com
    password = db.Column(db.String(32), nullable=False) 
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    @classmethod
    def get_by_id(cls, user_id):
        return cls.query.filter_by(id=user_id).first()
        
    def __repr__(self):
        return f"User({self.id}, '{self.display_name}', '{self.email}')"      

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def update(self):
        db.session.commit()   
To make some references work you need to add the following to the imports ection on the top of the file:

from flask_login import UserMixin
from datetime import datetime
At this point you need to start your app locally, and force a re-creation of your DB. You do that by un-commenting the method db_drop_and_create_all() that is in app.py

Then start your app (in any form you are doing it by now / ie. by command line / with VSCode run, etc):

flask run
At this point it can be a good idea to take a look at your database with DBeaver or a similar editor, or the SQL command line client, and verify a new table was created. (TODO: make a step-by-step guide for this)

Once the Flask app started and the DB is recreated you can comment back the method db_drop_and_create_all(). If you do more changes later, for example add some attribute for the User class, modify the SampleLocation class, etc. You need to do this procedure of executing db_drop_and_create_all() again, otherwise the changes will not be 'impacted into' or executed in the DB.

Step 3 - Create a registration Form and page
Content for the Registration form class (you add it to forms.py):

class RegistrationForm(FlaskForm):
    fullname = StringField(
        'Full Name', 
        validators=
            [DataRequired(), 
            Length(min=2, max=200)
        ]
    )

    username = StringField(
        'Username / Display Name', 
        validators=
            [DataRequired(), 
            Length(min=2, max=20)
        ]
    )

    email = StringField(
        'Email',
        validators=[
            DataRequired(), 
            Email()
        ]
    )

    password = PasswordField(
        'Password',
        validators=[
            DataRequired()
        ]
    )

    confirm_password = PasswordField(
        'Confirm Password',
        validators=[
            DataRequired(),
            EqualTo('password')
        ]
    )

    submit = SubmitField('Sign up')  

You need to modify existing import lines to add a few more imports:

from wtforms import StringField, SubmitField, HiddenField, PasswordField
from wtforms.validators import DataRequired, Length, Email, EqualTo
You need a new template file, called registration.html:

{% extends "layout.html" %}
{% block body %}
<div id="container">
    {% for field, errors in form.errors.items() %}
    <div class="alert alert-error">
        {{ form[field].label }}: {{ ', '.join(errors) }}
    </div>
    {% endfor %}
    <div class="content-section">
        <form method="POST" action="">
            {{ form.hidden_tag() }}
            <fieldset class="form-group">
                <legend class="border-bottom mb-4">Join Today</legend>
                <div class="form-group">
                    {{ form.fullname.label(class="form-control-label") }}  
                    {% if form.fullname.errors %}
                        {{ form.fullname(class="form-control form-control-lg is-invalid") }} 
                        <div class="invalid-feedback">
                            {% for error in form.fullname.errors %}
                                <span>{{ error }}</span>
                            {% endfor %}
                        </div>  
                    {% else %}    
                        {{ form.fullname(class="form-control form-control-lg") }} 
                    {% endif %}
                </div>
                <div class="form-group">
                    {{ form.username.label(class="form-control-label") }}  
                    {% if form.username.errors %}
                        {{ form.username(class="form-control form-control-lg is-invalid") }} 
                        <div class="invalid-feedback">
                            {% for error in form.username.errors %}
                                <span>{{ error }}</span>
                            {% endfor %}
                        </div>  
                    {% else %}    
                        {{ form.username(class="form-control form-control-lg") }} 
                    {% endif %}
                </div>
                <div class="form-group">
                    {{ form.email.label(class="form-control-label") }}    
                    {% if form.email.errors %}
                    {{ form.email(class="form-control form-control-lg is-invalid") }}
                        <div class="invalid-feedback">
                            {% for error in form.email.errors %}
                                <span>{{ error }}</span>
                            {% endfor %}
                        </div>  
                    {% else %}    
                        {{ form.email(class="form-control form-control-lg") }}
                    {% endif %} 
                </div>  
                <div class="form-group">
                    {{ form.password.label(class="form-control-label") }}      
                    {% if form.password.errors %}
                        {{ form.password(class="form-control form-control-lg is-invalid") }} 
                        <div class="invalid-feedback">
                            {% for error in form.password.errors %}
                                <span>{{ error }}</span>
                            {% endfor %}
                        </div>  
                    {% else %}    
                        {{ form.password(class="form-control form-control-lg") }} 
                    {% endif %}
                </div>    
                <div class="form-group">
                    {{ form.confirm_password.label(class="form-control-label") }}    
                      
                    {% if form.confirm_password.errors %}
                        {{ form.confirm_password(class="form-control form-control-lg is-invalid") }} 
                        <div class="invalid-feedback">
                            {% for error in form.confirm_password.errors %}
                                <span>{{ error }}</span>
                            {% endfor %}
                        </div>  
                    {% else %}    
                        {{ form.confirm_password(class="form-control form-control-lg") }} 
                    {% endif %}
                </div>            
            </fieldset>
            <div class="form-group">
                {{ form.submit(class='btn btn-outline-info')}}    
            </div>
        </form>
    </div>
    <div class="border-top pt-3">
        <small class="text-muted">
            Already have an account? <a class="ml-2" href="{{ url_for('login')}}">login</a>
        </small>
    </div>
</div>    
{% endblock body %}
You need to add the code to handle this new registration page / route in your app.py: (add this at the end of all other routes in app.py)

   @app.route("/register", methods=['GET', 'POST'])
    def register():
        # Sanity check: if the user is already authenticated then go back to home page
        # if current_user.is_authenticated:
        #     return redirect(url_for('home'))

        # Otherwise process the RegistrationForm from request (if it came)
        form = RegistrationForm()
        if form.validate_on_submit():
            # hash user password, create user and store it in database
            hashed_password = hashlib.md5(form.password.data.encode()).hexdigest()
            user = User(
                full_name=form.fullname.data,
                display_name=form.username.data, 
                email=form.email.data, 
                password=hashed_password)

            try:
                user.insert()
                flash(f'Account created for: {form.username.data}!', 'success')
                return redirect(url_for('home'))
            except IntegrityError as e:
                flash(f'Could not register! The entered username or email might be already taken', 'danger')
                print('IntegrityError when trying to store new user')
                # db.session.rollback()
            
        return render_template('registration.html', form=form)   
Update 1: Because th registration.html is making reference to url_for('login') we need to create at least a stub of this route, so the call in the registration template works. We can add an empty route for now, that will be replaced with the complete implementation in the next step:

(add it after the route for register):

    @app.route("/login", methods=['GET', 'POST'])
    def login():
        pass

Some stuff needs to be added to the imports of app.py:

from forms import RegistrationForm
from models import User
from sqlalchemy.exc import IntegrityError
import hashlib
With these bits you can hit /register on your browser against your running app and try out the registration page. We do not have a link to register from the site yet, but we will add it later, maybe to the navigation bar in the home page.

Try out your form, what happens if you do not fill all fields? Can you register a user when entering all correct values?

Step 4 - Create a login Form and page
Content for the Login form class (you add it to forms.py):

class LoginForm(FlaskForm):
    username = StringField(
        'Username / Display Name',
        validators=[
            DataRequired()
        ]
    )

    password = PasswordField(
        'Password',
        validators=[
            DataRequired()
        ]
    )

    remember = BooleanField('Remember me')

    submit = SubmitField('Login')    
Some additional imports are needed in forms.py now (BooleanField is the new thing):

from wtforms import StringField, SubmitField, HiddenField, PasswordField, BooleanField
You need a new template file, called login.html:

{% extends "layout.html" %}
{% block body %}
<div id="container">
    <div class="content-section">
        <form method="POST" action="">
            {{ form.hidden_tag() }}
            <fieldset class="form-group">
                <legend class="border-bottom mb-4">Login</legend>
                <div class="form-group">
                    {{ form.username.label(class="form-control-label") }}    
                    {% if form.username.errors %}
                    {{ form.username(class="form-control form-control-lg is-invalid") }}
                        <div class="invalid-feedback">
                            {% for error in form.username.errors %}
                                <span>{{ error }}</span>
                            {% endfor %}
                        </div>  
                    {% else %}    
                        {{ form.username(class="form-control form-control-lg") }}
                    {% endif %} 
                </div>  
                <div class="form-group">
                    {{ form.password.label(class="form-control-label") }}      
                    {% if form.password.errors %}
                        {{ form.password(class="form-control form-control-lg is-invalid") }} 
                        <div class="invalid-feedback">
                            {% for error in form.password.errors %}
                                <span>{{ error }}</span>
                            {% endfor %}
                        </div>  
                    {% else %}    
                        {{ form.password(class="form-control form-control-lg") }} 
                    {% endif %}
                </div>      
                <div class="form-check">
                    {{ form.remember(class="form-check-input") }}
                    {{ form.remember.label(class="form-check-label") }}
                </div>       
                <small class="text-muted ml-2">
                    <a href="#">Forgot password?</a>
                </small>
            </fieldset>
            <div class="form-group">
                {{ form.submit(class='btn btn-outline-info')}}    
            </div>
        </form>
    </div>
    <div class="border-top pt-3">
        <small class="text-muted">
            You do not have an account? <a class="ml-2" href="{{ url_for('register')}}">Register</a>
        </small>
    </div>
</div>    
{% endblock body %}
You need to add the code to handle the login, and also the loading of an user and logout routes in your app.py: (In the previous step we had created a stub method for login, replace that now with the actual implementation)

    @login_manager.user_loader
    def load_user(user_id):
        return User.get_by_id(user_id)           

    @app.route("/login", methods=['GET', 'POST'])
    def login():
        # Sanity check: if the user is already authenticated then go back to home page
        # if current_user.is_authenticated:
        #    return redirect(url_for('home'))

        form = LoginForm()
        if form.validate_on_submit():
            user = User.query.filter_by(display_name=form.username.data).first()
            hashed_input_password = hashlib.md5(form.password.data.encode()).hexdigest()
            if user and user.password == hashed_input_password:
                login_user(user, remember=form.remember.data)
                next_page = request.args.get('next')
                return redirect(next_page) if next_page else redirect(url_for('home'))
            else:
                flash('Login Unsuccessful. Please check user name and password', 'danger')
        return render_template('login.html', title='Login', form=form) 

    @app.route("/logout")
    @login_required
    def logout():
        logout_user()
        flash(f'You have logged out!', 'success')
        return redirect(url_for('home'))   
Again, there is some additional classes to import at the top of the file:

from forms import LoginForm
from flask_login import login_user, logout_user, login_required, current_user, login_manager, LoginManager
Also, because we are using flask_login, we need to initialize a LoginManager at the app level. This will help us start a session for the user when they login correctly, and allow us to have a current_user in our app (if requests are being made by a logged in user)

In app.py inside the create_app() method, before you start defining routes, add the following lines:

login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'
Now, there is no link in the site yet, but you can try to access /login on your app to try out the login form. You should be able to use some usser data you registered, to login successfully. At this point, because we do not show anywhere in the site if the user is logged in or not, after a successfull login you get redirected to the home page and nothing else changes. It is hard to tell if login is working / we have a logged in user or not. Next step will be to improve on that, we will change the navigation bar to reflect if the user is logged in or not!

Step 5 - Use the current_user to display conditionally some content (login link / new location)
Now that we can login users, we can make new location page only accesible to logged in users. If you are not logged in to the site you should not be able to do that. Also, if the user is not logged in we will show the login / register links in nav bar, but if the user is already logged, we will instead show a logout.

Modify the NavBar in map.html, what you whant to change is how the the items are displayed, now conditionally (with an if block) depending on whether we have a current user that is authenticated / logged in, or not:

(Careful! The chunck below is not the whole content of file map.html, only the part of the navigation bar that changes for our current feature)

  ...
  <nav class="navbar navbar-expand-lg navbar-dark bg-dark">
    <span class="navbar-brand mb-0 h1">Navbar</span>
    <button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarSupportedContent" aria-controls="navbarSupportedContent" aria-expanded="false" aria-label="Toggle navigation">
      <span class="navbar-toggler-icon"></span>
    </button>    
    <div class="collapse navbar-collapse" id="navbarSupportedContent">
      {% if current_user.is_authenticated %}
      <ul class="navbar-nav mr-auto">
        <li class="nav-item">
          <span class="nav-link text-reset">Hi {{ current_user.display_name }}!</span>
        </li>
        <li class="nav-item">
          <a class="nav-link" href="{{ url_for('new_location') }}">New Location</a>
        </li>
        <li class="nav-item">
          <a class="nav-link" href="{{ url_for('logout') }}">Logout</a>
        </li>      
      </ul>    
      {% else %}
      <ul class="navbar-nav mr-auto">
        <li class="nav-item">
          <a class="nav-link" href="{{ url_for('login') }}">Login</a>
        </li>
        <li class="nav-item">
          <a class="nav-link" href="{{ url_for('register') }}">New User Registration</a>
        </li>
      </ul>     
      {% endif %}
      <form method="GET" action="" onsubmit="return searchAddressSubmit()" class="form-inline my-2 my-lg-0">
        <input class="form-control mr-sm-2" id="search_address" type="search" placeholder="Search near..." aria-label="Search near">
        <button class="btn btn-info my-2 my-sm-0" type="submit">Search</button>
      </form>   
    </div>
  </nav>
  ....
You might need to tweak some additional styles to make everything look ok, I added this to styles.css:

.navbar li.nav-item {
  color: #fff;    
}
Add the @login_required annotation to the new_location route (the line in the middle):

    @app.route("/new-location", methods=['GET', 'POST'])
    @login_required
    def new_location():

## NEW STEPS/ CHANGES ##



- created a launch.json file  in .vscode
   - added lines 15-20:  "env": {
                "FLASK_APP": "app.py",
                "FLASK_ENV": "development",
                "DATABASE_URL": "postgres://xxx",
                "MAPS_API_KEY": "xxx"
            }
- MAKING APP RUN: instead of using "flask run" in terminal, run the debug mode to get right port. Make sure that port is exited with ctrl+c in "main" console (i.e. not the debug console) if you have used "flask run" beforehand. IMPORTANT: click on app.py and then on debug mode on the left. Otherwise, the app will not work properly. 

- Changed center of map that is seen when calling the "/-route" in the map.js-file (line 39) from Berlin to Leizig :
 view = new MapView({
    map: map,
    center: [12.3731, 51.3397], // Longitude, latitude. We start at the center of Leipzig
    zoom: 13, // Zoom level

    

## EXISTING ROUTES in app.py