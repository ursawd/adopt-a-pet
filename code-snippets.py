from libs.petlib import get_API_response

# parameters for this request
params = (
    ("type", "dog"),
    ("page", "2"),
    ("limit", "2"),
)

# URL for this request
URL = "https://api.petfinder.com/v2/animals"

# response will contain API response (json) for supplied params and URL
response = get_API_response(URL, params)
print(">>>>>>>>>>", response, flush=True)
