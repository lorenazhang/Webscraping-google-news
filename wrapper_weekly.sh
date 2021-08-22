#!/bin/bash
/usr/bin/python3 /home/pi/webscraping/scrape_google_weekly.py >>  /home/pi/webscraping/log/log_weekly.txt 2>&1
/home/pi/webscraping/push_to_git.sh >> /home/pi/webscraping/log/log_git.txt 2>&1
