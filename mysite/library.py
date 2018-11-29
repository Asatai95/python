from django import *

from django.contrib.auth.forms import UserCreationForm
from config.settings import session

from mysite.models.user import *

def check_form(form):

    user = User(
         name=form.get('name'),
         email=form.get('email'),
         password=form.get('password'),
    )

    return user

def check_email(form):

    user_email_cheker = session.query(User).filter(
                            User.email == form.get('email'),
                        ).all()

    if user_email_cheker:
        return False
    else:
        return True

def users_create(form):

    user = User(
           name=form.get('name'),
           email=form.get('email'),
           password=form.get('password'),
    )

    session.add(user)
    session.commit()

    return user


def user_login(form):

    mail = session.query(User).filter(
                User.email == form.get('email')
           ).first()

    password = session.query(User).filter(
                  User.password == form.get('password')
               ).first()


    if mail == None or password == None:
        return False
    else:
        return True


def create_facebook_user(data):
    user = User(
             name = data['name']
            )
    session.add(user)
    session.commit()
    return user

def create_socials(user, data, provider):
    if provider == 'facebook':
        social = Social(
            user_id = user.id,
            provider = provider,
            provider_id = data['id'],
        )

    session.add(social)
    session.commit()

def check_socials(data, provider):
    if provider == 'facebook':
        social = session.query(Social).filter(
                        Social.provider == 'facebook',
                        Social.provider_id == data['id']
                    ).first()

    if social is None:
        return False
    else:
        # login_user(social.user_id)
        return True

def get_facebook_access_token(code):
    url = 'https://graph.facebook.com/v3.1/oauth/access_token'
    params = {
            'redirect_uri': config.setting.FACEBOOK_CALLBACK_URL,
            'client_id': config.setting.FACEBOOK_ID,
            'client_secret': config.setting.FACEBOOK_SECRET,
            'code': code,
    }
    r = requests.get(url, params=params)

    return r.json()['access_token']


def check_facebook_access_tokn(access_token):
    url = 'https://graph.facebook.com/debug_token'
    params = {
        'input_token': access_token,
        'access_token': '%s|%s' % (config.setting.FACEBOOK_ID, config.setting.FACEBOOK_SECRET)
    }
    r = requests.get(url, params=params)
    return r.json()['data']

def get_facebook_user_info(access_token, user_id):
    url = 'https://graph.facebook.com/%s' % (user_id)
    params = {
        'fields': 'name,email',
        'access_token': access_token,
    }
    return requests.get(url, params=params).json()


def get_socials_info(user):
    return session.query(Social).filter(Social.user_id == user.id)
