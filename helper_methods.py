import os
import json

def check_file_exists(submission_path, file_name):
  path = os.path.join(submission_path, file_name)
  if not(os.path.exists(path)):
      return file_name + ", "
  else:
      return ""


def check_files_exist(submission_path, files_array):
    missing_files = ""
    for file in files_array:
        missing_files += check_file_exists(submission_path, file)

    # Update final output for missing files
    if len(missing_files) > 0:
      missing_files = missing_files[0:-2]  # remove trailing comma and whitespace
    else:
      missing_files = "All required files have been found."

    missing_files = [{
      'score': 0,
      'max': 0,
      'name': "Below is a list of any missing files in your submission. If any files are listed as missing that you believe you have uploaded please confirm you have uploaded the correct files/names, with the correct directory structure.",
      'output': missing_files
    }]

    return missing_files


def output_score(total_score):
    if(os.path.isdir("/autograder/results")):
    	resultsjson = open("/autograder/results/results.json","w")
    	resultsjson.write(json.dumps(total_score))
    	resultsjson.close()
    else:
    	print("local test: ", total_score)
