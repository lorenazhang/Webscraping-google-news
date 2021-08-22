#!/bin/bash
/usr/bin/python3 /home/pi/webscraping/scrape_security_daily.py >> /home/pi/webscraping/log/log_daily.txt 2>&1
/home/pi/webscraping/push_to_git.sh >> /home/pi/webscraping/log/log_git.txt 2>&1
