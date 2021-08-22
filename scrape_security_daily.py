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
    today_str = today.strftime('%Y%m%d')
    filename = f'securitynews_date_{today_str}.p' 

    LOGIN    = pwd_google.login
    PASSWORD = pwd_google.pwd

    ## Web Scraping

    # Blank dataframe, based on fields identified later

    rss_feeds = pd.DataFrame(columns = ['title',  'summary',  'links',  'link',  'id',  'guidislink',  'published',  
                                        'published_parsed',  'title_detail.type',  'title_detail.language',  
                                        'title_detail.base',  'title_detail.value',  'summary_detail.type',  
                                        'summary_detail.language',  'summary_detail.base',  'summary_detail.value',  
                                        'media_content',  'feedburner_origlink'])


    # List of RSS URLs to scrape

    rss_urls = [r'http://www.schneier.com/blog/index.rdf', 
                r'http://feeds.feedburner.com/darknethackers', 
                r'http://securityaffairs.co/wordpress/feed', 
                r'http://healthitsecurity.com/feed/', 
                r'http://blog.seanmason.com/feed/', 
                r'http://threatpost.com/feed', 
                r'http://feeds.trendmicro.com/Anti-MalwareBlog/', 
                r'http://www.infosecurity-magazine.com/rss/news/', 
                r'http://krebsonsecurity.com/feed/', 
                r'http://www.darkreading.com/rss/all.xml', 
                r'http://blog.kaspersky.com/feed/', 
                r'http://www.baesystems.com/page/rss?lg=en', 
                r'http://rss.nytimes.com/services/xml/rss/nyt/Technology.xml', 
                r'http://feeds.feedburner.com/scmagazinenews', 
                r'http://taosecurity.blogspot.com/atom.xml', 
                r'http://www.rms.com/blog/feed/', 
                r'http://iscxml.sans.org/rssfeed.xml', 
                r'https://community.qualys.com/blogs/securitylabs/feeds/posts', 
                r'http://googleonlinesecurity.blogspot.com/atom.xml', 
                r'http://thehackernews.com/feeds/posts/default', 
                r'http://www.us-cert.gov/current/index.rdf', 
                r'http://feeds.feedburner.com/Securityweek', 
                r'http://nakedsecurity.sophos.com/feed/', 
                r'http://feeds.arstechnica.com/arstechnica/index/', 
                r'http://www.csoonline.com/feed/attribute/41014', 
                r'http://blogs.rsa.com/feed/', 
                r'http://feeds.feedburner.com/Techcrunch', 
                r'http://recode.net/feed/', 
                r'http://www.techmeme.com/index.xml', 
                r'http://www.technologyreview.com/stream/rss/']

    # Get all the feed entries.  But the dataframe resulting from this has only a summary line, 
    # not the entire text of the article.  For that we will pull the URL in using the 
    # newspaper library later.

    for rss in tqdm(rss_urls):
        try:
            feed = feedparser.parse(rss)
            rss_feeds=pd.concat([rss_feeds, pd.json_normalize(feed.entries)], axis=0)
        except:
            print(f'Something went wrong, {rss}')
    print(len(rss_feeds), 'items in rss_feed dataframe')    

    # Remove duplicate URLs
    urllist =rss_feeds.link.unique()

    # Get full text using scraping from the newspaper library

    df = pd.DataFrame(columns = ["date",  "URL", "authors", "keywords", "summary", "text"])

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

    final = rss_feeds.merge(df,how="right", left_on="link", right_on="URL")
    final = final[['id','title', 'summary_x', 'URL', 'published', 'keywords', 'summary_y', 'text' ]]
    print(len(final),'unique articles in file.')

    # Save the file
    pickle.dump(final, open(f'{dtp}/{filename}','wb'))
    print('Pickle file created')

    #sent email with attachment
    send_email(login = LOGIN
              , password = PASSWORD
              , subject = f'Security News for {today_str}'
              , to_list = to_list
              , content = f'Please find attached the security news for {today_str}'
              , attachment = f'{dtp}/{filename}')
except:
    send_email(login = LOGIN
              , password = PASSWORD
              , subject = f'Web scrapping Security news failed for {today_str}'
              , to_list = to_list
              , content = f'Job failed for Web scrapping Google news for {today_str}'
              )
