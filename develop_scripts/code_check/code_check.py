import os
import re
import sys

total = 0.0
count = 0

BASE_DIRECTORY = os.getcwd()
EXTENDED = ""
TYPE = "text"
excluded_directories = ["develop_scripts", "tests", "docs", "demo"]
excluded_files = ["__init__.py", "setup.py", "custom_assertions.py", "conftest.py"]

expected_html_tags = ["<table>", "<html>"]
expected_parsable_lines = ["<h2>Global evaluation</h2>"]


def parse_html(line):
    if "<html>" in line:
        return ""
    if "<table>" in line:
        return '<table class="table" style="width:auto;">'


def parse_line(line):
    if "Global evaluation" in line:
        return "<h2>File evaluation</h2>"


def check(module):
    global total, count, BASE_DIRECTORY

    if module[-3:] == ".py":

        pout = os.popen('pylint {} --output-format={}'.format(module, TYPE), 'r')
        module = module.replace("../", "")
        if TYPE == "html":
            print('<button data-toggle="collapse" data-target="#{1}" class="btn btn-default" style="width: 500px;">'
                  '{0}</button> <div id="{1}" class="collapse">'
                  .format(module, module.replace(".", "-").replace("\\", "-")))
        else:
            "Checking : {0}".format(module)
        for line in pout:
            if line.strip() in expected_html_tags:
                print(parse_html(line))
            elif EXTENDED == "f":
                print(line)
            elif EXTENDED == "e" and line[0:2] in ["C:", "W:", "E:"]:
                print(line)
            elif "Your code has been rated at" in line:
                print(line)

            if "Your code has been rated at" in line:
                score = re.findall("[-]?(\d+.\d+)", line)[0]
                total += float(score)
                count += 1
        print("-" * 50 + "\n")
        if TYPE == "html":
            print("</div></br>")


def print_header():
    print("<html><head>")
    print('<script src="http://code.jquery.com/jquery-latest.min.js" type="text/javascript"></script>'
          '<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css" '
          'integrity="sha384-BVYiiSIFeK1dGmJRAkycuHAHRg32OmUcww7on3RYdg4Va+PmSTsz/K68vbdEjh4u" '
          'crossorigin="anonymous">'
          '<script src="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/js/bootstrap.min.js"'
          ' integrity="sha384-Tc5IQib027qvyjSMfHjOMaLkfuWVxZxUPnCJA7l2mCWNIpG9mGCD8wGNIcPD7Txa" '
          'crossorigin="anonymous"></script>')
    print("</head>")


if __name__ == "__main__":

    BASE_DIRECTORY = sys.argv[1]
    EXTENDED = sys.argv[2]
    TYPE = sys.argv[3]
    if len(sys.argv) > 4:
        sys.stdout = open(sys.argv[4], 'w+')
    if TYPE == "html":
        print_header()
    for root, dirs, files in os.walk(BASE_DIRECTORY):
        for ignore in excluded_directories:
            if ignore in dirs:
                dirs.remove(ignore)
        for name in files:
            if name in excluded_files:
                continue
            check(os.path.join(root, name))

    brk = "</br>" if TYPE == "html" else "\n"
    print(brk + "%d modules found" % count)
    print(brk + "AVERAGE SCORE = %.02f" % (total / count))