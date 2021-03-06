import requests, json, html
from random import randint

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
    while True:
        id = randint(50000000, 51000000)  # estimated range for pet id's
        # URL = f"https://api.petfinder.com/v2/animals/50703302"
        URL = f"https://api.petfinder.com/v2/animals/{id}"
        response = get_API_response(URL)

        if response != None:
            # "description" contains html entities such as &amp#39; (')
            # this changes them to display proper character
            if response["animal"]["description"] is not None:
                response["animal"]["description"] = html.unescape(response["animal"]["description"])
                org_web_site = get_org(response)
                response["animal"]["website"] = org_web_site
            break
    return response


# ###########################################################################
#
def get_org(resp):
    org_string = resp["animal"]["_links"]["organization"]["href"]
    URL = f"https://api.petfinder.com{org_string}"

    # get specific organization info
    response = get_API_response(URL)
    # check if organization has own website, if not use petfinder website info
    if response["organization"]["website"] is None:
        return response["organization"]["url"]
    else:
        return response["organization"]["website"]


# ###########################################################################
#
# def get_random_pet():
#     """Return response object of one random pet from API"""
#     while True:
#         id = randint(50000000, 51000000)  # estimated range for pet id's
#         # URL = f"https://api.petfinder.com/v2/animals/50703302"
#         URL = f"https://api.petfinder.com/v2/animals/{id}"
#         response = get_API_response(URL)

#         if response != None:
#             # "description" contains html entities such as &amp#39; (')
#             # this changes them to display proper character
#             if response["animal"]["description"] is not None:
#                 response["animal"]["description"] = html.unescape(response["animal"]["description"])
#                 org_web_site = get_org(response)
#                 response["animal"]["website"] = org_web_site
#             break
#     return response
