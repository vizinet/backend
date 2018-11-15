#!/bin/bash
sudo systemctl restart gunicorn
sudo nginx -t
sudo systemctl restart nginx
