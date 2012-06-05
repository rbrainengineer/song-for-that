"""
conceptnet5client is a simple client for interacting with ConceptNet 5's REST API
"""

import urllib, urllib2

try:
    import json
except:
    import simplejson as json

API_URL = 'http://conceptnet5.media.mit.edu/data/5.1/assoc/list/en/'
EN_TAG = '/c/en/'

def similar_to_concept5(concept, limit=5):
    result = similar_to_concept_core(concept, limit)
    # results look like
    #{u'similar': [[u'/c/en/toast', 0.9983175619906641],
    #[u'/c/en/sourdough', 0.9828311967828328],
    #[u'/c/fr/galette', 0.978226269867747]],
    #u'terms': [[u'/c/en/toast', 1.0]]}
    print result
    terms = map(lambda x:x[0], result['similar'])
    enterms = filter(lambda x:x.startswith(EN_TAG), terms)
    cleanedterms = map(lambda x:x.split('/')[-1], enterms)
    asciiterms = map(lambda x:x.encode('ascii','ignore'), cleanedterms)
    return map(lambda x:x.replace('_', ' '), asciiterms)

def similar_to_concept_core(conceptstr, limit):
    limitstr = 'limit=%d' %limit
    filterstr = 'filter=/c/en'
    return _get_json(conceptstr, limitstr, filterstr)

def _get_json(conceptstr, *arg_parts):
    url = API_URL + conceptstr+'?'+'&'.join(p for p in arg_parts)
    return json.loads(_get_url(url))

def _get_url(url):
    conn = urllib2.urlopen(url)
    return conn.read()
