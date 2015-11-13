''' 
Datamining Twitter Content About the 2015 election

Credits:

Base code by Dr. Gregory Saxton. Twitter: @gregorysaxton, website: social-metrics.org
Modifications to focus on the election 
by Dr. Weiai Wayne Twitter: @cosmopolitanvan, website: curiositybits.com
Modifications and comments to assist beginners by:
sarahd on Twitter @behaviordots, part of the @curiositybits collective
website: curiositybits.org

''' 




# for defining tables used in timeline database

import sqlalchemy
from sqlalchemy.orm import mapper, sessionmaker
from sqlalchemy import Column, Integer, String, ForeignKey, Text, DateTime, Unicode, Float
from sqlalchemy.ext.declarative import declarative_base
from types import *

Base = declarative_base()

class ACCOUNT(Base):
    __tablename__ = 'accounts'
    Unique_ID = Column(Integer, primary_key=True)     
    candidate_name = Column(String)
    candidate_websiteURL = Column(String)
    Twitter_URL = Column(String)  
    Twitter_handle = Column(String)  
    party_code = Column(Integer)
    #state = Column(String)
    earliest_tweet_in_db = Column(String)
    number_of_tweets_in_db_first_run = Column(Integer)
    
    def __init__(self, candidate_name, candidate_websiteURL, Twitter_URL, Twitter_handle, party_code,
        earliest_tweet_in_db, number_of_tweets_in_db_first_run, 
    ):       
    
        self.candidate_name = candidate_name
        self.candidate_websiteURL = candidate_websiteURL
        self.Twitter_URL = Twitter_URL       
        self.Twitter_handle = Twitter_handle
        self.party_code = party_code
        #self.state = state
        self.earliest_tweet_in_db = earliest_tweet_in_db
        self.number_of_tweets_in_db_first_run = number_of_tweets_in_db_first_run
     
    def __repr__(self):
       return "<Twitter handle, party_code('%s', '%s')>" % (self.Twitter_handle,self.party_code)

class TWEET(Base):
    __tablename__ = 'candidate_timeline'
    rowid = Column(Integer, primary_key=True)  
    query = Column(String)
    tweet_id = Column(String) 
    tweet_id_str = Column(String, unique=True)		##### UNIQUE CONSTRAINT ##### 
    inserted_date = Column(DateTime)
    truncated = Column(String)
    language = Column(String)
    possibly_sensitive = Column(String)  ### NEW 
    coordinates = Column(String)					#Represents the geographic location of this Tweet as reported by the user or client application. The inner coordinates array is formatted as geoJSON (longitude first, then latitude). 
    retweeted_status = Column(String)
    withheld_in_countries = Column(String)
    withheld_scope = Column(String)
    created_at_text = Column(String)   				#UTC time when this Tweet was created. 
    created_at = Column(DateTime)
    month = Column(String)
    year = Column(String)
    content = Column(Text)
    from_user_screen_name = Column(String)			#The screen name, handle, or alias that this user identifies themselves with. screen_names are unique but subject to change. Use id_str as a user identifier whenever possible. 
    from_user_id = Column(String)   
    from_user_followers_count = Column(Integer)  	#The number of followers this account currently has. 
    from_user_friends_count = Column(Integer)  		#The number of users this account is following (AKA their "followings"). 
    from_user_listed_count = Column(Integer)  		#The number of public lists that this user is a member of.
    from_user_favourites_count = Column(Integer)	#The number of tweets this user has favorited in the account's lifetime. British spelling used in the field name for historical reasons. 
    from_user_statuses_count = Column(Integer)  	#The number of tweets (including retweets) issued by the user. 
    from_user_description = Column(String)  		#The user-defined UTF-8 string describing their account. 
    from_user_location = Column(String)  			#The user-defined location for this account's profile. 
    from_user_created_at = Column(String)  			#The UTC datetime that the user account was created on Twitter. 
    retweet_count = Column(Integer)
    favorite_count = Column(Integer)				#Indicates approximately how many times this Tweet has been "favorited" by Twitter users. 
    entities_urls = Column(Unicode(255))
    entities_urls_count = Column(Integer)        
    entities_hashtags = Column(Unicode(255))
    entities_hashtags_count = Column(Integer)    
    entities_mentions = Column(Unicode(255))    
    entities_mentions_count = Column(Integer)  
    in_reply_to_screen_name = Column(String)  
    in_reply_to_status_id = Column(String)  
    source = Column(String)
    entities_expanded_urls = Column(Text) 
    json_output = Column(String)
    entities_media_count = Column(Integer)
    media_expanded_url = Column(Text) 
    media_url = Column(Text) 
    media_type = Column(Text) 
    video_link = Column(Integer)
    photo_link = Column(Integer)
    twitpic = Column(Integer)
    num_characters = Column(Integer)    				
    num_words = Column(Integer)        					
    retweeted_user = Column(Text) 
    retweeted_user_description = Column(Text) 
    retweeted_user_screen_name = Column(Text) 
    retweeted_user_followers_count = Column(Integer) 
    retweeted_user_listed_count = Column(Integer) 
    retweeted_user_statuses_count = Column(Integer) 
    retweeted_user_location = Column(Text) 
    retweeted_tweet_created_at = Column(DateTime)		
    Unique_ID = Column(Integer)							#SPECIFIC TO HEALTH ADVOCACY ACCOUNTS
    party_code = Column(String)							#SPECIFIC TO HEALTH ADVOCACY ACCOUNTS
    polarity = Column(Float) #USING TEXTBLOB
    subjectivity = Column(Float) #USING TEXTBLOB
    def __init__(self, query, tweet_id, tweet_id_str, inserted_date, truncated, language, possibly_sensitive, coordinates, 
    retweeted_status, withheld_in_countries, withheld_scope, created_at_text, created_at, month, year, content, 
    from_user_screen_name, from_user_id, from_user_followers_count, from_user_friends_count,   
    from_user_listed_count, from_user_favourites_count, from_user_statuses_count, from_user_description,   
    from_user_location, from_user_created_at, retweet_count, favorite_count, entities_urls, entities_urls_count,         
    entities_hashtags, entities_hashtags_count, entities_mentions, entities_mentions_count,   
    in_reply_to_screen_name, in_reply_to_status_id, source, entities_expanded_urls, json_output, 
    entities_media_count, media_expanded_url, media_url, media_type, video_link, photo_link, twitpic, 
    num_characters, num_words,  
    retweeted_user, retweeted_user_description, retweeted_user_screen_name, retweeted_user_followers_count,
    retweeted_user_listed_count, retweeted_user_statuses_count, retweeted_user_location,
    retweeted_tweet_created_at, 
    Unique_ID, party_code, polarity, subjectivity
    ):
    
        self.query = query
        self.tweet_id = tweet_id
        self.tweet_id_str = tweet_id_str
        self.inserted_date = inserted_date
        self.truncated = truncated
        self.language = language
        self.possibly_sensitive = possibly_sensitive
        self.coordinates = coordinates
        self.retweeted_status = retweeted_status
        self.withheld_in_countries = withheld_in_countries
        self.withheld_scope = withheld_scope
        self.created_at_text = created_at_text
        self.created_at = created_at 
        self.month = month
        self.year = year
        self.content = content
        self.from_user_screen_name = from_user_screen_name
        self.from_user_id = from_user_id       
        self.from_user_followers_count = from_user_followers_count
        self.from_user_friends_count = from_user_friends_count
        self.from_user_listed_count = from_user_listed_count
        self.from_user_favourites_count = from_user_favourites_count
        self.from_user_statuses_count = from_user_statuses_count
        self.from_user_description = from_user_description
        self.from_user_location = from_user_location
        self.from_user_created_at = from_user_created_at
        self.retweet_count = retweet_count
        self.favorite_count = favorite_count
        self.entities_urls = entities_urls
        self.entities_urls_count = entities_urls_count        
        self.entities_hashtags = entities_hashtags
        self.entities_hashtags_count = entities_hashtags_count
        self.entities_mentions = entities_mentions
        self.entities_mentions_count = entities_mentions_count     
        self.in_reply_to_screen_name = in_reply_to_screen_name
        self.in_reply_to_status_id = in_reply_to_status_id
        self.source = source
        self.entities_expanded_urls = entities_expanded_urls
        self.json_output = json_output
        self.entities_media_count = entities_media_count
        self.media_expanded_url = media_expanded_url
        self.media_url = media_url
        self.media_type = media_type
        self.video_link = video_link
        self.photo_link = photo_link
        self.twitpic = twitpic
        self.num_characters = num_characters
        self.num_words = num_words
        self.retweeted_user = retweeted_user
        self.retweeted_user_description = retweeted_user_description
        self.retweeted_user_screen_name = retweeted_user_screen_name
        self.retweeted_user_followers_count = retweeted_user_followers_count
        self.retweeted_user_listed_count = retweeted_user_listed_count
        self.retweeted_user_statuses_count = retweeted_user_statuses_count
        self.retweeted_user_location = retweeted_user_location
        self.retweeted_tweet_created_at = retweeted_tweet_created_at    
        self.Unique_ID = Unique_ID
        self.party_code = party_code
        self.polarity=polarity
        self.subjectivity = subjectivity
        
    def __repr__(self):
       return "<sender, created_at('%s', '%s')>" % (self.from_user_screen_name,self.created_at)
       
       
       

       