from social_core.backends.facebook import FacebookOAuth2

class SettingsBackend(FacebookOAuth2):
    REDIRECT_STATE = False
    RESPONSE_TYPE = None
