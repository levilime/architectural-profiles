import os
from bs4 import BeautifulSoup
import json

from solving.util import merge_dicts
from subprocess import call, check_output

import datetime

interactive_part = 'interactive.html'
definition_part = 'profile.json'

output_file = 'wow.html'

class InteractiveResult:

    def __init__(self, html, profile_json):
        self.html = html
        self.profile_json = profile_json

    def to_html(self):
        html = self.html
        soup = BeautifulSoup("<div></div>")
        tag = soup.new_tag('pre')
        tag.attrs = {"style": "height:400px;overflow: auto;width:50%;float:left;"}
        adjusted_profile_json = merge_dicts(self.profile_json, {})
        del adjusted_profile_json["tiles"]
        del adjusted_profile_json["adjacency"]
        del adjusted_profile_json["empty_tile"]
        tag.string = json.dumps(adjusted_profile_json, indent=4)
        soup.div.append(tag)
        soup.div.append(html)
        return soup.div

def export(results_folder):
    result_folders = [os.path.join(results_folder, x) for x in os.listdir(results_folder)]
    def create_interactive_result(folder):
        with open(os.path.join(folder, interactive_part)) as f:
            html = BeautifulSoup(f)
            soup = BeautifulSoup("<div></div>")
            original_tag = soup.div
            interactive_parts = [x for x in html.find('body').find_all() if 'type' in x.attrs]
            for i in interactive_parts:
                original_tag.append(i)
            interactive = original_tag
        with open(os.path.join(folder, definition_part), 'r') as f:
            definition = json.load(f)
        return InteractiveResult(interactive, definition)
    interactive_results = list(map(create_interactive_result, result_folders))
    soup = BeautifulSoup('<!DOCTYPE html><html lang="en"></html>')
    html = soup.html
    html.append(BeautifulSoup(
        '<script src="https://cdnjs.cloudflare.com/ajax/libs/require.js/2.3.4/require.min.js" integrity="sha256-Ae2Vz/4ePdIu6ZyI/5ZGsYnb+m0JlOmKPjt6XZ9JJkA=" crossorigin="anonymous"></script>'))
    html.append(BeautifulSoup('<script src="https://unpkg.com/@jupyter-widgets/html-manager@^0.14.0/dist/embed-amd.js" crossorigin="anonymous"></script>'))

    for interactive_result in interactive_results:
        html.append(interactive_result.to_html())
    f = open(output_file, "w+")
    f.write(soup.prettify())
    f.close()

