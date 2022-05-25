"""
Script used to generate a folder and README file for each project accepted
for BioHackathon Europe (https://biohackathon-europe.org/). The script will also
generate a YAML file of the projects.

INPUT: a CSV file from the event management software (EventBrite, EasyChair).
The CSV file will contain the projects submitted for the BioHackathon.
The expected fields in this file are: #, EventBrite, Authors, Title, Leads for Project,
Expected outcomes, Expected participants, Nominated participant,
Number of days for project, Topics, Time, Decision, Keywords, Abstract. These
fields seem to vary from year to year, so the script may need to be tweaked accordingly.

OUTPUT: (1) a folder for each project, containing a README file with a summary of
the project (e.g. https://github.com/elixir-europe/biohackathon-projects-2021);
(2) a YAML file containing the projects (e.g. https://github.com/elixir-europe/
biohackathon-europe-2021/blob/master/scripts/projects.yml). This is
used on the BioHackathon website to generate the Projects page (projects.html).

CONTACTS: webmaster@elixir-europe.org (for the script), jen.harrow@elixir-europe.org
(for the CSV file)

"""

# Make sure you have these Python modules installed.
import os
import csv
import yaml

# Adjust PROJECTS_FILE and PROJECTS_REPOSITORY for the current year.
PROJECTS_FILE = "biohackathon-2022-projects.csv"
PROJECTS_FOLDER = "projects"
PROJECT_YAML = "projects.yml"
PROJECTS_REPOSITORY = "https://github.com/elixir-europe/bioHackathon-projects-2022/tree/master/projects/{number}"

# Accepted projects column names
# (In 2021 these columns did not appear in the CSV file.)
ACPT_PROJECT_NUMBER = "number"
ACPT_PROJECT_MERGED = "merged_from"
ACPT_PROJECT_TITLE = "title"
ACPT_PROJECT_SUBMITTER = "submitter"

# Column names in the EasyChair CSV dump file.
# In 2021 the '#' column was the same as the PROJECT_EVENBRITE column.
# This is wrong. It should be a sequence of numbers 1-[Projects total].
PROJECT_NUMBER = "#"
#PROJECT_EVENBRITE = "EventBrite"
PROJECT_AUTHORS = "Authors"
PROJECT_TITLE = "Title"
PROJECT_ABSTRACT = "Abstract"
PROJECT_LEADS = "Main Lead for Project"
#PROJECT_NOMINATED_PARTICIPANT = "Nominated participant"
PROJECT_EXPECTED_OUTCOMES = "Expected outcomes"
PROJECT_EXPECTED_AUDIENCE = "Expected participants"
PROJECT_NUMBER_OF_EXPECTED_HACKING_DAYS = "Number of days for project"
PROJECT_HACKING_TOPIC = "Topics"
#PROJECT_DECISION = "Decision"
#PROJECT_PAPER = "paper"


# Create a list of dictionaries from the CSV file. Each dictionary represents a project.
#
# Input: CSV file
# Output: list of projects
#
# NOTE: each project has two numbers: an arbitrary, sequential 'project_number'
# and its number in EasyChair ('number' below).
# In 2021 the '#' field in the CSV was not a sequential list of numbers. It
# was a duplicate of the 'EventBrite'column. To get the sequential list needed
# the loop counter was used. This was possible because all the projects in the
# CSV were 'Accepted'.
def load_all_projects():
    # Initialise the projects list
    projects = []

    with open(PROJECTS_FILE) as pro_file:
        reader = csv.DictReader(pro_file, delimiter=',')
        line_count = 0
        accepted_count = 0
        # Loop through the CSV rows and create a dictionary for each project
        for index, row in enumerate(reader):
            if line_count == 0:
                print(f'Projects column names are {", ".join(row)}')

            
            accepted_count += 1
            project_link = PROJECTS_REPOSITORY.format(
                number=accepted_count)
            # Create a dictionary for the project. You may need to amend the key/value
            # assignments below to reflect what columns are in the CSV file. If you do,
            # don't forget to modify the to_file() function below to print out the fields
            # that actually exist in the dictionary.
            project = dict(
                number=row.get(PROJECT_NUMBER),
                authors=row.get(PROJECT_AUTHORS),
                title=row.get(PROJECT_TITLE),
                leads=row.get(PROJECT_LEADS),
                expected_outcomes=row.get(PROJECT_EXPECTED_OUTCOMES),
                expected_audience=row.get(PROJECT_EXPECTED_AUDIENCE),
                #nominated_participant=row.get(PROJECT_NOMINATED_PARTICIPANT),
                number_of_expected_hacking_days=row.get(
                    PROJECT_NUMBER_OF_EXPECTED_HACKING_DAYS),
                hacking_topic=row.get(PROJECT_HACKING_TOPIC),
                #decision=row.get(PROJECT_DECISION),
                abstract=row.get(PROJECT_ABSTRACT),
                link=project_link,
                project_number=accepted_count,
            )
            # Add the current project dictionary to the projects list
            projects.append(project)

            line_count += 1
    projects.sort(key = lambda project: int(project.get("project_number")))
    return projects

# Create the project directories and README files
# Input: dictionary for a project
# Output: project folder and README file
def to_file(project):

    path = "{}/{}".format(PROJECTS_FOLDER, project.get("project_number"))
    os.makedirs(path)

    file_name = "{}/{}/README.md".format(PROJECTS_FOLDER,
                                         project.get("project_number"))
    print("Creating file {}".format(file_name))

    with open(file_name, "w+") as output_file:
        output_file.write("# Project {}: {}\n\n".format(project.get("project_number"), project.get("title")))

        output_file.write("## Abstract\n\n")
        output_file.write(project.get("abstract"))

        output_file.write("\n\n## Topics\n\n")
        output_file.write(project.get("hacking_topic"))

        output_file.write(
            "\n\n**Project Number:** {}\n\n".format(project.get("project_number")))

        #output_file.write(
            #"\n\n**EasyChair Number:** {}\n\n".format(project.get("number")))

        #output_file.write("## Team\n\n")

        output_file.write("### Lead(s)\n\n")
        output_file.write(project.get("leads"))

        output_file.write("\n\n## Expected outcomes\n\n")
        output_file.write(project.get("expected_outcomes"))

        output_file.write("\n\n## Expected audience\n\n")
        output_file.write(project.get("expected_audience"))

        output_file.write(
            "\n\n**Number of expected hacking days**: {}\n\n".format(project.get("number_of_expected_hacking_days")))

# Main script to call load_all_projects() and to_file(), and so create folders and
# READMEs from the CSV file. It also creates the YAML file.
def main():
    projects = load_all_projects()

    projects_yaml = []

    for xls_project in projects:
        to_file(xls_project)

    yaml_projects = dict(
        project_list=projects
    )
    with open(PROJECTS_FILE) as pro_file, open(PROJECT_YAML, "w+") as yaml_output_file:
        yaml_output_file.write(
            yaml.dump(yaml_projects, default_flow_style=False))

    for xls_project in projects:
        print("* [Project {}](projects/{}) {}".format(xls_project.get("project_number"), xls_project.get("project_number"), xls_project.get("title")))

if __name__ == '__main__':
    main()
