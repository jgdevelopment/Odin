from django import template
import markdown2
import html.parser

register = template.Library()

def markdown(value):
    str = markdown2.markdown(value)
    return str
 
register.filter('markdown', markdown)