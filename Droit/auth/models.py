import enum
from flask_sqlalchemy import SQLAlchemy
from flask import current_app as app

from flask_login import UserMixin
from werkzeug.security import gen_salt
from authlib.oidc.core import UserInfo
from authlib.integrations.sqla_oauth2 import (
    OAuth2ClientMixin,
    OAuth2TokenMixin,
    OAuth2AuthorizationCodeMixin
)
from authlib.oidc.core.grants import (
    OpenIDCode as _OpenIDCode
)
from authlib.oauth2.rfc6749.grants import (
    AuthorizationCodeGrant as _AuthorizationCodeGrant,
)

auth_db = SQLAlchemy()

class UserAccountTypeEnum(enum.Enum):
    """
    Enumeration list about the user's register type
    """
    local = 0
    oidc = 1


class User(auth_db.Model, UserMixin):
    """
    User object, it can be register locally, or created by OpenID Connect
    """

    __tablename__ = 'user'

    id = auth_db.Column(auth_db.Integer, primary_key = True)
    username = auth_db.Column(auth_db.String(30), nullable = False)
    email = auth_db.Column(auth_db.String(35), unique = True, nullable = False)
    # if the user is loggedin using oidc, the password is random assigned
    password = auth_db.Column(auth_db.Text, nullable = False)  
    account_type = auth_db.Column(auth_db.Enum(UserAccountTypeEnum))
    provider_name = auth_db.Column(auth_db.String(80))

    def __str__(self):
        return f"Name: {self.username}, Email:{self.email}"

    def get_user_id(self):
        """
        Used by authlib
        """
        return self.id

    def get_id(self):
        """
        Return unicode user identifier, used by flask-login
        """
        return int_to_unicode(self.id)



# class OIDCProvider(auth_db.Model):
#     """
#     Representing a known OIDC Provider
#     """
#     __tablename__ = "oauth2_provider"

#     id = auth_db.Column(auth_db.Integer, primary_key = True)
#     name = auth_db.Column(auth_db.String(50), unique = True, nullable = False)
#     client_id = auth_db.Column(auth_db.String(200))
#     client_secret = auth_db.Column(auth_db.String(200))
#     access_token_url = auth_db.Column(auth_db.String(200))
#     authorize_url= auth_db.Column(auth_db.String(200))
#     # api_base_url='http://localhost:5000/api',
#     # access_token_params=None,
#     # authorize_params=None,
#     scope
#     client_id='T3GXMIk0hnYYAAWqlfWxW2sT',
#     client_secret='VtUZc0KxO4eNSOIqIhQXNBBwKykw57II9ERiQpcOjPombZiz',
#     access_token_url='http://localhost:5000/oauth/token',
#     access_token_params=None,
#     authorize_url='http://localhost:5000/oauth/authorize',
#     authorize_params=None,
#     api_base_url='http://localhost:5000/api',
#     client_kwargs={
#         'scope': 'openid profile',
#         'token_endpoint_auth_method': 'client_secret_basic'}


class OAuth2Client(auth_db.Model, OAuth2ClientMixin):
    """
    OAuth2/OpenID Connect client application class
    """

    __tablename__ = 'oauth2_client'

    id = auth_db.Column(auth_db.Integer, primary_key=True)
    # user_id = db.Column(
    #     db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'))
    # user = db.relationship('User')


class OAuth2AuthorizationCode(auth_db.Model, OAuth2AuthorizationCodeMixin):
    """
    Representation of OAuth2 Authorization Code Grant Type
    This is used to register at server end to support this code flow
    """
    __tablename__ = 'oauth2_code'

    id = auth_db.Column(auth_db.Integer, primary_key=True)
    user_id = auth_db.Column(
        auth_db.Integer, auth_db.ForeignKey('user.id', ondelete='CASCADE'))
    user = auth_db.relationship('User')



class OAuth2Token(auth_db.Model, OAuth2TokenMixin):
    """
    Representing the real token (Access Token, Refresh Token) in OAuth2 flow
    """
    __tablename__ = 'oauth2_token'

    id = auth_db.Column(auth_db.Integer, primary_key = True)
    name = auth_db.Column(auth_db.String(length=40))
    token_type = auth_db.Column(auth_db.String(length=40))
    access_token = auth_db.Column(auth_db.String(length=200))
    refresh_token = auth_db.Column(auth_db.String(length=200))
    id_token = auth_db.Column(auth_db.String(length=200))
    expires_at = auth_db.Column(auth_db.Integer)
    expires_in = auth_db.Column(auth_db.Integer)
    scope = auth_db.Column(auth_db.String(length=40))
    user_id = auth_db.Column(
        auth_db.Integer, auth_db.ForeignKey('user.id', ondelete='CASCADE'))
    user = auth_db.relationship('User')

    def to_token(self):
        return dict(
            access_token=self.access_token,
            token_type=self.token_type,
            refresh_token=self.refresh_token,
            id_token=self.id_token,
            expires_at=self.expires_at,
            expires_in=self.expires_in,
            scope = self.scope,
            name = self.name
        )

class AuthorizationCodeGrant(_AuthorizationCodeGrant):
    """
    Auth Code Grant
    """
    def create_authorization_code(self, client, grant_user, request):
        code = gen_salt(48)
        # nonce = request.data.get('nonce')
        item = OAuth2AuthorizationCode(
            code=code,
            client_id=client.client_id,
            redirect_uri=request.redirect_uri,
            scope=request.scope,
            user_id=grant_user.id,
            # nonce=nonce,
        )
        auth_db.session.add(item)
        auth_db.session.commit()
        return code

    def parse_authorization_code(self, code, client):
        item = OAuth2AuthorizationCode.query.filter_by(
            code=code, client_id=client.client_id).first()
        if item and not item.is_expired():
            return item

    def delete_authorization_code(self, authorization_code):
        auth_db.session.delete(authorization_code)
        auth_db.session.commit()

    def authenticate_user(self, authorization_code):
        return User.query.get(authorization_code.user_id)


class OpenIDCode(_OpenIDCode):
    """
    Representing the OpenID Token
    """

    def exists_nonce(self, nonce, request):
        """
        For this implementation, we will not determine whether the nonce is already seen
        so simply return False
        """
        return False
        # exists = OAuth2AuthorizationCode.query.filter_by(
        #     client_id=request.client_id, nonce=nonce
        # ).first()
        # return bool(exists)

    def get_jwt_config(self, grant):
        app_jwt_config = {
            'key': app.config["OAUTH2_JWT_KEY"],
            'alg': app.config["OAUTH2_JWT_ALG"],
            'iss': app.config["OAUTH2_JWT_ISS"],
            'exp': app.config["OAUTH2_JWT_EXP"],
        }
        return app_jwt_config

    def generate_user_info(self, user, scope):
        """
        Generate the user information that will be used to encode the ID token
        The allowed properties are:
        [
             'sub', 'name', 'given_name', 'family_name', 'middle_name', 'nickname',
             'preferred_username', 'profile', 'picture', 'website', 'email',
             'email_verified', 'gender', 'birthdate', 'zoneinfo', 'locale',
             'phone_number', 'phone_number_verified', 'address', 'updated_at',
        ]
        """
        return UserInfo(sub=str(user.id), username=user.username, email = user.email)



def int_to_unicode(number):
    """
    Convert the integer 'number' to 'unicode' str
    """
    return chr(number)


def unicode_to_int(unicode_str):
    """
    Convert the unicode 'unicode_str' to corresponding integer
    """
    return ord(unicode_str)