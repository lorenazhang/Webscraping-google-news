### Web Sraping security and google news
The ```scrape_security_daily.py``` and ```scrape_google_weekly.py``` is running by cron job to download daily/weekly news into a pickle file, then send it via email as attachment. Gmail login and password needs to be stored in advance in a seperate file. 

### Cron Jobs
https://www.geeksforgeeks.org/cron-command-in-linux-with-examples/
```
10 5 * * * /opt/anaconda3/bin/python /Users/jingyao/Desktop/Python/nlp/scrape_security_daily.py
10 4 * * 7 /opt/anaconda3/bin/python /Users/jingyao/Desktop/Python/nlp/scrape_google_weekly.py
```
### Set up cron jobs on mac
1. For mac, cron and terminal needs to get access to all disks:
   https://blog.bejarano.io/fixing-cron-jobs-in-mojave/
2. install commond line tools package:
   ```xcode-select --install```
3. ```which 'python'``` in terminal to get the correct python path 
4. ```crontab -e``` to set up cron jobs; ```crontab -l``` to view existing cron jobs
### Set up ```pwd_google.py```
save google login and password in pwd_google.py using below format
```
login = 'put email here'
pwd = 'put password here'
```
