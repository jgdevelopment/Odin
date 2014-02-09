from django.shortcuts import render, get_object_or_404, redirect
from topics.models import Subject, Topic, VocabWord, Link, PracticeProblem, Information
import urllib
import json
import base64
import pprint
import sys

def all_topics(request):
    def render_page(subjects):
        params = {'subjects': subjects}
        return render(request, 'topics/all_topics.html', params)
    '''
    each item in the 'subjects' list is a 2-item list.
    the first item is the name of the subject, and the other is the topics under that subject
    '''
    subjects = []
    for subject in Subject.objects.order_by('name'):
        elem = []
        elem.append(subject.name)
        elem.append(Topic.objects.filter(subject=subject).order_by('name'))
        subjects.append(elem)
    return render_page(subjects)
    
def view_topic(request,slug):
    def render_page(name, vocab_words, links, practice_problems, information):
        params = {'name': name,
                  'vocab_words': vocab_words,
                  'links': links,
                  'practice_problems': practice_problems,
                  'information': information}
        return render(request, 'topics/view_topic.html', params)
        
    topic = get_object_or_404(Topic, slug=slug)
    vocab_words = VocabWord.objects.filter(topic=topic)
    links = Link.objects.filter(topic=topic)
    practice_problems = PracticeProblem.objects.filter(topic=topic)
    information = Information.objects.filter(topic=topic)
    return render_page(topic.name, vocab_words, links, practice_problems, information)

def generate_topic(request):
    resp = _bing_api_call('chocolate')
    print(resp)
    return redirect('http://google.com/')

# return list of links
def _bing_api_call(search_term):
    auth = str(base64.b64encode(b'GADjTrr1YGG7uFx58yNvkuJNUTEN7s6++SnOiOnwaYM:GADjTrr1YGG7uFx58yNvkuJNUTEN7s6++SnOiOnwaYM'), 'utf-8')
    header = {'Authorization': 'Basic ' + auth}
    url = 'https://api.datamarket.azure.com/Bing/Search/Web?$format=json'
    data = {'Query': "'" + search_term + "'"}
    data = urllib.parse.urlencode(data)
    request = urllib.request.Request(url + '&' + data, None, header)
    request_open = urllib.request.urlopen(request)
    response = request_open.read()
    request_open.close()
    parsed = json.loads(response.decode('utf-8'))
    links = []
    for entry in parsed['d']['results']:
        links.append(str(entry['Url']))
    return links

# returns list of VocabularyWord
def _vocab_words(topic):
    vocab_words = []
    resp = _quizlet_api_call('https://api.quizlet.com/2.0/search/sets', {'q':topic})
    id = resp['sets'][0]['id']
    cards = _quizlet_api_call('https://api.quizlet.com/2.0/sets/' + str(id), {})['terms']
    for card in cards:
        vocab_words.append(VocabWord(word=card['term'], definition=card['definition']))
    return vocab_words
    
def _quizlet_api_call(url, params):
    data = {'client_id': 'nCscNPXHRC'}
    data.update(params)
    data = urllib.parse.urlencode(data)
    request = urllib.request.Request(url + '?' + data)
    request_open = urllib.request.urlopen(request)
    response = request_open.read()
    request_open.close()
    return json.loads(response.decode('utf-8'))