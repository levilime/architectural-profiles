import json
from datetime import date
date = date.today().strftime("%d%m%Y")

SUBFIX = "F"
base = f"experimentresults/{date}{SUBFIX}/"


batch_list = [
    # 1story
    (["profiles/1story/flathousesdense.json"], f"{base}1storydense"),
    (["profiles/1story/flathouses.json"], f"{base}1story"),
    (["profiles/1story/flathousesnotdense.json"], f"{base}1storynotdense"),
    (["profiles/1story/stackedrooms.json","profiles/util/purposefulshapeconnectionstreet.json"], f"{base}1storystacked"),
    (["profiles/1story/restrictedstackedrooms.json", "profiles/util/purposefulshapeconnectionstreet.json"], f"{base}1storyrestrictedstacked"),
    (["profiles/1story/roomsformingbuildings.json"],f"{base}1storymultirooms"),
    (["profiles/1story/roomsformingbuildingsandstackedrooms.json", "profiles/util/purposefulshapeconnectionstreet.json"],f"{base}1storystackedmultirooms"),

    # 2 story
    (["profiles/2story/2storyhousesnotdense.json"], f"{base}2storyhousesnotdense"),
    (["profiles/2story/2storyhouses.json"], f"{base}2storyhousessmall"),
    (["profiles/2story/2storyupperentrancestreetroof.json", "profiles/util/purposefulshapeconnectionstreet.json", "profiles/util/stackedroomrule.json"], f"{base}2storyupperentrancestreetroof"),
    (["profiles/2story/2storyupperentrance.json", "profiles/util/purposefulshapeconnectionstreet.json","profiles/util/stackedroomrule.json"], f"{base}2storyupperentrance"),
    # (["profiles/2story/2storyhouses.json", "profiles/util/stackedroomrule.json","profiles/util/purposefulshapeconnectionstreet.json"],f"{base}2storystacked"),
    (["profiles/2story/2storyhousesstackedstreetathouses.json", "profiles/util/purposefulshapeconnectionstreet.json","profiles/util/stackedroomrule.json"], f"{base}2storyupperentrancestreettobuilding"),

    # 1 and 2 story combined
    (["profiles/1story2story/0story1story.json"], f"{base}0story1story"),
    (["profiles/1story2story/0story1storystacked.json", "profiles/util/purposefulshapeconnectionstreet.json", "profiles/util/stackedroomrule.json"], f"{base}0story1story"),

    # highrise
    (["profiles/highrise/highrise.json"], f"{base}highrise"),
    (["profiles/highrise/highrisemany.json"], f"{base}highrisemany"),

    # monolith
    (["profiles/monolith/monolith.json"], f"{base}monolith")
]

def check_batch():
    """
    check if all files exist in the batch
    :return: 
    """
    for p in batch_list:
        try:
            for file in p[0]:
                with open(file, 'r') as f:
                    json.load(f)
            print(f"FOUND {p[1]}")
        except:
            raise FileNotFoundError(f"generation for {p[1]} not found: {file}")

check_batch()
