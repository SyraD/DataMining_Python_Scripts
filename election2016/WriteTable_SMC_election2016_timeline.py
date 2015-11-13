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





import string
from datetime import datetime, date, time

from Table_SMC_election2016_timeline import *

from sqlalchemy import exc

from textblob import TextBlob

def get_sentiment(text):
    try:
        testimonial=TextBlob(text)
        polarity=testimonial.sentiment.polarity
        #subjectivity=testimonial.sentiment.subjectivity
    except Exception, e:
        print "Error reading id %s, exception: %s" % (kid, e)
        return None
    return polarity


def get_subjectivity(text):
    try:
        testimonial=TextBlob(text)
        subjectivity=testimonial.sentiment.subjectivity
    except Exception, e:
        print "Error reading id %s, exception: %s" % (kid, e)
        return None
    return subjectivity

def write_data(self, d, Twitter_handle, Unique_ID, party_code):   

    Unique_ID = Unique_ID
    party_code = party_code

    query = Twitter_handle  #d['search_metadata']['query']  #THIS IS DIFFERENT FROM MENTIONS AND DMS FILES
    
    for entry in d: 			
        json_output = str(entry)
       
        tweet_id = entry['id']
        tweet_id_str = entry['id_str']        
        inserted_date = datetime.now()   
        truncated = entry['truncated']
        language = entry['lang']
        
        if 'possibly_sensitive' in entry:
            possibly_sensitive= entry['possibly_sensitive']
        else:
            possibly_sensitive = ''
        
        coordinates = []
        if 'coordinates' in entry and entry['coordinates'] != None:
            for coordinate in entry['coordinates']['coordinates']:
                coordinates.append(coordinate)
            coordinates = ', '.join(map(str, coordinates))							

        else:
            coordinates = ''
            
        if 'retweeted_status' in entry:
            retweeted_status = 'THIS IS A RETWEET'

            retweeted_user = entry['retweeted_status']['user']['id_str']  
            retweeted_user_description = entry['retweeted_status']['user']['description'] 
            retweeted_user_screen_name = entry['retweeted_status']['user']['screen_name'] 
            retweeted_user_followers_count = entry['retweeted_status']['user']['followers_count']
            retweeted_user_listed_count = entry['retweeted_status']['user']['listed_count']
            retweeted_user_statuses_count = entry['retweeted_status']['user']['statuses_count'] 
            retweeted_user_location = entry['retweeted_status']['user']['location'] 
            retweeted_tweet_created_at_text = entry['retweeted_status']['created_at']
            retweeted_tweet_created_at = datetime.strptime(retweeted_tweet_created_at_text, '%a %b %d %H:%M:%S +0000 %Y')   
        
        else:
            retweeted_status = ''  
            retweeted_user = ''
            retweeted_user_description = ''
            retweeted_user_screen_name = ''
            retweeted_user_followers_count = ''
            retweeted_user_listed_count = ''
            retweeted_user_statuses_count = ''
            retweeted_user_location = ''
            retweeted_tweet_created_at = None
            
        if 'withheld_in_countries' in entry:
            withheld_in_countries = 'WITHHELD --> CHECK JSON'
        else:
            withheld_in_countries = ''
     
        if 'withheld_scope' in entry:
            withheld_scope = entry['withheld_scope']
        else:
            withheld_scope = ''
       
        content = entry['text']
        content = content.replace('\n','')      
        
        num_characters = len(content) #NUMBER OF CHARACTERS (SPACES INCLUDED)
        words = content.split()
        num_words = len(words)
        
        created_at_text = entry['created_at']    
        created_at = datetime.strptime(created_at_text, '%a %b %d %H:%M:%S +0000 %Y')   
        created_at2 = created_at.strftime('%Y-%m-%d %H:%M:%S')   

        month = created_at.strftime('%m')
        year = created_at.strftime('%Y')
        print 'month', month, 'year', year
        
        from_user_screen_name = entry['user']['screen_name']
        from_user_id = entry['user']['id'] 
        from_user_followers_count = entry['user']['followers_count']
        from_user_friends_count = entry['user']['friends_count']   
        from_user_listed_count = entry['user']['listed_count']
        from_user_favourites_count = entry['user']['favourites_count']
        print '\n', 'from_user_favourites_count-------------->', from_user_favourites_count
        from_user_statuses_count = entry['user']['statuses_count'] 
        from_user_description = entry['user']['description'] 
        from_user_location = entry['user']['location'] 
        from_user_created_at = entry['user']['created_at']
        
        retweet_count = entry['retweet_count'] 
        favorite_count = entry['favorite_count']
        
        in_reply_to_screen_name = entry['in_reply_to_screen_name']
        in_reply_to_status_id = entry['in_reply_to_status_id']

        #GENERATES VARIABLES FOR #URLS, HASHTAGS, AND MENTIONS
        entities_urls_count = len(entry['entities']['urls'])    
        entities_hashtags_count = len(entry['entities']['hashtags'])   
        entities_mentions_count = len(entry['entities']['user_mentions']) 
    
        source = entry['source']
        

        entities_urls, entities_expanded_urls, entities_hashtags, entities_mentions = [], [], [], []
               
        for link in entry['entities']['urls']:
            if 'url' in link:
                url = link['url']
                expanded_url = link['expanded_url']
                entities_urls.append(url)
                entities_expanded_urls.append(expanded_url)
            else:
                print "No urls in entry"

        for hashtag in entry['entities']['hashtags']:
            if 'text' in hashtag:
                tag = hashtag['text']
                entities_hashtags.append(tag)
            else:
                print "No hashtags in entry"

        for at in entry['entities']['user_mentions']:
            if 'screen_name' in at:
                mention = at['screen_name']
                print at['screen_name']
                entities_mentions.append(mention)
            else:
                print "No mentions in entry"
                
        entities_mentions = string.join(entities_mentions, u", ")
        entities_hashtags = string.join(entities_hashtags, u", ")
        entities_urls = string.join(entities_urls, u", ")
        entities_expanded_urls = string.join(entities_expanded_urls, u", ")    
        
        video_link = 0
        if 'vimeo' in entities_expanded_urls or 'youtube' in entities_expanded_urls or 'youtu' in entities_expanded_urls or 'vine' in entities_expanded_urls:
            video_link = 1					#All of these videos show up in 'View Media' in tweets
            print "FOUND A VIDEO!!!"
        else:
            video_link = 0
            
        #if photo_text.find('twitpic'): # or photo_text.find('instagram') or photo_text.find('instagr'):
        #if 'twitpic' in photo_text:
        if 'twitpic' in entities_expanded_urls:
            twitpic = 1						#twitpic images show up in 'View Media' in tweets
            print "FOUND A TWITPIC LINK!"
        else:
            twitpic = 0
        if 'twitpic' in entities_expanded_urls or 'instagram' in entities_expanded_urls or 'instagr' in entities_expanded_urls or 'imgur' in entities_expanded_urls:
            photo_link = 1					#instagram images DO NOT show up in 'View Media' in tweets
            print "FOUND A TWITPIC OR INSTAGRAM OR IMGUR LINK!!!"
        else:
            photo_link = 0
        
        #CONVERT TO UNICODE FOR INSERTION INTO SQLITE DB        
        entities_urls = unicode(entities_urls)
        entities_expanded_urls = unicode(entities_expanded_urls)
        entities_hashtags = unicode(entities_hashtags)
        entities_mentions = unicode(entities_mentions)

        if 'symbols' in entry['entities']:
		    print "HERE ARE THE SYMBOLS.......", entry['entities']['symbols']
        else:
		    print "THERE AIN'T NO entry['entities']['symbols']"
		
        if 'media' in entry['entities']:
			print "HERE ARE THE MEDIA.......", entry['entities']['media']
			entities_media_count = len(entry['entities']['media'])   
        else:
            entities_media_count = ''
					      
        if 'media' in entry['entities']:
            if 'expanded_url' in entry['entities']['media'][0]:
		        media_expanded_url = entry['entities']['media'][0]['expanded_url']
            else:
                print "THERE AIN'T NO expanded_url in entry['entities']['media']"
                media_expanded_url = ''
					    
            if 'media_url' in entry['entities']['media'][0]:
		        media_url = entry['entities']['media'][0]['media_url']
            else:
		        print "THERE AIN'T NO media_url in entry['entities']['media']"
		        media_url = ''
					    
            if 'type' in entry['entities']['media'][0]:
		        media_type = entry['entities']['media'][0]['type']
            else:
		        print "THERE AIN'T NO type in entry['entities']['media']"
		        media_type = ''
        else:
		    media_type = ''
		    media_url = ''
		    media_expanded_url = ''
         
        polarity = get_sentiment(content)
        subjectivity = get_subjectivity(content)
        
        upd = TWEET(query, tweet_id, tweet_id_str, inserted_date, truncated, language, possibly_sensitive, 
                coordinates, retweeted_status, withheld_in_countries, withheld_scope, created_at_text, 
                created_at, month, year, content, from_user_screen_name, from_user_id, from_user_followers_count, 
                from_user_friends_count, from_user_listed_count, from_user_favourites_count, from_user_statuses_count, from_user_description,   
                from_user_location, from_user_created_at, retweet_count, favorite_count, entities_urls, entities_urls_count,         
                entities_hashtags, entities_hashtags_count, entities_mentions, entities_mentions_count,   
                in_reply_to_screen_name, in_reply_to_status_id, source, entities_expanded_urls, json_output, 
                entities_media_count, media_expanded_url, media_url, media_type, video_link, photo_link, twitpic, 
                num_characters, num_words,
                retweeted_user, retweeted_user_description, retweeted_user_screen_name, retweeted_user_followers_count,
                retweeted_user_listed_count, retweeted_user_statuses_count, retweeted_user_location,
                retweeted_tweet_created_at,
                Unique_ID, party_code, polarity,  subjectivity,
                )
                
        self.session.add(upd)
        try:
            self.session.commit()
        except exc.SQLAlchemyError:
            self.session.rollback()
            print "NOT INSERTING --> IT'S A DUPLICATE"