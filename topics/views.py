from django.shortcuts import render, get_object_or_404, redirect
from topics.models import Subject, Topic, VocabWord, Link, PracticeProblem, Information    

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