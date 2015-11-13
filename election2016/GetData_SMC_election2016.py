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


from twython import Twython

import sys
sys.path.insert(0, './Imports') #adds Imports folder to path
from Keys import * #import all variables stored in Imports/Keys.py 

def get_data_search(kid, max_id=None):
    try:
        #d = simplejson.loads(urllib.urlopen(url % (kid, page)).read())  #3/24/2013 - THIS IS THE PREVIOUS VERSION
        '''
        NOTES ON 'count' -- Specifies the number of tweets to try and retrieve, up to a maximum of 100 per distinct request. 
        The value of count is best thought of as a limit to the number of tweets to return because suspended or 
        deleted content is removed after the count has been applied. 
        
        https://dev.twitter.com/docs/api/1.1/get/search/tweets
        
        'count' = 'The number of tweets to return per page, up to a maximum of 100. Defaults to 15.'
        '''
        d = twitter.search(q=kid, count = '100', result_type = 'recent', max_id = max_id) #'354722821986979839') #max_id)
        
    except Exception, e:
        print "Error reading id %s, exception: %s" % (kid, e)
        return None
        
    print "######## # OF STATUSES IN THIS GRAB: ", len(d['statuses'])
    print "max_id VALUE USED FOR THIS GRAB-->", max_id
    return d
    
    
def get_data_user_timeline(kid):
    try:        
        '''
        'count' specifies the number of tweets to try and retrieve, up to a maximum of 200 per distinct request. 
        The value of count is best thought of as a limit to the number of tweets to return because suspended or 
        deleted content is removed after the count has been applied. We include retweets in the count, 
        even if include_rts is not supplied. It is recommended you always send include_rts=1 when using this API method.
        '''
        #d = t.getUserTimeline(screen_name=kid, count="200", page="1", include_entities="true", include_rts="1")  #NEW LINE (OLD VERSION)
        d = twitter.get_user_timeline(screen_name=kid, count="200", page="1", include_entities="true", include_rts="1")  #NEW LINE        
    except Exception, e:
        print "Error reading id %s, exception: %s" % (kid, e)
        return None

    return d
    

def get_data_user_timeline_all_pages(kid, page):
    try:        
        '''
        'count' specifies the number of tweets to try and retrieve, up to a maximum of 200 per distinct request. 
        The value of count is best thought of as a limit to the number of tweets to return because suspended or 
        deleted content is removed after the count has been applied. We include retweets in the count, 
        even if include_rts is not supplied. It is recommended you always send include_rts=1 when using this API method.
        '''
        d = twitter.get_user_timeline(screen_name=kid, count="200", page=page, include_entities="true", include_rts="1")          
    except Exception, e:
        print "Error reading id %s, exception: %s" % (kid, e)
        return None
 
    return d
    
 
def get_followers_ids(kid, cursor):
    """
    cursor = -1 IS THE 'FIRST PAGE'
    """
    try:        
        d = twitter.get_followers_ids(screen_name=kid, count="5000", cursor=cursor, stringify_ids="true")  #NEW LINE        
    except Exception, e:
        print "Error reading id %s, exception: %s" % (kid, e)
        return None
    return d
