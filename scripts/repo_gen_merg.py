import os
import csv
import yaml

PROJECTS_FILE = "projects.csv"
PROJECTS_FOLDER = "projects"
PROJECT_YAML = "projects.yml"
ACEPTED_PROJECTS = "accepted_projects.csv"
PROJECTS_REPOSITORY = "https://github.com/elixir-europe/BioHackathon-projects-2019/tree/master/projects/{number}"

# ACEPTED PROJECTS COLUMN NAMES
ACPT_PROJECT_NUMBER = "number"
ACPT_PROJECT_MERGED = "merged_from"
ACPT_PROJECT_TITLE = "title"
ACPT_PROJECT_SUBMITTER = "submitter"

# EASY CHAIR DUMP PROJECT COLUMNS
PROJECT_NUMBER = "#"
PROJECT_AUTHORS = "Authors"
PROJECT_TITLE = "Title"
PROJECT_HACKING_TOPIC = "Hacking topic"

PROJECT_LEADS = "Leads"
PROJECT_NOMINATED_PARTICIPANT = "Nominated_participant"
PROJECT_RESEARCH_AREA_ALIGNMENT = "Research area alignment"
PROJECT_EXPECTED_OUTCOMES = "Expected Outcomes"
PROJECT_EXPECTED_AUDIENCE = "Expected Audience"

PROJECT_NUMBER_OF_EXPECTED_HACKING_DAYS = "Number of Expected hacking days"
PROJECT_TIME = "Time"
PROJECT_DECISION = "Decision"

PROJECT_PAPER = "paper"


def load_accepted_projects():

    accepted_projects = []

    with open(ACEPTED_PROJECTS) as aprojects_file:

        reader = csv.DictReader(aprojects_file, delimiter=',')
        line_count = 0
        for row in reader:

            if line_count == 0:
                print(f'Accepted projects columns names are {", ".join(row)}')

            accepted_projects.append(row)
            line_count += 1

    return accepted_projects


def load_all_projects():
    projects = []

    with open(PROJECTS_FILE) as pro_file:
        reader = csv.DictReader(pro_file, delimiter=',')
        line_count = 0
        for row in reader:

            if line_count == 0:
                print(f'Projects column names are {", ".join(row)}')

            project = dict(
                number=row.get(PROJECT_NUMBER),
                title=row.get(PROJECT_TITLE),
                hacking_topic=row.get(PROJECT_HACKING_TOPIC),
                research_area_alignment=row.get(
                    PROJECT_RESEARCH_AREA_ALIGNMENT),
                number_of_expected_hacking_days=row.get(
                    PROJECT_NUMBER_OF_EXPECTED_HACKING_DAYS),
                authors=row.get(PROJECT_AUTHORS),
                leads=row.get(PROJECT_LEADS),
                nominated_participant=row.get(PROJECT_NOMINATED_PARTICIPANT),
                expected_outcomes=row.get(PROJECT_EXPECTED_OUTCOMES),
                expected_audience=row.get(PROJECT_EXPECTED_AUDIENCE)
            )
            projects.append(project)
            line_count += 1

    return projects


def to_file(project):

    path = "{}/{}".format(PROJECTS_FOLDER, project.get("number"))
    os.makedirs(path)

    file_name = "{}/{}/README.md".format(PROJECTS_FOLDER,
                                         project.get("number"))
    print("Creating file {}".format(file_name))

    with open(file_name, "w+") as output_file:
        output_file.write("# {}\n\n".format(project.get("title")))
        
        output_file.write(
            "**Project Number:** {}\n\n".format(project.get("number")))
                
        output_file.write("## Research area alignment\n\n")
        research_alignment = "\n".join(
            "- {}".format(project.get("research_area_alignment")) for project in project.get("merged_from"))
        output_file.write(research_alignment)

        if len(project.get("merged_from")) > 1:
            output_file.write("\n\n## Merged from\n\n")
            merged_titles = "\n".join("- {}".format(project.get("title"))
                                      for project in project.get("merged_from"))
            output_file.write(merged_titles)

        output_file.write("\n\n## Team\n\n")

        output_file.write(
            "**Submitter:** {}\n\n".format(project.get("submitter")))

        output_file.write("### Proponent(s)\n\n")

        authors = "\n".join("- {}".format(project.get("authors"))
                            for project in project.get("merged_from"))
        output_file.write(authors)

        output_file.write("\n\n### Lead(s)\n\n")
        leads = "\n".join("- {}".format(project.get("leads"))
                          for project in project.get("merged_from"))
        output_file.write(leads)

        output_file.write("\n\n### Nominated participant(s)\n\n")
        participant = "\n".join("- {}".format(project.get("nominated_participant"))
                                for project in project.get("merged_from"))
        output_file.write(participant)

        output_file.write("\n\n## Expected outcomes\n\n")
        expected_outcomes = "\n".join(
            "- {}".format(project.get("expected_outcomes")) for project in project.get("merged_from"))
        output_file.write(expected_outcomes)

        output_file.write("\n\n## Expected audience\n\n")
        expected_audience = "\n".join(
            "- {}".format(project.get("expected_audience")) for project in project.get("merged_from"))
        output_file.write(expected_audience)

        number_of_days = max(int(project.get("number_of_expected_hacking_days"))
                             for project in project.get("merged_from"))
        output_file.write(
            "\n\n**Number of expected hacking days**: {}\n\n".format(number_of_days))


def main():
    acpt_projects = load_accepted_projects()
    projects = load_all_projects()

    projects_yaml = []

    for acpt_project in acpt_projects:

        project_link = PROJECTS_REPOSITORY.format(
            number=acpt_project.get(ACPT_PROJECT_NUMBER))
        merged_from_list = acpt_project.get(ACPT_PROJECT_MERGED).split("|")

        merged_from_yaml = []
        merged_from = []

        for pr_num in merged_from_list:
            project_detail = next(
                (project for project in projects if project.get("number") == pr_num), None)
            project = dict(
                number=project_detail.get("number"),
                title=project_detail.get("title"),
                research_area_alignment=project_detail.get(
                    "research_area_alignment"),
                number_of_expected_hacking_days=project_detail.get(
                    "number_of_expected_hacking_days"),
                authors=project_detail.get("authors"),
                leads=project_detail.get("leads"),
            )
            merged_from_yaml.append(project)

            project = dict(
                number=project_detail.get("number"),
                title=project_detail.get("title"),
                hacking_topic=project_detail.get("hacking_topic"),
                research_area_alignment=project_detail.get(
                    "research_area_alignment"),
                number_of_expected_hacking_days=project_detail.get(
                    "number_of_expected_hacking_days"),
                authors=project_detail.get("authors"),
                leads=project_detail.get("leads"),
                nominated_participant=project_detail.get(
                    "nominated_participant"),
                expected_outcomes=project_detail.get("expected_outcomes"),
                expected_audience=project_detail.get("expected_audience")
            )

            merged_from.append(project)

        pro = dict(
            number=acpt_project.get(ACPT_PROJECT_NUMBER),
            title=acpt_project.get(ACPT_PROJECT_TITLE),
            submitter=acpt_project.get(ACPT_PROJECT_SUBMITTER),
            link=project_link,
            merged_from=merged_from_yaml
        )
        projects_yaml.append(pro)

        pro["merged_from"] = merged_from

        to_file(pro)

    yaml_projects = dict(
        project_list=projects_yaml
    )
    with open(PROJECTS_FILE) as pro_file, open(PROJECT_YAML, "w+") as yaml_output_file:
        yaml_output_file.write(
            yaml.dump(yaml_projects, default_flow_style=False))


if __name__ == '__main__':
    main()
