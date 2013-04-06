# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response
from core.models import News, Photo, Gallery, Movie, Day, Sponsor, About,\
    Contact, Event, Sentence, GuestMeeting, NewsPage, MediaPatron, HonorPatron,\
    Partner
from django.utils.safestring import mark_safe
from django.http import HttpResponse
import random
def merge( _list1, _list2 ):
    _list = []
    i = 0
    j = 0
    while i < len( _list1 ) and j < len( _list2 ) :
        if _list1[ i ].publish_date > _list2[ j ].publish_date:
            _list.append( _list1[ i ] )
            i += 1
        else:
            _list.append( _list2[ j ] )
            j += 1
    while i < len( _list1 ):
        _list.append( _list1[i] )
        i += 1
    while j < len( _list2 ):
        _list.append( _list2[j] )
        j += 1
    return _list
    
def homepage( request ):
    data = {}
    _list = []
    tmp1 = News.objects.filter( homepage = True ).order_by("-publish_date")
    tmp2 = Photo.objects.filter( homepage = True ).order_by("-publish_date")
    _list = merge( tmp1, tmp2 )
    _list = merge( _list, Gallery.objects.filter( homepage = True ).order_by("-publish_date") )
    _list = merge( _list, Movie.objects.filter( homepage = True ).order_by("-publish_date") )
    data["list"] = _list
    return render_to_response( "core/homepage.html", data )
def newspage( request, name ):
    data = {}
    np = NewsPage.objects.get( name = name )
    np.news.show_title = False
    np.news.show_date = False
    data["item"] = np.news
    data["name"] = np.name
    return render_to_response( "core/newspage.html", data )

def dayView( request, id, name ):
    day = Day.objects.get( nr = id )
    data = {}
    _list = []
    tmp1 = News.objects.filter( day = day )
    tmp2 = Photo.objects.filter( day = day )
    _list = merge( tmp1, tmp2 )
    _list = merge( _list, Gallery.objects.filter( day = day ) )
    _list = merge( _list, Movie.objects.filter( day = day ) )
    data["day"] = day
    data["guests"] = GuestMeeting.objects.filter( day = day ).order_by("hour_begin").order_by("order")
   
    data["events"] = Event.objects.filter( day = day ).order_by("hour_begin")
    data["list"] = _list
    return render_to_response( "core/day.html", data )
def guests( request ):
    data = {}
    _days = Day.objects.all().order_by("date")
    days = []
    for day in _days:
        day.guests = GuestMeeting.objects.filter( day = day ).order_by("order")
        days.append( day )
    data["days"] = days
    
    return render_to_response( "core/guests.html", data )
def sponsors( request ):
    data = {
            "sponsors" : Sponsor.objects.all().order_by("order"),
            "mpatrons" : MediaPatron.objects.all().order_by("order"),
            "hpatrons" : HonorPatron.objects.all().order_by("order"),
            "partners" : Partner.objects.all().order_by("order"),
            }
    return render_to_response( "core/sponsors.html", data )
def sponsors2( request ):
    html =""
    list = Sponsor.objects.all().order_by("order")
            
    for item in list :
        html += """
        <div class="flash_sponsor">
            <img src="/media/{url}" />
        </div>
    """.format(  url = item.image )
    return HttpResponse( html )
def sponsor( request, nr = None ):
    s = Sponsor.objects.all()
    l = len( s )
    if nr is None:
        nr = random.randint( 0, l-1 )
    else:
        nr = ( nr + 1 ) % l
    html = """
        <div class="flash_sponsor">
            <img src="/media/{url}" />
            <a href="/sponsor/{nr}"></a>
        </div>
    """.format( nr = nr, url = s[nr].image )
    return HttpResponse( html )

def about( request ):
    data = {
            "list" : About.objects.all().order_by("order")
            }
    return render_to_response( "core/about.html", data )

def contact( request ):
    data = {
            "list" : Contact.objects.all().order_by("order")
            }
    return render_to_response( "core/contact.html", data )

def galleries( request ):
    data = {
            "list" : Gallery.objects.all().order_by("-publish_date")
            }
    return render_to_response( "core/galleries.html", data )

def gallery( request, id, name ):
    data = {
            "gallery" : Gallery.objects.get( id = id ),
            }
    data["list"] = data["gallery"].photos.all().order_by("-publish_date")
    return render_to_response( "core/gallery.html", data )

def sentence( request, nr = None ):
    s = Sentence.objects.all()
    if len( s ) == 0:
        return HttpResponse( "" )
    if nr is None:
        nr = random.randint( 0 , len( s )  - 1 )
    else:
        nr = int( nr )
        nr = ( nr + 1 ) % len( s )
    response = u"""
            <div class="stext">{text}<div class="sauthor">{author}</div></div>
            
            <a href="/sentence/{nr}"></a>
    """.format(
               text = unicode( s[nr].text ),
               author = s[nr].author,
               nr = nr
               )
    return HttpResponse( response )
    
