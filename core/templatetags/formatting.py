# -*- coding: utf-8 -*-
from django import template

from django.utils.safestring import mark_safe
import re
register = template.Library()


def template_function( function ):
    function = function.strip()
    
    if function == "list":
        return '<ul class="dot">'
    if function == "enumerate":
        return '<ul class="enum">'
    if function == "/list":
        return "</ul>"
    if function == "/enumerate":
        return "</ul>"
    if function == "item":
        return "<li>"
    if function == "/item":
        return "</li>"
    if function == "bold":
        return "<b>"
    if function == "/bold":
        return "</b>"
    if function == "strong":
        return "<strong>"
    if function == "/strong":
        return "</strong>"
    if function == "italic":
        return "<i>"
    if function == "/italic":
        return "</i>"
    
    if function[:5] == "image":
        matched = re.search('image="(.*?)"' , function )
        if matched is not None:
            ret = '<img src="%s"' % matched.group(1)
            matched = re.search('alt="(.*?)"' , function )
            if matched is not None:
                ret += ' alt="%s" ' % matched.group(1)
            matched = re.search('class="(.*?)"' , function )
            if matched is not None:
                ret += ' class="inline_photo %s" style="display:inline" ' % matched.group(1)
            else:
                ret += ' class="inline_photo"  ' 
            ret += " />"
            return ret
    if function[:4] == "link":
        matched = re.search('link="(.*?)"' , function )
        if matched is not None:
            url = matched.group(1)
            ret = '<a href="%s">' % url
            matched = re.search('display="(.*?)"' , function )
            if matched is not None:
                ret +=  matched.group(1)
            else:
                ret+= url
            ret += "</a>"
            return ret
            
    return ""
   
    
def format( text ):
    new_text = ""
    paragraph = False
    for line in text.split("\n"):
        line = line.strip()
        
        if len( line ) > 0:
            if not  paragraph:
                paragraph = True
                new_text += "<p>"
                
            if  not ( line[:2] == "{%" and line[-2:] == "%}" ) :
                new_text += line + "</br>"
            else: 
                new_text += line + "\n"
        else:
            if paragraph:
                new_text += "</p>"
                paragraph = False
    
    if paragraph:
        new_text += "</p>"
   
    pattern = re.compile("{%(.*?)%}", re.DOTALL)
    result = re.search( pattern, new_text )
    while result is not None:
        p = result.group(0)
        print p
        print template_function(  result.group(1) )
        new_text = re.sub( re.escape(p) , template_function(  result.group(1) ),new_text ) 
        
        result = re.search( pattern, new_text )
    
    return mark_safe( new_text )
        
    
register.filter('format', format) 

