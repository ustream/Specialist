***SPECialist***

***What is this?***

This is a heavily modified version of [this awesome little piece of code](https://github.com/vincentbernat/serverspec-example) (mad props for it, really). This tool makes you able to run serverspec locally on your production servers and post the results to a dashboard , where you can have a look at the results. This is achieved with a heavily modified Rakefile, and a simple Flask API +Angular.JS Frontend. It can be used as a dashboard, or as a really simple monitoring solutions.

***Getting started***

**Prerequisites**

* a relational database
* python 2
* virtualenv

**Setup**

```
git clone https://github.com/ustream/specialist.git
cd specialist
virtualenv virtualenv
. virtualenv/bin/activate
python application.py
```

**DB Support**

Specialist uses SQLAlchemy, so supports wide variety of relational databases. The requirements.txt comes with the mysql binding, you should change that to reflect your needs if You are not using MySQL

**Configuration**

You can set the environment variable SPECIALIST_SETTINGS_PATH to point to a python file containing your special settings.
Example config

```
LISTEN_HOST = "127.0.0.1"
LISTEN_PORT = 8080
ALCHEMY_URL = 'sqlite:////opt/specialist/spec.db'
```

You should change the $SPEC_ENDPOINT constant on the top of your Rakefile as well, to send the reports to the correct place

**Contributors**

* [deathowl](http://github.com/deathowl) : Rakefile, Flask API
* [kispocok](http://github.com/kispocok) : Thanks for the Angular part

Made with love at Ustream