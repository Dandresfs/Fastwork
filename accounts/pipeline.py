from social.backends.facebook import FacebookOAuth2
from social.backends.google import GoogleOAuth2
from social.backends.linkedin import LinkedinOAuth2
from accounts.backends import TwitterOAuth
from urllib import urlencode
from urlparse import urlparse, urlunparse, parse_qs
from mail_templated import send_mail
from Fastwork.settings.base import DEFAULT_FROM_EMAIL

def user_details(strategy, details, user=None, *args, **kwargs):
    """Update user details using data from provider."""
    if user:
        changed = False  # flag to track changes
        protected = ('username', 'id', 'pk', 'email') + \
            tuple(strategy.setting('PROTECTED_USER_FIELDS', []))

        # Update user model attributes with the new data sent by the current
        # provider. Update on some attributes is disabled by default, for
        # example username and id fields. It's also possible to disable update
        # on fields defined in SOCIAL_AUTH_PROTECTED_FIELDS.
        for name, value in details.items():
            if value and hasattr(user, name):
                # Check https://github.com/omab/python-social-auth/issues/671
                current_value = getattr(user, name, None)
                if not current_value or name not in protected:
                    changed |= current_value != value
                    setattr(user, name, value)
        send_mail('email/bienvenida.tpl', {'email': user.email,'username':user.username,'fullname':user.fullname}, DEFAULT_FROM_EMAIL, [user.email])
        if changed:
            strategy.storage.user.changed(user)

def save_profile_picture(backend, user, response, details, is_new=False, *args, **kwargs):

    if isinstance(backend, FacebookOAuth2):
        url = 'http://graph.facebook.com/{0}/picture?width=1000'.format(response['id'])
        user.photo = url
        user.save()

    if isinstance(backend, TwitterOAuth):
        if response.get('profile_image_url'):
            url = response.get('profile_image_url').replace('_normal','')
            user.photo = url
            user.save()

    if isinstance(backend, GoogleOAuth2):
        if response.get('image') and response['image'].get('url'):
            url = response['image'].get('url')
            u = urlparse(url)
            query = parse_qs(u.query)
            query.pop('sz', None)
            u = u._replace(query=urlencode(query, True))
            url = urlunparse(u)
            user.photo = url
            user.save()

    if isinstance(backend, LinkedinOAuth2):
        if response.get('pictureUrls') and response['pictureUrls'].get('values') and response['pictureUrls']['values'][0]:
            url = response['pictureUrls']['values'][0]
            user.photo = url
            user.save()