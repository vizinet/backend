
# Developing Locally

Restore development environment for Python 2.7 on Ubuntu:

`pip2 install -r requirements.txt`

This will install all the same packages we used to develop the website and
backend.

# Getting Started

Step 1: SSH into the thing!
sudo ssh admin@airpacfire.eecs.wsu.edu
Password: airpact@fire  # 16

Step 2: run server
cd / home / justin / AIRPACT - Fire - Website

* No Logs *
sudo gunicorn - -bind 0.0.0.0: 80 AIRPACT_Fire.wsgi: application(in the same directory as manage.py)

* Log to master_log file *
sudo gunicorn - -bind 0.0.0.0: 80 - -log - level debug - -log - file master_log AIRPACT_Fire.wsgi: application


# Restarting Server

- ps - A(Find the proccess with the gunicorn pid)
- sudo kill[pid]
- sudo gunicorn - -bind 0.0.0.0: 80 AIRPACT_Fire.wsgi: application(in the same directory as manage.py)


# Log Script

Usage:

sudo . / log_script[log_file][url_to_post]

or with nohup(Script doesn't die when server is off)
sudo nohup . / log_script[file][url] &

Example:

sudo nohup . / log_script master_log https: // hooks.slack.com / services / T2EFPF5LM / B3VBZKUPL / nRUFIh8VcUzlxqO8sCPBgc72 &

# Git
git clone https: // github.com / AIRPACT - Fire / Website.git
