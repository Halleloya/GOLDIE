"""
This file defines all the API endpoints used for the user authentication. It contains three
different and related modules:
1. Local user management: using flask-login library to login、register、logout user
2. OpenID Connect client: render the OIDC login option page and redirect the user
    to the corresponding provider's login page.
    After the OIDC is finished, an API endpoint is used to deal with the redirection
    and retrieve the user's identification using authorization token in the
    redirection URL's query parameter.

3. OpenID Connect server: contains the following APIs for OpenID Connect providers
    1. register a new client.
    2. Ask for user's consent after logged in via OpenID Connect and issue auth code
        after the consent.
    3. Issue an access token and optionally a refresh token

"""
import hashlib
import uuid
import time
import jwt
from jwt.exceptions import InvalidAudienceError
from flask import request, jsonify, abort
from flask import Blueprint, render_template, request, make_response, redirect, url_for
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import gen_salt
from authlib.oauth2 import OAuth2Error

from ..forms import UserRegisterForm, UserLoginForm
from ..auth import login_manager
from .models import auth_db, User, UserAccountTypeEnum, OAuth2Client
from .oauth2 import oauth, authorization
from .forms import OAuthClientRegisterForm

auth = Blueprint('auth', __name__)

# Flask-login library used this variable to determine the login page
# when an anonymous user is trying to access a page without authentication
login_manager.login_view = "auth.login"

"""
Note: 
`current_user` variable is a proxy for flask_login to get access to current session's user.
By default, when a user is not actually logged in, current_user is set to an AnonymousUserMixin object. 
It has the following properties and methods:
* is_active and is_authenticated are False
* is_anonymous is True
* get_id() returns None
"""


@auth.route('/oauth_list', methods=['GET'])
def oauth_list():
    """List all providers(stored in the OAuth class in the memory) and all registered clients(from database)

    """
    # as a client, getting all known providers' names
    oauth_providers = [provider for provider in oauth._clients.values() if provider.client_id is not None]
    # as a provider, getting all registered clients
    oauth_clients = OAuth2Client.query.all()
    return render_template("/auth/oauth_list.html", oauth_providers=oauth_providers, oauth_clients=oauth_clients)


"""
OIDC Provider API endpoints
"""


@auth.route('/oidc_create_client', methods=('GET', 'POST'))
def oidc_create_client():
    """Endpoint for processing OpenID Connect client

    When the api is accessed using GET HTTP method, a form is returned to ask for
    client's registration information.

    When the api is accessed using POST HTTP method, the client's information is
    gathered and a corresponding 'client' entry is registered in the provider's
    database
    """
    oauth_client_form = OAuthClientRegisterForm(request.form)

    def split_by_crlf(s):
        """
        Helper function to splitlives for the input
        """
        return [v for v in s.splitlines() if v]

    if request.method == 'POST' and oauth_client_form.validate():
        client_id = gen_salt(24)
        client = OAuth2Client(client_id=client_id)  # optionally bind a user with the client
        client.client_id_issued_at = int(time.time())
        if oauth_client_form.token_endpoint_auth_method.data == 'none':
            client.client_secret = ''
        else:
            client.client_secret = gen_salt(48)

        client_metadata = {
            "client_name": oauth_client_form.client_name.data,
            "client_uri": oauth_client_form.client_uri.data,
            "grant_types": split_by_crlf(oauth_client_form.grant_type.data),
            "redirect_uris": split_by_crlf(oauth_client_form.redirect_uri.data),
            "response_types": split_by_crlf(oauth_client_form.response_type.data),
            "scope": oauth_client_form.scope.data,
            "token_endpoint_auth_method": oauth_client_form.token_endpoint_auth_method.data
        }
        client.set_client_metadata(client_metadata)

        auth_db.session.add(client)
        auth_db.session.commit()
        return redirect(url_for('auth.oauth_list'))

    return render_template('/auth/oidc_create_client.html', form=oauth_client_form)


@auth.route('/oidc_authorize', methods=['GET', 'POST'])
def oidc_consent_authorize():
    """Ask for login user's consent to provide the request scope to the replying party

    """
    # user is not authenticated, redirect to login page
    if request.method == 'GET':
        # 1. if user is not logged in, redirect to log in user
        if current_user.is_anonymous:
            redirect_response = redirect(url_for('auth.login', oauth_authorization=True, **request.args))
            return redirect_response
        # 2. check whether the client info is valid
        try:
            grant = authorization.validate_consent_request(end_user=current_user)
        except OAuth2Error as error:
            return jsonify(dict(error.get_body()))
        # 3. ask for authorizization
        return render_template("auth/oidc_authorize.html", grant=grant)

    elif request.method == 'POST':
        # Check user's response and respond to the replying party accordingly
        if 'confirm' in request.form:
            grant_user = current_user
        else:
            grant_user = None
        return authorization.create_authorization_response(grant_user=grant_user)


@auth.route('oidc_token', methods=['POST'])
def oidc_issue_token():
    """OpenID Connect token endpoint. Issues access token and ID token when receiving
    a request that contains an authorization code.

    """
    return authorization.create_token_response()


"""
OIDC Client routes
"""


@auth.route('/oidc_login', methods=['GET'])
@auth.route('/oidc_login/<provider_name>', methods=['GET'])
def oidc_login(provider_name=None):
    """Return a list of OPID providers to login

    If a specific option is requested, redirect the page to the provider's auth page
    """
    if not provider_name:
        providers = [provider.name for provider in oauth._clients.values() if provider.client_id is not None]
        return render_template("/auth/oidc_login.html", providers=providers)
    else:
        # Redirect to the authorization page of the provider
        provider = oauth.create_client(provider_name)
        return provider.authorize_redirect()


@auth.route('/oidc_auth_code/<provider_name>', methods=['GET'])
def oidc_auth_code_process(provider_name):
    """This is the redirection URL when current client is registered and used to
    process OIDC user login.

    When a OIDC user is logged in succesfully, a redirection is happened and
    the user's authorization code is contained in the URL's query parameter.
    After receiving the redirection request, this method retrieve the authorization
    code and use it to retrieve access token and id token.
    When the id token is retrieved, the user infomration will be further processed
    to change the session's authentication status.
    """

    # get token using the authorization_code in the query string
    if "code" not in request.args:
        abort(401, description=request.args['error'])

    provider = oauth.create_client(provider_name)
    token = provider.authorize_access_token()
    # get user profile using access token
    id_token = token['id_token']
    try:
        user_info = jwt.decode(id_token, f'{provider_name}-secret', audience=oauth._clients[provider_name].client_id)
    except InvalidAudienceError as e:
        print(e)
        abort(401)

    # if the user email is the same, we treat them as the same user
    user = User.query.filter_by(email=user_info['email']).first()
    # get user from database or create a new one
    if not user:
        user = User(username=user_info['username'],
                    email=user_info['email'],
                    password=gen_salt(30),
                    account_type=UserAccountTypeEnum.oidc,
                    provider_name=provider_name)
        auth_db.session.add(user)
        auth_db.session.commit()

    # login this user using flask-login
    login_user(user)
    return redirect(url_for('home.index'))


"""
Local authentication flows
"""


@auth.route('/login', methods=['GET', 'POST'])
def login():
    """Render login pages and also handle local user's login request

    """
    user_form = UserLoginForm(request.form)
    if request.method == 'POST' and user_form.validate():
        user = User.query.filter_by(email=user_form.email.data).first()
        if user and verify_password(user.password, user_form.password.data):
            # login success, record it using flask-login
            login_user(user, remember=user_form.remember_me)
            # check whether it's from authorize page. If so, redirect back, with same request parameters
            if "oauth_authorization" in request.args:
                return redirect(url_for('auth.oidc_consent_authorize', **request.args))
            else:
                # local login, redirect to home page
                return redirect(url_for('home.index'))
        else:
            user_form.password.errors.append("email/password incorrect")
            return render_template('auth/login.html', form=user_form)
    return render_template('auth/login.html', form=user_form)


@auth.route('/register', methods=['GET', 'POST'])
def register():
    """Render local user register page and handle user registration

    """
    user_form = UserRegisterForm(request.form)
    # Get request, no such user's email or password not match, return to 'register' page
    if request.method == 'POST' and user_form.validate():
        # check the user from database, then compare the password
        user = User.query.filter_by(email=user_form.email.data).first()
        if not user:
            new_user = User(username=user_form.username.data,
                            email=user_form.email.data,
                            password=get_hashed_password(user_form.password.data),
                            account_type=UserAccountTypeEnum.local)  # local user register
            auth_db.session.add(new_user)
            auth_db.session.commit()
            # login success, record it using flask-login
            login_user(new_user)

            return redirect(url_for('home.index'))
        else:
            # User already exist, return to the register page and show the error
            user_form.email.errors.append("User email already exist")

    return render_template('auth/register.html', form=user_form)


@auth.route('/logout')
@login_required
def logout():
    """Logout user in the current session

    """
    logout_user()
    return redirect(url_for('home.index'))


def get_hashed_password(raw_password, salt=None):
    """Hash the raw password and return

    This method is usually used to hash user's plain password and store the hashed
    string into the database
    """
    # salt's length is 32
    if not salt:
        salt = uuid.uuid4().hex
    hashed_password = hashlib.sha512((raw_password + salt).encode('utf-8')).hexdigest()

    return hashed_password + salt


def verify_password(saved_hashed_password, input_raw_password):
    """Check if the stored hashed password is generated by the input_raw_password

    The user's input raw password is hashed first and then compared with the
    'saved_hashed_password'. Return a boolean value to indicate the comparison result.

    """
    pwd_salt = saved_hashed_password[-32:]

    return saved_hashed_password == get_hashed_password(input_raw_password, pwd_salt)
