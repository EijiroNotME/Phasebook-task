from flask import Blueprint, request
from .data.search_data import USERS

bp = Blueprint("search", __name__, url_prefix="/search")

@bp.route("")
def search():
    return search_users(request.args.to_dict()), 200

def search_users(args):
    search_id = args.get("id")
    search_name = args.get("name", "").lower()
    search_age = args.get("age")
    search_occupation = args.get("occupation", "").lower()

    results = []
    matched_ids = set()


    def matches_partial(value, search):
        return search in value.lower()

    def matches_age(user_age, search_age):
        return abs(int(user_age) - int(search_age)) <= 1


    if search_id:
        for user in USERS:
            if user["id"] == search_id:
                user["match_priority"] = 1
                results.append(user)
                matched_ids.add(user["id"])


    for user in USERS:
        if user["id"] in matched_ids:
            continue

        match = False
        priority = 5  

        if search_name and matches_partial(user["name"], search_name):
            match = True
            priority = min(priority, 2)  # Name has priority 2
        if search_age and matches_age(user["age"], search_age):
            match = True
            priority = min(priority, 3)  # Age has priority 3
        if search_occupation and matches_partial(user["occupation"], search_occupation):
            match = True
            priority = min(priority, 4)  # Occupation has priority 4

        if match:
            user["match_priority"] = priority
            results.append(user)
            matched_ids.add(user["id"])


    results.sort(key=lambda x: x["match_priority"])


    for user in results:
        del user["match_priority"]

    return results
