from authlib.integrations.flask_client import OAuth
from authlib.integrations.flask_oauth2 import (
    AuthorizationServer, ResourceProtector)
from authlib.integrations.sqla_oauth2 import (
    create_query_client_func,
    create_save_token_func,
    create_bearer_token_validator,
)

from .models import OAuth2Token, OAuth2Client, AuthorizationCodeGrant, OpenIDCode
from .models import auth_db
from .providers_config import providers

# def fetch_token(name):
#     """
#     Authlib library helper function, used to retrieve access token relating to current user, issued by 'name'
#     """
#     token = OAuth2Token.query.filter_by(
#         name = name,
#         # current_user is the proxy variable to access logged in user
#         user_id = current_user.get_user_id()
#     ).first()
#     return token.to_token()


# oauth = OAuth(fetch_token = fetch_token)
oauth = OAuth()
authorization = AuthorizationServer()
require_oauth = ResourceProtector()

def initiate_providers(self_name):
    """
    Register pre-configuered OpenID Connect Providers
    """
    
    for provider_name in providers:
        if provider_name == self_name:
            continue
        oauth.register(name = provider_name, **providers[provider_name])

def config_oauth(app):
    """
    Initialize authorization server, and register suportted authorization grant types
    """

    query_client = create_query_client_func(auth_db.session, OAuth2Client)
    save_token = save_token = create_save_token_func(auth_db.session, OAuth2Token)
    authorization.init_app(
        app,
        query_client=query_client,
        save_token=save_token
    )

    # Register Authorization code grant types
    authorization.register_grant(AuthorizationCodeGrant, [
        OpenIDCode(require_nonce=False),
    ])

    # protect resource
    bearer_cls = create_bearer_token_validator(auth_db.session, OAuth2Token)
    require_oauth.register_token_validator(bearer_cls())
