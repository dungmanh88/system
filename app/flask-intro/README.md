### Install pip
wget https://bootstrap.pypa.io/get-pip.py
python get-pip.py
pip install -U pip

### Install venv
pip install virtualenv
cd flask-intro
virtualenv venv

### Using venv
source venv/bin/activate
deactivate

### Into venv
pip install Flask gunicorn Flask-SQLAlchemy ipython psycopg2

### Using ipython
ipython

### Install heroku
wget https://cli-assets.heroku.com/branches/stable/heroku-linux-amd64.tar.gz
mkdir -p /usr/local/lib /usr/local/bin
tar -xvzf heroku-linux-amd64.tar.gz -C /usr/local/lib
ln -s /usr/local/lib/heroku/bin/heroku /usr/local/bin/heroku
heroku --version
heroku login ### make sure you have an account

### Using gunicorn to start app
gunicorn -b 192.168.10.121:4000 app:app
gunicorn app:app ### run on 0.0.0.0:8000

### Procfile
web: gunicorn app:app

### Using Procfile to start app via gunicorn
heroku local

### Flush requirements
pip freeze > requirements.txt

### Using heroku
heroku create [app-name]
heroku apps/heroku list
heroku apps:info --app [app-name]
heroku open --app [app-name]

### heroku unit test
heroku run --app [app-name] python test.py -v

### Run python on heroku
heroku run --app [app-name] python test.py -v
heroku run --app [app-name] python db_create.py
heroku run python ### call python shell
heroku run ipython 

### Push code to heroku
git init
git add .
### Make sure you have configured user.name and user.email (not global)
git config user.name "my username"
git config user.email "my email"
git commit -m "Init"
heroku create
heroku info [app-name]
git remote add heroku [remote-url]
git remote -v
git config --list
git push heroku master
git pull heroku master

### Create .gitignore
*.pyc
*.db
venv
.gitignore
.gitkeep
.git

### Procfile: which process type and how to start app
### requirements: Libraries that is neccessary for app


### Create db
python sql.py ### -> sample.db
or
python db_create.py ### -> posts.db

### Set environment variables on heroku
heroku config:set APP_SETTINGS=config.ProductionConfig --remote heroku
heroku addons:add heroku-postgresql:hobby-dev

Database has been created and is available
 ! This database is empty. If upgrading, you can transfer
 ! data from another database with pg:copy
Created postgresql-octagonal-15381 as DATABASE_URL
-> This means heroku created an database and you can access it via DATABASE_URL

### View heroku config
heroku config

### Install pg adapter
sudo apt-get install libpq-dev
or
yum install postgresql-devel
pip install psycopg2
