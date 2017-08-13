https://github.com/huginn/huginn/wiki/Novice-setup-guide
git clone git://github.com/cantino/huginn.git

http://www.ruby-lang.org/en/documentation/installation/#yum
https://rvm.io/

Install rvm
RVM ("Ruby Version Manager")
RVM allows you to install and manage multiple installations of Ruby on your system. It can also manage different gemsets.
It is available for OS X, Linux, or other UNIX-like operating systems.

gpg --keyserver hkp://keys.gnupg.net --recv-keys 409B6B1796C275462A1703113804BB82D39DC0E3 7D2BAF1CF37B13E2069D6956105BD0E739499BDB
curl -sSL https://get.rvm.io | bash -s stable
/usr/local/rvm/bin/rvm reload
/usr/local/rvm/bin/rvm -v
rvm 1.29.2 (latest) by Michal Papis, Piotr Kuczynski, Wayne E. Seguin [https://rvm.io/]

/usr/local/rvm/bin/rvm requirements run
Checking requirements for centos.
Requirements installation successful.

Install ruby
/usr/local/rvm/bin/rvm install 2.3.3
/usr/local/rvm/rubies/ruby-2.3.3/bin/ruby -v
ruby 2.3.3p222 (2016-11-21 revision 56859) [x86_64-linux]

Install gem
https://rubygems.org/pages/download#formats
wget https://rubygems.org/rubygems/rubygems-2.6.12.tgz
tar xvzf rubygems-2.6.12.tgz
cd rubygems-2.6.12
/usr/local/rvm/rubies/ruby-2.3.3/bin/ruby setup.rb
/usr/local/rvm/rubies/ruby-2.3.3/bin/gem --version
2.6.12
/usr/local/rvm/rubies/ruby-2.3.3/bin/gem install rails -v 4.2.5

Install rake and bundler
/usr/local/rvm/rubies/ruby-2.3.3/bin/gem install rake bundler

/etc/profile.d/ruby.sh
```
export PATH=$PATH:/usr/local/rvm/rubies/ruby-2.3.3/bin/
```
source /etc/profile.d/ruby.sh

By default, rvm will install /etc/profile.d/rvm.sh

Other options: use ln
```
ln -s /usr/local/rvm/rubies/ruby-2.3.3/bin/ruby /usr/bin/ruby
ln -s /usr/local/rvm/rubies/ruby-2.3.3/bin/gem /usr/bin/gem
ln -s /usr/local/rvm/rubies/ruby-2.3.3/bin/rake /usr/bin/rake
ln -s /usr/local/rvm/rubies/ruby-2.3.3/bin/bundle /usr/bin/bundle
ln -s /usr/local/rvm/bin/rvm /usr/bin/rvm
```

Install huginn dependencies
cd huginn
mv .env.example .env
config db
export LANG=en_US.UTF-8
export LANGUAGE=en_US.UTF-8
export LC_ALL=en_US.UTF-8
sudo bundle install

Rake something
[bundle exec] rake secret
Edit .env, at least updating the APP_SECRET_TOKEN variable we just created.

[bundle exec] rake db:migrate
[bundle exec] rake db:seed

Start
foreman start & (run in tmux)

http://<IP-SERVER>:3000
