### Web Sraping security and google news
The ```scrape_security_daily.py``` and ```scrape_google_weekly.py``` is running by cron job to download daily/weekly news into a pickle file, then send it via email as attachment. Gmail login and password needs to be stored in advance as instructed below. 

### Cron Jobs
```
#https://www.geeksforgeeks.org/cron-command-in-linux-with-examples/
10 5 * * * python3 scrape_security_daily.py
10 4 * * 7 python3 scrape_google_weekly.py
```
### pwd_google.py
save google login and password in pwd_google.py using below format
```
login = 'put email here'
pwd = 'put password here'
```
