from website.content.retrieve import retrieveJson


def get_clubs_by_category():
    """
    Retrieves clubs by category json:
    [
        {
            "category": string,
            "clubs": [
                {
                    "imageName": string,
                    "heading": string,
                    "description": string[]
                }
            ]
        }
    ]
    """
    clubs_by_category = retrieveJson("studentlife/clubsandsocieties")
    return clubs_by_category


def get_facilities_by_area():
    """
    Retrieves facilities by area json:
    [
        {
            "area": string,
            "facilities": [
                {
                    "imageName": string,
                    "heading": string,
                    "description": string[]
                }
            ]
        }
    ]
    """
    facilities_by_area = retrieveJson("studentlife/facilities")
    return facilities_by_area
