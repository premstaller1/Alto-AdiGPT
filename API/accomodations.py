import requests
import json

# Base URL for the API
base_url = "https://tourism.opendatahub.com/v1/Accommodation"

# Parameters for the GET request
params = {
    "pagenumber": 1,            # Default page number
    #"pagesize": 10,             # Default page size
    "active": "true",           # Display all accommodations
    "language": "en",           # Language for the response
    "removenullvalues": "true"   # Include null values in the response
}

# Make the GET request
response = requests.get(base_url, params=params)

# Check if the request was successful
if response.status_code == 200:
    # Parse and print the JSON response
    data = response.json()
    print(data)
    # Extract the 'Items' section of the JSON response
    accommodations = data.get("Items", [])

    # Filter and structure the relevant fields
    filtered_accommodations = [
        {
            "Id": acc.get("Id"),
            "Shortname": acc.get("Shortname"),
            "Name": acc.get("AccoDetail", {}).get("en", {}).get("Name"),
            "City": acc.get("AccoDetail", {}).get("en", {}).get("City"),
            "Phone": acc.get("AccoDetail", {}).get("en", {}).get("Phone"),
            "Website": acc.get("AccoDetail", {}).get("en", {}).get("Website"),
            "Description": acc.get("AccoDetail", {}).get("en", {}).get("Shortdesc"),
            "Category": acc.get("AccoCategoryId"),
            "Altitude": acc.get("Altitude"),
            "Latitude": acc.get("Latitude"),
            "Longitude": acc.get("Longitude"),
        }
        for acc in accommodations
    ]

    # Pretty-print the filtered data
    print(json.dumps(filtered_accommodations, indent=2))
else:
    # Print an error message if the request failed
    print(f"Error: {response.status_code} - {response.text}")
