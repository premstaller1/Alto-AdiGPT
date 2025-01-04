import requests
import json

# Base URL for the API
base_url = "https://tourism.opendatahub.com/v1/ODHActivityPoi"

# Parameters for the GET request
params = {
    "pagenumber": 1,            # Page number
    "pagesize": 1,             # Number of results per page
    "active": "true",           # Only active activities
    "language": "en",           # Language for the response
    "removenullvalues": "true"  # Exclude null values from the response
}

# Make the GET request
response = requests.get(base_url, params=params)

# Check if the request was successful
if response.status_code == 200:
    # Parse the JSON response
    data = response.json()

    # Extract the 'Items' section of the JSON response
    activities = data.get("Items", [])

    # Filter and structure the relevant fields
    formatted_activities = [
        {
            "Id": activity.get("Id"),
            "Name": activity.get("Detail", {}).get("en", {}).get("Title"),
            "Description": activity.get("Detail", {}).get("en", {}).get("BaseText"),
            "Category": activity.get("AdditionalPoiInfos", {}).get("en", {}).get("MainType"),
            "Attraction Type": activity.get("AdditionalPoiInfos", {}).get("en", {}).get("PoiType"),
            "Tags": [tag.get("TagName", {}).get("en") for tag in activity.get("LTSTags", []) if tag.get("TagName")],
            "Latitude": activity.get("GpsPoints", {}).get("position", {}).get("Latitude"),
            "Longitude": activity.get("GpsPoints", {}).get("position", {}).get("Longitude"),
            "Altitude": activity.get("GpsPoints", {}).get("position", {}).get("Altitude"),
            "Region": activity.get("LocationInfo", {}).get("RegionInfo", {}).get("Name", {}).get("en"),
            "Municipality": activity.get("LocationInfo", {}).get("MunicipalityInfo", {}).get("Name", {}).get("en"),
            "Contact": {
                "City": activity.get("ContactInfos", {}).get("en", {}).get("City"),
                "Email": activity.get("ContactInfos", {}).get("en", {}).get("Email"),
                "Address": activity.get("ContactInfos", {}).get("en", {}).get("Address"),
                "Phonenumber": activity.get("ContactInfos", {}).get("en", {}).get("Phonenumber"),
                "Website": activity.get("ContactInfos", {}).get("en", {}).get("Url"),   
            },
            "Images": [
                {
                    "ImageUrl": image.get("ImageUrl"),
                    "Title": image.get("ImageTitle", {}).get("en"),
                    "Description": image.get("ImageDesc", {}).get("en"),
                    "Width": image.get("Width"),
                    "Height": image.get("Height")
                }
                for image in activity.get("ImageGallery", [])
            ],
        }
        for activity in activities
    ]

    # Pretty-print the formatted data
    print(json.dumps(formatted_activities, indent=2))
else:
    # Print an error message if the request failed
    print(f"Error: {response.status_code} - {response.text}")
