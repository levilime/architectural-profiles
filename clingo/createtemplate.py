import os

REPLACE_TOKEN_IN_CLINGO_TEMPLATE = "% INSERT TEXTURE CONSTRAINTS HERE"
CLINGO_FILE = os.path.join("clingo", "clingo.lp")


def create_clingo_file(constraints_for_clingo, template_folder):
    templates = os.listdir(template_folder)
    new_file = ""
    for template in templates:
        file = open(os.path.join(template_folder, template), "r")
        for line in file:
            if line.startswith(REPLACE_TOKEN_IN_CLINGO_TEMPLATE):
                new_file += "\n" + constraints_for_clingo
            else:
                new_file += line
        file.close()
    file = open(CLINGO_FILE, "w")
    file.write(new_file)
    file.close()
