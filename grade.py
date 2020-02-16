import os
import json
from subprocess import call, check_output
from helper_methods import check_files_exist, output_score

####################################################################################################
# GET CORRECT PATHS
####################################################################################################

# get correct path for student submission
if(os.path.isdir("/autograder/results")):
  STUDENT_PATH = "/autograder/submission/" # AUTOGRADER_SUBMISSION_PATH
else:
  STUDENT_PATH = "../../submission/" # LOCAL_SUBMISSION_PATH

####################################################################################################
# CHECK TO SEE IF ALL STUDENT FILES REQUIRED FOR PA3 EXIST
####################################################################################################
REQUIRED_HTML_FILES = ["index.html", "images.html", "form.html",
    "table_and_lists.html", "externals.html", "styles/main.css"]

# All paths in student submission to confirm all exist.
REQUIRED_FILES = ["README.md", "link.md"] + REQUIRED_HTML_FILES

missing_files = check_files_exist(STUDENT_PATH, REQUIRED_FILES)

####################################################################################################
# Check validation of html - MUST manually check url is legit
####################################################################################################
def read_file(path):
    f = open(path,"r"
    results_str = f.read()
    f.close()
    return results_str

def get_student_url():
    url = read_file(STUDENT_PATH + "link.md")
    url = url[:(url.find('.com') + 4)] # remove newline character
    return url

def validate_page(validation_url):
    call_output = open("output", "w")
    call_err = open("stderr", "w")

    exit_code = call(["curl", validation_url], stdout=call_output, stderr=call_err)

    call_output.close()
    call_err.close()


    if (exit_code == 0):
      return 1
    else:
      studentCompileError = read_file("stderr")
      print("Error occured while trying to validate the student's website")
      return -1 # for error occurred


    return exit_code

def validate_html_css_page(file_name, url):
    validator_html_url = "https://validator.w3.org/nu/?doc=https%3A%2F%2F" + url + "%2F" + file_name
    html_val_msg = validate_page(validator_html_url)

    html_validation_txt = read_file("output")
    count_html = html_validation_txt.count("class=\"error\"")

    validator_css_url = "https://jigsaw.w3.org/css-validator/validator?uri=https%3A%2F%2F" + url + "%2F" + file_name + "&profile=css3svg&usermedium=all&warning=1&vextwarning=&lang=en"
    css_val_msg = validate_page(validator_css_url)
    css_validation_txt = read_file("output")

    if (css_validation_txt.count("<h3>Sorry! We found the following errors (") > 0):
        start_idx = css_validation_txt.index("Sorry! We found the following errors (")
        end_idx = css_validation_txt.index(")</h3>")
        error_msg = css_validation_txt[start_idx:(end_idx)]
        print(error_msg)
        count_css = error_msg[38:]
        print(count_css)
    else:
        count_css = -1

    if (html_val_msg != -1 or css_val_msg != -1):
      print("\n\n============================")
      print("File Name: ", file_name)
      print("Student URL: ", url)
      print("HTML Validator URL: ", validator_html_url)
      print("CSS Validator URL: ", validator_css_url)
      print("============================")
      print("HTML # of Errors: ", count_html)
      print("CSS Errors: ", count_css) # TODO add # of errors???
    else:
      print("Error occured while trying to validate the student's website")


if (os.path.exists(STUDENT_PATH + "link.md")):

    files_unable_to_validate = []
    for file_name in REQUIRED_HTML_FILES:
        validate_html_css_page(file_name, get_student_url())

####################################################################################################
# Check for correct tags
####################################################################################################

REQUIRED_HTML_FILES_ATTRIBUTES_MAP = {
    # manually check font-family and font 6 sizes
    "index.html": ["html","head", "body","title", "meta","h1", "h2", "h3",
                   "section", "header", "footer", "main", "output", "p", "div", 
                   "address","em", "i", "code","pre","img","nav", "a", "link",
                   "details", "summary"],
    # manually check gradients (linear, radial), color 5 types
    "images.html": ["img", "picture", "gif", "jpg",
        "png", "webp", "svg"],
    # use of border-left, border-top, etc, positions, padding/margin
    "form.html": ["form", "label", "input", "button", "select", "datalist", "optgroup", "option",
                    "textarea", "output", "progress", "meter", "fieldset", "legend", 
                    "required","pattern","readonly","placeholder","title","disabled","for",
                    "value","tabindex","autofocus","autocomplete","min","max","checked","maxlength","multiple"],
    "table_and_lists.html": ["table", "thead", "tbody", "tfoot", "tr", "th", "td", "rowspan", "colspan", "colgroup", "col",  "caption"],
    "externals.html": ["iframe", "ol"],
}

# TODO: check for correct tag names in files
for file_name, required_html in REQUIRED_HTML_FILES_ATTRIBUTES_MAP.items():
    if (os.path.exists(STUDENT_PATH + file_name)):
        file_html = read_file(STUDENT_PATH + file_name)
        file_html = file_html.replace(" ", "") # remove spaces
        file_html = file_html.lower()

        missing_tags = []
        for tag in required_html:
            isFound = file_html.find(tag)
            if (isFound == -1):
                missing_tags += [tag]

        if (file_name == "form.html"):
            form_input_types = ["button", "checkbox", "color", "date", "datetime-local", "email",
                "file", "hidden", "image", "month", "number", "password", "radio", "range", "reset",
                "search", "submit", "tel", "text", "time", "url", "week"]

            for input_type in form_input_types:
                isFound = file_html.find("<inputtype=\""+input_type)
                if (isFound == -1):
                    missing_tags += ["input type: " + input_type]

        # if (file_name == "forms.html"):
        #     form_input_types = ["button", "checkbox", "color", "date", "datetime-local", "email",
        #         "file", "hidden", "image", "month", "number", "password", "radio", "range", "reset",
        #         "search", "submit", "tel", "text", "time", "url", "week"]
        #
        #     for input_type in form_input_types:
        #         isFound = file_html.find("<inputtype=\""+input_type)
        #         if (isFound == -1):
        #             missing_tags += ["input type: " + input_type]

        print("\n\n============================")
        print("File Name: ", file_name)
        print("============================")
        if (len(missing_tags) > 0):
            print("Missing Tags: ", missing_tags)
            print("# of Missing Tags: ", len(missing_tags))
        else:
            print("ALL TAGS FOUND")
    else:
        print(file_name, "DOES NOT EXIST")

################################################################################################
# Print results.json
################################################################################################
total_score = {
  'output': "The current output from the grader will ONLY tell you if your submission is missing any files and a message will appear if we are unable to run the validator on your code (NOT if it validates). Your score will show as a 0 until AFTER the deadline when your submission is graded. Please make sure the provided url for your website is correct.",
  'tests': missing_files
}
output_score(total_score)
