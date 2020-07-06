"""
Intialize OpenID Connect Providers
"""

providers = {
    "level1": {

    },
    "level2": {
        "client_id": 'KvzOxYNYKdTQ18c0KMAV76PA',
        "client_secret": '3OezXqMrEWS0B9SUTtxAdvMK6rG0LXkwzhUPSyC4wHZdWnFE',
        "access_token_url": 'http://localhost:5002/auth/oidc_token',
        "access_token_params": None,
        "authorize_url": 'http://localhost:5002/auth/oidc_authorize',
        "authorize_params": None,
        "api_base_url": 'http://localhost:5002/api',
        "client_kwargs": {
            'scope': 'openid profile',
            'token_endpoint_auth_method': 'client_secret_basic'}
    },
    "level3": {},
    "level4a": {},
    "level4b": {},
    "level5a": {},
    "level5b": {},

}
