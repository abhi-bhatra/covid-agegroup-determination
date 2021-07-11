import urllib.request
import json
import os
import ssl

def allowSelfSignedHttps(allowed):
    # bypass the server certificate verification on client side
    if allowed and not os.environ.get('PYTHONHTTPSVERIFY', '') and getattr(ssl, '_create_unverified_context', None):
        ssl._create_default_https_context = ssl._create_unverified_context

allowSelfSignedHttps(True) # this line is needed if you use self-signed certificate in your scoring service.

print("=======Enter the Data==========")
sex = input("Enter the sex(Male/Female): ")
# "Regions supported: "
# "1. Vancouver Coastal\n2.Simcoe Muskoka\n3.Fraser\n4.\n5.New York\n6.Edmonton\n7.Hamilton\nand many more"
health_region = input("Enter the region you are from: ")
# Request data goes here
data = {
    "data":
    [
        {
            'sex': sex,
            'health_region': health_region,
        },
    ],
}

body = str.encode(json.dumps(data))

url = 'http://cec526e0-6f01-4cc4-9a56-94d38a6426b2.eastus.azurecontainer.io/score'
api_key = '' # Replace this with the API key for the web service
headers = {'Content-Type':'application/json', 'Authorization':('Bearer '+ api_key)}

req = urllib.request.Request(url, body, headers)

try:
    response = urllib.request.urlopen(req)

    result = response.read()
    result = result.decode('utf-8')
    print("Most affected age group, from the particular region is: ", result[17:22])
except urllib.error.HTTPError as error:
    print("The request failed with status code: " + str(error.code))

    # Print the headers - they include the requert ID and the timestamp, which are useful for debugging the failure
    print(error.info())
    print(json.loads(error.read().decode("utf8", 'ignore')))