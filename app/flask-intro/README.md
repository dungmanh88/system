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
pip install Flask gunicorn

### Install heroku
wget https://cli-assets.heroku.com/branches/stable/heroku-linux-amd64.tar.gz
mkdir -p /usr/local/lib /usr/local/bin
tar -xvzf heroku-linux-amd64.tar.gz -C /usr/local/lib
ln -s /usr/local/lib/heroku/bin/heroku /usr/local/bin/heroku
heroku --version
heroku login ### make sure you have an account

### Using gunicorn
gunicorn -b 192.168.10.121:4000 app:app

### Using Procfile
heroku local

### Flush requirements
pip freeze > requirements.txt

### Using heroku
heroku create [app-name]
heroku apps
heroku apps:info --app dungnm-app
heroku open --app dungnm-app

### heroku unit test
heroku run python test.py -v

### Push code to heroku
git init
git add .
### Make sure you have configured user.name and user.email (not global)
git commit -m "Init"
heroku create
git remove -v
git config --list
git push heroku master

### Create .gitignore
*.pyc
*.db
venv
.gitignore
.gitkeep
.git
