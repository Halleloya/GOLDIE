"""
Functions declared in this file are helper functions that can be shared by all other modules
"""
import flask
from urllib.parse import urljoin
from .models import DirectoryNameToURL, TargetToChildName

def is_json_request(request: flask.Request, properties: list = []) -> bool:
    """Check whether the request's body could be parsed to JSON format, and all necessary properties specified by `properties` are in the JSON object

    Args:
        request (flask.Request): the flask request object wrapping the real HTTP request data
        properties (list[str]): list of property names to check. By default its an empty list

    Returns:
        boolean: whether the request is a JSON-content request and contains all the properties
    """
    try:
        body = request.get_json()
    except TypeError:
        return False
    if body is None:
        return False
    for prop in properties:
        if prop not in body:
            return False
    return True


def clean_thing_description(thing_description: dict) -> dict:
    """Change the property name "@type" to "thing_type" and "id" to "thing_id" in the thing_description

    Args:
        thing_description (dict): dict representing a thing description

    Returns:
        dict: the same dict with "@type" and "id" keys are mapped to "thing_type" and "thing_id"
    """
    if "@type" in thing_description:
        thing_description["thing_type"] = thing_description.pop("@type")
    if "id" in thing_description:
        thing_description["thing_id"] = thing_description.pop("id")
    return thing_description


def get_target_url(location: str, api: str = "") -> str:
    """Check the next possible location to request in order to get the 'location' directory

    It will check database if the 'location' is an adjacent directory to the current one.
    If it is, then return the concatenated URI using this adjacent directory's URI.

    Then it will check whether this 'location' is one of descendants directories.
    If it is, then return.

    Finally if current directory is not master, then it will return the URI using master directory's location

    Args:
        location (str): the target location to be searched
        api(str): url path after the host name, such as /register, /search. It is highly encouraged to form this parameter using 'url_for'

    Returns:
        str: if the location is possible, return the concatenated URI along with the 'api', otherwise return None

    """
    target_url = None
    # 1. check whether the location is known to current directory (parent or direct children)
    known_directory = DirectoryNameToURL.objects(
        directory_name=location).first()
    if known_directory is not None:
        target_url = urljoin(known_directory.url, api)

    # 2. check if the location is its descendants
    elif TargetToChildName.objects(target_name=location).first() is not None:
        descendant_directory = TargetToChildName.objects(
            target_name=location).first()
        target_url = urljoin(DirectoryNameToURL.objects(
            directory_name=descendant_directory.child_name).first().url, api)

    # 3. if current is not master directory, return the url of master directory
    elif DirectoryNameToURL.objects(relationship="parent").first() is not None:
        master_url = DirectoryNameToURL.objects(
            directory_name="master").first().url
        target_url = urljoin(master_url, api)

    return target_url
