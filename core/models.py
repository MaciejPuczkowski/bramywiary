# -*- coding: utf-8 -*-
from django.db import models
from django.template.defaultfilters import title
from datetime import datetime
from django.contrib import admin
from django.utils.safestring import mark_safe
from core.managers import ContentManager
from DniWiary.settings import STATIC_URL, MEDIA_URL, MEDIA_ROOT, THUMBNAIL_WIDTH,\
    THUMBNAIL_HEIGHT
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
import Image
from django.utils.formats import localize
import re
import templatetags.formatting as formatting

# Create your models here.

class Day( models.Model ):
    class Meta:
        verbose_name = "Dzień"
        verbose_name_plural = "Dni"
    nr = models.SmallIntegerField()
    title = models.CharField( max_length = 64 )
    description = models.TextField( null = True, blank = True )
    date = models.DateField()
    def __unicode__(self):
        return self.title

class Event( models.Model ):
    class Meta:
        verbose_name = "Punkt programu"
        verbose_name_plural = "Punkty programu"
    title = models.CharField( max_length = 255 )
    day = models.ForeignKey( Day )
    hour_begin = models.TimeField()
    hour_end = models.TimeField()
    description = models.TextField( null = True, blank = True )
    place = models.CharField( max_length = 255, default = '',null = True, blank = True )
    def __unicode__(self):
        return self.title

class Content( models.Model ):
    day = models.ForeignKey( Day, null = True, blank = True ) 
    title = models.CharField( max_length = 255 )
    show_title = models.BooleanField( default = True )
    author = models.CharField( max_length = 64, blank = True, null = True )
    show_author = models.BooleanField( default = True )
    publish_date = models.DateTimeField( default = datetime.now(), null = True, blank = True )
    show_date = models.BooleanField( default = True )
    description = models.TextField( null = True, blank = True )
    show_description = models.BooleanField( default = True )
    homepage = models.BooleanField( default = False )
    hidden = models.BooleanField( default = False )
    objects = ContentManager()
    def show(self):
        html = ""
        if self.show_title and self.title is not None: 
            html += '<div class="title">%s</div>' %self.title
        if self.show_author and self.author is not None: 
            html += '<div class="author">Autor:&nbsp;%s</div>' %self.author
        if self.show_date and localize( self.publish_date ) is not None: 
            html += '<div class="date">%s</div>' %localize( self.publish_date )
        if self.show_description and self.description is not None: 
            html += '<div class="description">%s</div>' %self.description
        
        return mark_safe( html )
        
          
    def __unicode__(self):
        return self.title
class News( Content ):
    class Meta:
        verbose_name = "News"
        verbose_name_plural = "Newsy"
    text = models.TextField()
    objects = ContentManager()
    def show(self):
        html = '<div class="news">'
        if self.show_title and self.title: 
            html += '<div class="title">%s</div>' %self.title
        html += '<div class="text">%s</div>' % formatting.format( self.text )
        if self.show_author and self.author: 
            html += '<div class="author">Autor:&nbsp;%s</div>' %self.author
        if self.show_date and self.publish_date : 
            html += '<div class="date">%s</div>' %localize( self.publish_date )
        html +='<div class="clearer"></div>'
        html += '</div>'
        return mark_safe( html )
class NewsPage( models.Model ):
    class Meta:
        verbose_name = "Strona z newsa"
        verbose_name_plural = "Strony z newsów"
    name = models.CharField( max_length = 255 )
    news = models.ForeignKey( News )
    def __unicode__(self):
        return self.name
    
class Photo( Content ):
    class Meta:
        verbose_name = "Zdjęcie"
        verbose_name_plural = "Zdjęcia"
    image = models.ImageField( upload_to = "photo/")
    objects = ContentManager()
    def show(self):
        html = '<div class="singlephoto">'
        if self.show_title and self.title : 
            html += '<div class="title">%s</div>' %self.title
        html += '<img  src="/media/%s" />' %self.image
        if self.show_author and self.author: 
            html += '<div class="author">Autor:&nbsp;%s</div>' %self.author
        if self.show_date and self.publish_date : 
            html += '<div class="date">%s</div>' %localize( self.publish_date )
        html += '<div class="clearer"></div>'
        if self.show_description and self.description: 
            html += '<div class="description">%s</div>' %self.description
        html += '</div>'
        return mark_safe(  html  )

class Gallery( Content ):
    class Meta:
        verbose_name = "Galeria"
        verbose_name_plural = "Galerie"
    photos = models.ManyToManyField( Photo )
    objects = ContentManager()
    def show(self):
        photos = self.photos.all().order_by( "-publish_date" )[:4]
        width = 200 * len( photos )
        html = '<div class="gallery short" ><div class="title">' 
        if self.show_title and self.title : 
            html +=  self.title
        html += '</div>'
        html +='<div class="list" style="width:%dpx;margin-left:auto;margin-right:auto;">' % width
        for photo in photos:
            src = unicode( photo.image ) 
            html += '<a rel="prettyPhoto[pp_gal]" title="{description}" href="/media/{image}" ><img  src="/media/thumbnails/{image}" /></a>'\
            .format( description = photo.description, image = src )
        html +='<div class="clearer"></div>'
        html += '</div>'
        if self.photos.count() > 4:
            
            html += '<a href="/gallery,%d,%s.html" class="more">Zobacz całą galerię.</a>'  % ( self.id, self.title )
        html +='<div class="clearer"></div>'
        if self.show_description and self.description: 
            html += '<div class="description">%s</div>' %self.description
        if self.show_author and self.author : 
            html += '<div class="author">Autor:&nbsp;%s</div>' %self.author
        if self.show_date and self.publish_date: 
            html += '<div class="date">%s</div>' % localize( localize( self.publish_date ) )
        html +='<div class="clearer"></div>'
        html += "</div>"
       
        return mark_safe( html )
        

class Movie( Content ):
    class Meta:
        verbose_name = "Film"
        verbose_name_plural = "Filmy"
    url = models.CharField( max_length = 1024 )
    objects = ContentManager()
    def show(self):
        if self.show_title:
            title = self.title
        else:
            title = ""
        html =' <div class="movie">'
        html += """
       
        <div class="title">{title}</div>
        <div class="clearer"></div>
        <div class="movie_object">
            <iframe width="640" height="390" src="{url}?wmode=opaque" frameborder="0" allowfullscreen></iframe>
        </div>
        
        """.format(
                   title = title,
                   url = self.url
                   )
        if self.show_author and self.author: 
            html += '<div class="author">Autor:&nbsp;%s</div>' %self.author
        if self.show_date and localize( self.publish_date ) : 
            html += '<div class="date">%s</div>' %localize( self.publish_date )
        html +='<div class="clearer"></div>'
        if self.show_description and self.description : 
            html += '<div class="description">%s</div>' %self.description
        html += '</div>'
        return mark_safe( html )
 
    
class About( models.Model ):
    class Meta:
        verbose_name = "O nas"
        verbose_name_plural = "O nas"
    text = models.ForeignKey( News, null = True, blank = True )
    photo = models.ForeignKey( Photo, null = True, blank = True )
    gallery = models.ForeignKey( Gallery , null = True, blank = True )
    movie = models.ForeignKey( Movie, null = True, blank = True )
    choice = models.CharField( max_length = 8, choices = ( 
                                                          ( "text", "Text" ), 
                                                          ( "photo", "Photo" ),
                                                          ( "gallery", "Gallery" ), 
                                                          ( "movie", "Movie" ),  
                                                          ) )
    order = models.IntegerField( max_length = 11, default = 0 )
    def __unicode__(self):
        name = unicode( self.order )
        if self.choice == "text" and self.text is not None:
            name = self.text.title
        if self.choice == "photo" and self.photo is not None:
            name = self.photo.title
        if self.choice == "gallery" and self.gallery is not None:
            name = self.gallery.title
        if self.choice == "movie" and self.movie is not None:
            name = self.movie.title
        return name
    def show(self):
        if self.choice == "text" and self.text is not None:
            return self.text.show()
        if self.choice == "photo" and self.photo is not None:
            return self.photo.show()
        if self.choice == "gallery" and self.gallery is not None:
            return self.gallery.show()
        if self.choice == "movie" and self.movie is not None:
            return self.movie.show()
        return ""
    
class Contact( models.Model ):
    class Meta:
        verbose_name = "Kontakt"
        verbose_name_plural = "Kontakty"
    name = models.CharField( max_length = 255 )
    order = models.IntegerField( max_length = 11, default = 0 )
    phone = models.CharField( max_length = 64, null = True, blank = True )
    email = models.CharField( max_length = 64, null = True, blank = True )
    skype = models.CharField( max_length = 64, null = True, blank = True )
    gg = models.CharField( max_length = 64, null = True, blank = True )
    street = models.CharField( max_length = 64, null = True, blank = True )
    house_no = models.CharField( max_length = 64, null = True, blank = True )
    flat_no = models.CharField( max_length = 64, null = True, blank = True )
    postal_code = models.CharField( max_length = 64, null = True, blank = True )
    city = models.CharField( max_length = 64, null = True, blank = True )
    def __unicode__(self):
        return self.name
    def show(self):
        html = '<div class="title">%s</div>' % self.name
        if self.phone : 
            html += '<div class="contact phone"><h3>Telefon: </h3><span>%s</span></div>' % self.phone
        if self.email : 
            html += '<div class="contact email"><h3>E-Mail: </h3><span>%s</span></div>' % self.email
        if self.skype : 
            html += '<div class="contact skype"><h3>Skype: </h3><span>%s</span></div>' % self.skype
        if self.gg : 
            html += '<div class="contact gg"><h3>gg: </h3><span>%s</span></div>' % self.gg
        if self.street  and  self.house_no: 
            html += '<div class="contact  address street"><h3></h3><span>%s</span></div>' % self.street
            html += '<div class="contact  address house"><h3></h3><span>%s</span></div>' % self.house_no
        if self.house_no and self.flat_no: 
            html += '<div class="contact  address flat"><h3>/</h3><span>%s</span></div>' % self.flat_no
        if self.postal_code  and self.city : 
            html += '<div class="clearer"></div><div class="contact  address postal"><h3></h3><span>%s</span></div>' % self.postal_code
        if self.city: 
            html += '<div class="contact  address city"><h3></h3><span>%s</span></div>' % self.city
        return mark_safe( html )
    
#Sponsor powinien dziedziczyc po Patronie, ale ze wzgledu na integralnosc bazy ktora powstaje online musi zostac tak jak jest.
#Na przyszlosc trzeba poprawic.
class Sponsor( models.Model ):
    class Meta:
        verbose_name = "Sponsor"
        verbose_name_plural = "Sponsorzy"
    name = models.CharField( max_length = 255 )
    image = models.ImageField( upload_to = "upload/logos/", null = True, blank = True )
    description = models.TextField( null = True, blank = True  )
    order = models.IntegerField( max_length = 11, default = 0 )
    url = models.CharField( max_length = 1024 )
    def __unicode__(self):
        return self.name
    
class Patron( models.Model ):
    class Meta:
        verbose_name = "Patron"
        verbose_name_plural = "Patroni"
    name = models.CharField( max_length = 255 )
    image = models.ImageField( upload_to = "upload/logos/", null = True, blank = True )
    url = models.CharField( max_length = 1024 )
    description = models.TextField( null = True, blank = True  )
    order = models.IntegerField( max_length = 11, default = 0 )
    def __unicode__(self):
        return self.name
    
class MediaPatron( Patron ):
    class Meta:
        verbose_name = "Patron medialny"
        verbose_name_plural = "Patroni medialni"
        
class HonorPatron( Patron ):
    class Meta:
        verbose_name = "Patron honorowy"
        verbose_name_plural = "Patroni honorowy"        
class Organizer( Patron ):
    class Meta:
        verbose_name = "Organizator"
        verbose_name_plural = "Organizatorzy"  
class Partner( Patron ):
    class Meta:
        verbose_name = "Partner"
        verbose_name_plural = "Partnerzy"

    
class GuestMeeting( models.Model ):
    class Meta:
        verbose_name = "Spotkanie z gościem"
        verbose_name_plural = "Spotkania z goścmi"
    day = models.ForeignKey(Day)
    hour_begin = models.TimeField()
    hour_end = models.TimeField( null = True, blank = True );
    place = models.CharField( max_length = 255, null = True, blank = True )
    guest = models.ForeignKey("Guest")
    order = models.IntegerField( max_length = 11, default = 0 )
    def __unicode__(self):
        return self.guest.name + " " + self.day.title
    
class Guest( models.Model ):
    class Meta:
        verbose_name = "Gość"
        verbose_name_plural = "Goście"
    name = models.CharField( max_length = 255 )
    description = models.TextField( null = True, blank = True  )
    def __unicode__(self):
        return self.name

class Sentence( models.Model ):
    text = models.CharField( max_length = 2048 )
    author = models.CharField( max_length = 255 )
    def __unicode__(self):
        return self.text
import math
@receiver( post_save, sender = Photo )
def make_thumbnail( sender, instance, **kwargs ):
    print instance
    img = Image.open( MEDIA_ROOT + unicode( instance.image ) ).copy()
    x1, y1, width, height = img.getbbox()
    w = THUMBNAIL_WIDTH
    h = THUMBNAIL_HEIGHT
    i = 1
    while True:
        if w + THUMBNAIL_WIDTH >  width or h + THUMBNAIL_HEIGHT > height:
            height = h
            width = w
            break
        w += THUMBNAIL_WIDTH
        h += THUMBNAIL_HEIGHT
    
    
       
    
    img = img.crop( ( 0 , 0 , width, height) )
    img.load()
    img.thumbnail( (200, 150 ) )
    img.save( MEDIA_ROOT + "thumbnails/" + unicode( instance.image ), "jpeg" )

@receiver( pre_save, sender = Movie )
def youtube_url_parse( sender, instance, **kwargs ):
    id_ = re.findall( "youtu.be/(\w+)", instance.url )

    if len( id_ ) == 0:
        id_ = re.findall( "www.youtube.com/watch\?v=(\w+)", instance.url )
    if len( id_ ) == 0:
        id_ = re.findall( "www.youtube.com/v/(\w+)", instance.url )
    if len( id_ ) == 0:
        id_ = re.findall( "www.youtube.com/embed/(\w+)", instance.url )
    if len( id_ ) == 0:
        id_ = ["#"]
    print id_
    instance.url = "http://www.youtube.com/embed/" + id_[0]
 
 
admin.site.register( NewsPage )     
admin.site.register( Sentence ) 
admin.site.register( Day )  
admin.site.register( Event )  
admin.site.register( News )  
admin.site.register( Photo )  
admin.site.register( Gallery )  
admin.site.register( Movie )
admin.site.register( About )    
admin.site.register( Contact )  
admin.site.register( Sponsor )  
admin.site.register( HonorPatron )
admin.site.register( MediaPatron )
admin.site.register( Partner )      
admin.site.register( Guest )  
admin.site.register( GuestMeeting )  