try: 
    import newspaper
    import feedparser
    import numpy as np
    import pandas as pd
    import requests
    import datetime 
    from tqdm import tqdm
    import nltk
    from nltk.corpus import stopwords
    from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
    from sklearn.decomposition import NMF, LatentDirichletAllocation
    import joblib
    from newspaper import Article
    import pickle
    import smtplib
    from email.message import EmailMessage
    import pwd_google
    import os

    #dtp = '/Users/jingyao/Desktop/Python/nlp/data'
    dtp = '/home/pi/webscraping/data'
    to_list = "lorenazhang@gmail.com,jingyao.zhang@wellsfargo.com"

    def send_email(login
                   , password
                   , subject
                   , to_list
                   , content = None
                   , attachment = None
                   ):
        msg = EmailMessage()
        msg.set_content(content)
        msg['From'] = login
        msg['Subject'] = subject
        msg['To'] = to_list
        #attachment
        if attachment is not None:
            with open(attachment, 'rb') as content_file:
                content = content_file.read()
                msg.add_attachment(content, maintype='application', subtype='pickle', filename = os.path.basename(attachment))

        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.set_debuglevel(0)
        server.ehlo()
        server.starttls()
        server.login(login, password)
        server.send_message(msg)
        server.quit()
        print('Email successfully sent!')

    today = pd.Timestamp.today()
    sunday = today - datetime.timedelta(days = today.dayofweek) + datetime.timedelta(days = 6)
    sunday_str = sunday.strftime('%Y%m%d')
    filename = f'googlenews_{sunday_str}.pkl'

    LOGIN    = pwd_google.login
    PASSWORD = pwd_google.pwd

    # Blank dataframe, based on fields identified later

    rss_feeds = pd.DataFrame(columns = ['title',  'summary',  'links',  'link',  'id',  'guidislink',  'published',  
                                        'published_parsed',  'title_detail.type',  'title_detail.language',  
                                        'title_detail.base',  'title_detail.value',  'summary_detail.type',  
                                        'summary_detail.language',  'summary_detail.base',  'summary_detail.value',  
                                        'media_content',  'feedburner_origlink'])
    rss_urls = ['https://news.google.com/rss/search?q=%3Cdigital+inequality%3E&hl=en-US&gl=US&ceid=US:en']

    # Get all the feed entries.  But the dataframe resulting from this has only a summary line, 
    # not the entire text of the article.  For that we will pull the URL in using the 
    # newspaper library later.

    for rss in tqdm(rss_urls):
        feed = feedparser.parse(rss)
        rss_feeds=pd.concat([rss_feeds, pd.json_normalize(feed.entries)], axis=0)
    print(len(rss_feeds), 'items in rss_feed dataframe')

    # Remove duplicate URLs
    urllist =rss_feeds.link.unique()

    # Get full text using scraping from the newspaper library

    df = pd.DataFrame(columns = ["date", "URL", "authors", "keywords", "summary", "text"])

    for url in tqdm(urllist):
        article = Article(url)
        try:
            article.download()
            article.parse()
            article.nlp()
            dict1 = {"date": article.publish_date, 
                     "URL": url, 
                     "authors": article.authors,
                     "keywords": article.keywords, 
                     "summary": article.summary, 
                     "text": article.text}
        #print(dict1)
            df = df.append(dict1, ignore_index=True)
        except:
            print('Something wrong with', url)

    print(len(df),'stories in dataframe df')



    # Merge the RSS dataframe with the full text obtained from the 
    # newspaper library

    df_final = rss_feeds.merge(df,how="right", left_on="link", right_on="URL")
    print(len(df_final),'unique articles in file.')

    #just keep columns that are useful
    df_final = df_final[['id','title', 'summary_x', 'URL', 'published', 'keywords', 'summary_y', 'text' ]]

    def no_timezone(time_string):
        try:
            no_tz = datetime.datetime.strftime(pd.Timestamp(time_string), "%Y-%m-%d %H:%M:%S")
        except:
            no_tz = 0
        return no_tz

    df_final['published_date'] = df_final['published'].apply(lambda x: no_timezone(x))
    df_final.drop(columns = ['published'], inplace = True)
    df_final['keywords'] = [','.join(a) for a in df_final['keywords'].copy(deep=True)]

    pickle.dump(df_final, open(f'{dtp}/{filename}', 'wb'))
    print(f'pickle file created')

    #sent email with attachment

    send_email(login = LOGIN
              , password = PASSWORD
              , to_list = to_list
              , subject = f'Google News for {sunday_str}'
              , content = f'Please find attached the google news for week {sunday_str}'
              , attachment = f'{dtp}/{filename}')
except:
    send_email(login = LOGIN
              , password = PASSWORD
              , subject = f'Web scrapping Google news failed for {sunday_str}'
              , to_list = to_list
              , content = f'Job failed for Web scrapping Google news for week {sunday_str}'
              )
