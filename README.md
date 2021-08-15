### Web Sraping security and google news
The ```scrape_security_daily.py``` and ```scrape_google_weekly.py``` is running daily/weekly to download security news into csv/pickle files, then send via email as an attachment. Gmail login and password needs to be stored in advance in a seperate file. 

### Set up ```pwd_google.py```
save google login and password in pwd_google.py using below format
```
login = 'put email here'
pwd = 'put password here'
```

### Cron Jobs
https://www.geeksforgeeks.org/cron-command-in-linux-with-examples/
```
01 6 * * * /opt/anaconda3/bin/python /Users/jingyao/Desktop/Python/nlp/scrape_security_daily.py
03 6 * * 7 /opt/anaconda3/bin/python /Users/jingyao/Desktop/Python/nlp/scrape_google_weekly.py
```
### Set up cron jobs on mac
1. For mac, cron and terminal needs to get access to all disks:
   https://blog.bejarano.io/fixing-cron-jobs-in-mojave/
2. install commond line tools package:
   ```xcode-select --install```
3. ```which 'python'``` in terminal to get the correct python path 
4. ```crontab -e``` to set up cron jobs; ```crontab -l``` to view existing cron jobs and view logs
5. ```System Preferences -> Battery -> Schedule``` 
   set up auto-wake (cron jobs will not run while macbook is sleeping)
6. uncheck ```System Preferences -> Security & Privacy -> Require password after sleep```


