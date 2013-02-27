import urllib, urllib2, simplejson, webbrowser

def pretty(obj):
    return simplejson.dumps(obj, sort_keys=True, indent=2)

def safeGet(url):
    try:
        return urllib2.urlopen(url)
    except urllib2.URLError, e:
        if hasattr(e,'reason'):
            print "We failed to reach a server"
            print "Reason", e.reason
        elif hasattr(e,"code"):
            print "The server couldn't fulfill the request."
            print "Error code: ", e.code
        return None
    
#returns JSON dictionary of trending topics for a given location id
def searchTweets(id, format="json"):
    baseurl = 'https://api.twitter.com/1/trends/'
    url = baseurl + str(id) + '.' + format
    result = safeGet(url) 
    jsonresult = result.read()
    d = simplejson.loads(jsonresult)
    return d    

#returns JSON dictionary of location data for a given location name
def findLocation(name, format = 'json'):
    baseurl = 'http://where.yahooapis.com/v1/places.q('
    yahooAPI = 'jFxIVPTV34FaFl2zXpuiwH5HgeWL_lHTd3CwSoABldlQSJaLBuFlu5YrLB9gPe_Ed8qHkJgNtkM3i0jtJ3zuTKRZwaRVO8Y-'
    params = {}
    params['appid'] = yahooAPI
    params['format'] = format
    url = baseurl + urllib.quote(name) + ')?' + urllib.urlencode(params)
    result = safeGet(url)
    jsonresult = result.read()
    d = simplejson.loads(jsonresult)
    return d

#returns JSON dictionary of news results for a given topic
def getNewsResult(topic):
    baseurl = 'https://ajax.googleapis.com/ajax/services/search/news?v=1.0&'
    params = {}
    params['q'] = topic
    url = baseurl + urllib.urlencode(params)
    result = safeGet(url)
    jsonresult = result.read()
    d = simplejson.loads(jsonresult)
    return d

print 'Please enter the name of the nearest city/town to you,'

location = raw_input('Keep in mind bigger cities work best: ')
location_data = findLocation(location)
 
location_id = location_data['places']['place'][0]['locality1 attrs']['woeid'] 
trend_dict = searchTweets(location_id)
tweets = trend_dict[0]['trends']
tweet_list = []

print '\nHere is a list of trending topics for ' + location + ':'

for trend in range(len(tweets)):
    s = str(trend + 1) + '. '
    s += tweets[trend]['name']
    print s
    tweet_list.append(tweets[trend]['name'])

print '-------------'
print '\nPlease select the number of the corresponding trending topic from above that you want to read about.'
print 'After making a selection, you will be taken news results from Google News.'

choice = input('Selection: ')
news = getNewsResult(tweet_list[choice - 1])
news_url = news['responseData']['cursor']['moreResultsUrl']
webbrowser.open(news_url)
 