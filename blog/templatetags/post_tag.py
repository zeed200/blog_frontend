from django import template
import requests

register = template.Library()
# @register.inclusion_tag('blog/base.html')
@register.simple_tag()

def latest_post():
    backend_url = "http://127.0.0.1:8000/"
    headers = {'Content-Type':"application/json"}
    response = requests.get(backend_url,headers=headers)
    posts = response.json()
    
    # context = {
    #     'l_posts': posts[0:5]
    # }
    return posts[0:5]