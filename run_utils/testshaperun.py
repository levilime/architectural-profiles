import json
from shaperun import merge_profile, get_shapes_of_profile, solve
from datetime import date

date = date.today().strftime("%d%m%Y")

with open("../profiles/base/shapebasestairs.json", 'r') as f:
    profile_json = json.load(f)

profile = merge_profile(profile_json, ["profiles/1story/flathousesdense.json"])
shapes = get_shapes_of_profile(profile, True, False)
solve(f"experimentresults/{date}/flathousesdense", profile, shapes, 1, restart_on_models=True,
      block_mode={"x":4, "y":4, "z":4})