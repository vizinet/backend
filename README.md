
# Developing Locally

Restore development environment for Python 2.7 on Ubuntu:

`pip2 install -r requirements.txt`

This will install all the same packages we used to develop the website and
backend.

# Getting Started

## Step 1: SSH into the thing!

```bash
sudo ssh admin@airpacfire.eecs.wsu.edu # Password: airpact@fire#16
```

## Step 2: Run server

```bash
cd /home/justin/AIRPACT-Fire-Website
```

*No Logs*
```bash
sudo gunicorn --bind 0.0.0.0:80 AIRPACT_Fire.wsgi:application # in the same directory as `manage.py`
```

*Log to master_log file*
```bash
sudo gunicorn --bind 0.0.0.0:80 --log-level debug --log-file master_log AIRPACT_Fire.wsgi:application
```

# Restarting Server

```bash
ps -A # Find the process with the Gunicorn pid
sudo kill[pid] # Kill that process
sudo gunicorn --bind 0.0.0.0:80 AIRPACT_Fire.wsgi:application # In the same directory as manage.py
```

# Log Script

Usage:

```bash
sudo ./log_script[log_file][url_to_post]
```

or with nohup (so script doesn't die when server is off):

```bash
sudo nohup ./log_script[file][url] &
```

Example:

```bash
sudo nohup ./log_script master_log https://hooks.slack.com/services/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 &
```

# Git
```bash
git clone https://github.com/AIRPACT-Fire/Website.git
```
