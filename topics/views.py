from django.shortcuts import render, get_object_or_404, redirect
from topics.models import Subject, Topic, VocabWord, Link, PracticeProblem, Information
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse

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
    def render_page(name, vocab_words, links, practice_problems, information, slug):
        params = {'name': name,
                  'vocab_words': vocab_words,
                  'links': links,
                  'practice_problems': practice_problems,
                  'information': information,
                  'slug': slug}
        return render(request, 'topics/view_topic.html', params)
        
    topic = get_object_or_404(Topic, slug=slug)
    vocab_words = VocabWord.objects.filter(topic=topic)
    links = Link.objects.filter(topic=topic)
    practice_problems = PracticeProblem.objects.filter(topic=topic)
    information = Information.objects.filter(topic=topic)
    return render_page(topic.name, vocab_words, links, practice_problems, information, topic.slug)

def create_topic(request):
    def render_page():
        params = {'all_subjects':Subject.objects.all()}
        return render(request, 'topics/create_topic.html', params)
        
    if request.method == 'POST':
        subject_name = request.POST.get('subject')
        topic_name = request.POST.get('topic')
        
        if not Topic.objects.filter(name=topic_name):
            subj = Subject.objects.get(name=subject_name)
            topic = Topic.create(topic_name, subj)
            topic.save()
            
            for vocab in _vocab_words(topic_name):
                vocab.topic = topic
                vocab.save()
                
            for link in _bing_api_call(topic_name):
                link.topic = topic
                link.save()
        else:
            topic = Topic.objects.get(name=topic_name)
        return HttpResponseRedirect(reverse('topics.views.view_topic', args=(topic.slug,)))
    else:
        return render_page()
        
def add_vocab(request, topic_slug):
    topic = Topic.objects.get(slug=topic_slug)

    def render_page():
        params = {'topic_name': topic.name}
        return render(request, 'topics/add_vocab.html', params)
    
    if request.method == 'POST':
        word = request.POST.get('word')
        definition = request.POST.get('definition')
        if not VocabWord.objects.filter(word=word).exists():
            vocab = VocabWord(word=word, definition=definition)
            vocab.topic = topic
            vocab.save()
        return HttpResponseRedirect(reverse('topics.views.view_topic', args=(topic.slug,)))
    else:
        return render_page()

def add_link(request, topic_slug):
    topic = Topic.objects.get(slug=topic_slug)

    def render_page():
        params = {'topic_name': topic.name}
        return render(request, 'topics/add_link.html', params)
    
    if request.method == 'POST':
        url = request.POST.get('url')
        description = request.POST.get('description')
        if not Link.objects.filter(url=url).exists():
            link = Link(url=url, description=description)
            link.topic = topic
            link.save()
        return HttpResponseRedirect(reverse('topics.views.view_topic', args=(topic.slug,)))
    else:
        return render_page()
    
def add_information(request, topic_slug):
    print(topic_slug)
    topic = Topic.objects.get(slug=topic_slug)

    def render_page():
        params = {'topic_name': topic.name}
        return render(request, 'topics/add_information.html', params)
    
    if request.method == 'POST':
        subtopic = request.POST.get('subtopic')
        information = request.POST.get('information')
        if not Information.objects.filter(subtopic=subtopic).exists():
            info = Information(subtopic=subtopic, info=information)
            info.topic = topic
            info.save()
        return HttpResponseRedirect(reverse('topics.views.view_topic', args=(topic.slug,)))
    else:
        return render_page()
    
def add_problem(request, topic_slug):
    topic = Topic.objects.get(slug=topic_slug)

    def render_page():
        params = {'topic_name': topic.name}
        return render(request, 'topics/add_problem.html', params)
    
    if request.method == 'POST':
        question = request.POST.get('question')
        answer = request.POST.get('answer')
        if not PracticeProblem.objects.filter(question=question).exists():
            problem = PracticeProblem(question=question, answer=answer)
            problem.topic = topic
            problem.save()
        return HttpResponseRedirect(reverse('topics.views.view_topic', args=(topic.slug,)))
    else:
        return render_page()

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
        link = Link(url=entry['Url'], description=entry['Description'])
        links.append(link)
    return links[:10]

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