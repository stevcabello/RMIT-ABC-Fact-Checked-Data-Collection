import requests
from bs4 import BeautifulSoup, NavigableString, Tag
import snscrape.modules.twitter as sntwitter
import pandas as pd
import re
import datetime
import time
from datetime import datetime
import json

pd.set_option("display.max_rows", None)
pd.set_option("display.max_columns", None)
pd.set_option('display.max_colwidth', None)



def hasTweetSource(text):
    tweet_terms = ['tweet','Twitter','Tweet','twitter']
    for searched_word in tweet_terms:
        results = re.findall(r"(\.*?%s.*?\.)" % searched_word, text) ##Adapted from https://stackoverflow.com/a/34347639
        if len(results) > 0:
            return True,results
    return False,""


def getTextInClaim(soup):
    #Adapted from: https://stackoverflow.com/a/42821649
    text_in_claim = ""
    for header in soup.find_all('h2', {"data-component": "Heading"} )[:1]: ## [:1] due to The claim is the first h2 node. Do not to inspect more 
        nextNode = header
        while True:
            nextNode = nextNode.nextSibling
            if nextNode is None:
                break
            if isinstance(nextNode, Tag):
                if nextNode.name == "h2":
                    break
                if nextNode.name != "p": ## to avoid print information not included between <p> </p> tags
                    continue
                extracted_sentence = nextNode.get_text(strip=True).strip()
                extracted_sentence = extracted_sentence.replace('\'\'','"')
                extracted_sentence = extracted_sentence.replace(u'\xa0', u' ')
                extracted_sentence = re.sub(r"([\(\[]).*?([\)\]])", "", extracted_sentence) #remove [ ] from claims
                text_in_claim += extracted_sentence
    return text_in_claim

def getSinceUntilTimestamps(published_time, months_before_publication):
    until_tstamp = (time.mktime(published_time.timetuple()))
    until_tstamp = int(until_tstamp)
    
    since_tstamp = until_tstamp - (months_before_publication*30*24*60*60)
    since_tstamp = int(since_tstamp)
    
    return since_tstamp, until_tstamp


def extractFromMeta(metas, to_extract):
    if to_extract == "title" or to_extract=="description":
        extracted_info = [meta.attrs['content'].replace(u'\xa0', u' ') for meta in metas if 'name' in meta.attrs and meta.attrs['name'] == to_extract ][0]
        extracted_info = extracted_info.split('?',1)[0]
        extracted_info = extracted_info.split('.',1)[0]
    elif to_extract == "published_time":
    	try:
    		extracted_info = [ meta.attrs['content'] for meta in metas if 'property' in meta.attrs and meta.attrs['property'] == 'article:'+to_extract ][0]
    		extracted_info = datetime.fromisoformat(extracted_info)
    	except:
        	extracted_info = ""

    return extracted_info



def getOriginalTweets(quotes_to_search, since_tstamp, until_tstamp, max_tweets_to_retrieve):
	original_tweets = []
	for quote_to_search in quotes_to_search:
		tweets_list = []
		if len(quote_to_search) < 200: #to avoid errors for large quotes... 253 is the maximum number of characters allowd for TwitterSearchScraper
			# Using TwitterSearchScraper to scrape data and append tweets to list
			for i,tweet in enumerate(sntwitter.TwitterSearchScraper('"'+quote_to_search+'" since_time:'+str(since_tstamp)+' until_time:'+str(until_tstamp)).get_items()):
			    if i>max_tweets_to_retrieve:
			        break
			    tweets_list.append([tweet.date, tweet.id, tweet.content, tweet.user.username])
			
			if len(tweets_list) > 0:
				# Creating a dataframe from the tweets list above
				tweets_df = pd.DataFrame(tweets_list, columns=['Datetime', 'Tweet Id', 'Text', 'Username'])
				tweet_status = getTweetStatus(tweets_df[-1:]) #-1 to just use the first tweet found when searching quote_to_search
				original_tweets.append(tweet_status)
			else:
				original_tweets.append("No tweets found")
		else:
			original_tweets.append("Quoted claim exceeds 280 characters")

	return original_tweets


def getTweetStatus(tweet_info):
	username = tweet_info["Username"].to_string(index=False).strip()
	tweet_id = tweet_info["Tweet Id"].to_string(index=False).strip()
	return "www.twitter.com/"+username+"/status/"+tweet_id
