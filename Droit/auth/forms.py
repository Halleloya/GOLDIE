from random import choices
from wtforms import Form, BooleanField, StringField, validators, SelectField

class OAuthClientRegisterForm(Form):
    """
    Basic form class (abstract)
    """
    client_name = StringField('Client Name', [validators.InputRequired('Please enter a Client Name'), 
                    validators.Length(min=4, max=35)])
    client_uri = StringField('Client URI', [validators.URL(require_tld = False, message = "Please enter a valid URI"),
                    validators.Length(min=6,max=200)])
    redirect_uri =  StringField("Redirect URI", [validators.URL(require_tld = False, message = "Please enter a valid URI"),
                    validators.Length(min=6,max=200)])
    scope = SelectField("Allowed Scopes", choices = [('openid profile', 'openid profile')])
    grant_type = SelectField("Allowed Grant Types", choices = [('authorization_code', 'authorization_code')])
    response_type = SelectField("Allowed Response Types", choices = [('code', 'code')])
    token_endpoint_auth_method = SelectField("Token Endpoint Auth Method", choices = [('client_secret_basic','client_secret_basic'), ('none', 'none')])
