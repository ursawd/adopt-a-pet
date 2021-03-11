# Helpers library
###########################################################################
# def get_token():
# Gets access token from API
# def get_API_response(URL, params=None):
# Retrieve all data from API for pets
# def get_random_pet():
# Retrieves a single random animal
# def fix_web_desc(petOfDay):
# Check websites and descriptions of an animal
# def get_org(resp):
# Retrieves info about an organization from the API
###########################################################################
#
import requests, json, html
from random import randint
from flask import flash, redirect

# ###########################################################################
#
def get_token():
    """Get security token.
    ARGUMENTS:
        NONE:
    RETURNS: 3 part security token in json format

        from the API docs: curl -d "grant_type=client_credentials&client_id={CLIENT-ID}&
        client_secret={CLIENT-SECRET}" https://api.petfinder.com/v2/oauth2/token
    """
    payload = {
        "grant_type": "client_credentials",
        # API Key
        "client_id": "MGvOT3PCnsjcivWjftGpVKOreC8gFlgKcOB6IS8WkMj2Ol4Jbh",
        # API Secret
        "client_secret": "vFCY83ALuMNGfxDZnPTTrD0T3bEZLOlQd1zSnIBx",
    }

    # Note request for token is a POST request. API docs not clear.
    r = requests.post("https://api.petfinder.com/v2/oauth2/token", data=payload)

    if r.status_code != 200:
        return None
    else:
        return r.json()  # returns 3 part authorization token


# ###########################################################################
#
def get_API_response(URL, params=None):
    """Get API info.
    ARGUMENTS:
        PARAMS:
            Argument params needs this structure:
            params = (
            ("type", "dog"),
            ("page", "2"),
            )
        URL:
            Appropiate URL to query API
    RETURNS: API response in json format or None if error
    """
    # Get valid access token
    token = get_token()  # get_token defined in this file

    # Create header to enable API access authorization
    # access_token key contains required access token for every API request
    headers = {
        "Authorization": f"Bearer {token['access_token']}",
    }
    # Request info from API
    if params == None:
        req = requests.get(URL, headers=headers)
    else:
        req = requests.get(URL, headers=headers, params=params)

    # check response for errors
    if req.status_code != 200:
        print(">>>>>>>>>>", req, req.status_code, flush=True)
        return None
    else:
        return req.json()


# -----------------------------------------------------------
# ? USAGE:
#     # parameters for this request
# params = (
#     ("type", "dog"),
#     ("page", "2"),
# )

# # URL for this request
# URL = "https://api.petfinder.com/v2/animals"

# # response will contain API repsonse for supplied params and URL
# response = get_API_response(URL, params)
# ###########################################################################
#
def get_random_pet():
    """Return response object of one random pet from API"""

    # get 'page' (100) of all pets -or- less if fewer records match
    params = (("limit", "100"), ("location", "42086"), ("distance", "500"))
    URL = "https://api.petfinder.com/v2/animals/"
    response = get_API_response(URL, params)

    # Select one random record for Pet Of The Day
    rndNum = randint(10, 99)
    try:
        petOfDay = response["animals"][rndNum]
    except:
        flash("Random pet error: API Error. Contact Support / Try again later")
        return redirect("/")

    # Insert Photo Not Found picture if none supplied by API
    if len(petOfDay["photos"]) == 0:
        petOfDay["photos"] = [{"large": "/static/imgs/avatar.jpg"}]

    # Get organizations website and remove html characters
    fix_web_desc(petOfDay)

    return petOfDay


# ###########################################################################
#
def fix_web_desc(petOfDay):
    """Return organizations website if they have one other wise pet finders
    entry and remove html entities and characters from description."""

    petOfDay["website"] = get_org(petOfDay)

    # 'description often contains html characters like:
    #       If you&amp;#39;ve been looking for Petey from...
    # The first pass through unescape converts &amp; to & which
    # is used in &#39; (an '). The 2nd pass through unescape converts
    # the &#39; to the '.
    if petOfDay["description"] is not None:
        petOfDay["description"] = html.unescape(petOfDay["description"])
        petOfDay["description"] = html.unescape(petOfDay["description"])

    return petOfDay


# ###########################################################################
#
def get_org(resp):
    """Gets info about organization holding animal"""

    org_string = resp["_links"]["organization"]["href"]
    URL = f"https://api.petfinder.com{org_string}"

    # get specific organization info
    response = get_API_response(URL)
    # check if organization has own website, if not use petfinder website info
    if response["organization"]["website"] is None:
        return response["organization"]["url"]
    else:
        return response["organization"]["website"]