from website.content.retrieve import retrieveJson


def get_clubs_by_category():
    clubs_by_category = retrieveJson("studentlife/clubsandsocieties")
    return clubs_by_category


def get_facilities_by_area():
    facilities_by_area = retrieveJson("studentlife/facilities")
    return facilities_by_area
