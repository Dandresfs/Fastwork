from social.backends.facebook import FacebookOAuth2
from social.backends.google import GoogleOAuth2
from social.backends.linkedin import LinkedinOAuth2
from accounts.backends import TwitterOAuth
import urllib2
from urllib import urlencode
from io import BytesIO
from django.core.files import File
from urlparse import urlparse, urlunparse, parse_qs



def save_profile_picture(backend, user, response, details, is_new=False, *args, **kwargs):

    if isinstance(backend, FacebookOAuth2):
        url = 'http://graph.facebook.com/{0}/picture?width=1000'.format(response['id'])
        response = urllib2.urlopen(url)
        io = BytesIO(response.read())
        user.photo.save('profile_pic_{}.jpg'.format(user.pk), File(io))
        user.save()

    if isinstance(backend, TwitterOAuth):
        if response.get('profile_image_url'):
            url = response.get('profile_image_url').replace('_normal','')
            response = urllib2.urlopen(url)
            io = BytesIO(response.read())
            user.photo.save('profile_pic_{}.jpg'.format(user.pk), File(io))
            user.save()

    if isinstance(backend, GoogleOAuth2):
        if response.get('image') and response['image'].get('url'):
            url = response['image'].get('url')
            u = urlparse(url)
            query = parse_qs(u.query)
            query.pop('sz', None)
            u = u._replace(query=urlencode(query, True))
            url = urlunparse(u)
            response = urllib2.urlopen(url)
            io = BytesIO(response.read())
            user.photo.save('profile_pic_{}.jpg'.format(user.pk), File(io))
            user.save()

    if isinstance(backend, LinkedinOAuth2):
        if response.get('pictureUrls') and response['pictureUrls'].get('values') and response['pictureUrls']['values'][0]:
            url = response['pictureUrls']['values'][0]
            response = urllib2.urlopen(url)
            io = BytesIO(response.read())
            user.photo.save('profile_pic_{}.jpg'.format(user.pk), File(io))
            user.save()