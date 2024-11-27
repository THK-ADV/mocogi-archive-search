# ----------------------------------------------------------------------------------------------------------------------
# Imports
# ----------------------------------------------------------------------------------------------------------------------
import re
import unittest
import base64
from gitlab import AKGitlab
from gitlab_api import GitlabAPI
import yaml
# ----------------------------------------------------------------------------------------------------------------------
# Classes
# ----------------------------------------------------------------------------------------------------------------------
class GitlabRestAPIClientUnitTest(unittest.TestCase):

  @classmethod
  def setUpClass(cls):
    rest_api = GitlabAPI()
    cls.gitlab = AKGitlab(api=rest_api)

  def test_001_get_all_users(self):
    users = self.gitlab.users.get_all_users()
    for user in users:
      print("name: " + user["name"] + "; username: " + user["username"], "; id: " + str(user["id"]))

  def test_002_get_user_by_id(self):
    user_id = "1736"
    user = self.gitlab.users.get_user_by_id(user_id=user_id)
    print(user)

  def test_003_get_all_names_of_projects(self):
    projects = self.gitlab.projects.get_all_projects()
    for project in projects:
      print(project["name"])

  def test_004_get_commit_by_id(self):
    project_id = 3020
    commit_id = "a4e4b96340a2f6ba50b38ebb236045570ae25a82"
    commit = self.gitlab.commits.get_commit_by_id(project_id=project_id, commit_id=commit_id)
    self.assertIsNotNone(commit)
    print(commit)

  def test_005_get_all_commits(self):
    project_id = 3020
    ref_name = "main"
    commits = self.gitlab.commits.get_all_commits(project_id=project_id, ref_name=ref_name)
    self.assertTrue(len(commits) > 0)
    print(commits)

  def test_006_get_all_branches(self):
    project_id = 3020
    branches = self.gitlab.branches.get_all_branches(project_id=project_id)
    self.assertTrue(len(branches) > 0)
    print(branches)

  def test_007_get_branch_by_name(self):
    project_id = 3020
    branch_name = "main"
    branch = self.gitlab.branches.get_branch_by_name(project_id=project_id, branch_name=branch_name)
    self.assertIsNotNone(branch)
    print(branch)

  def test_008_get_all_projects(self):
    projects = self.gitlab.projects.get_all_projects()
    self.assertTrue(len(projects) > 0)
    for project in projects:
      print(project)

  def test_009_get_project_by_id(self):
    project_id = 3020
    project = self.gitlab.projects.get_project_by_id(project_id=project_id)
    self.assertIsNotNone(project)
    print(project)

  def test_010_get_files_of_project(self):
    project_id = 3020
    response = self.gitlab.files.get_project_files(project_id=project_id, path="modules")
    print(response)

  def test_011_get_all_modules(self):
      project_id = 3020
      path = "modules"
      all_module_files = []
      page = 1
      per_page = 100  # Maximale Anzahl von Einträgen pro Anfrage (abhängig von GitLab-API)

      while True:
          # Abrufen der Dateien für die aktuelle Seite
          module_files = self.gitlab.files.get_project_files(
              project_id=project_id,
              path=path,
              ref="main",
              page=page, per_page=per_page
          )

          # Breche die Schleife ab, wenn keine weiteren Dateien vorhanden sind
          if not module_files:
              break

          # Füge die Ergebnisse zur Liste hinzu
          all_module_files.extend(module_files)
          page += 1

      print(f"Total modules fetched: {len(all_module_files)}")
      for file in all_module_files:
          module = self.gitlab.files.get_file_content(project_id=project_id, file_path=f"{file['path']}")
          print(module)

  def test_012_get_all_modules_with_study_programs(self):
      """
      Test fetching and cleaning module content and extracting study programs.
      """

      def clean_yaml_content(content):
          """
          Cleans and prepares YAML content:
          - Replaces invalid headers.
          - Handles duplicated colons and malformed keys.
          - Strips invalid lines.
          """
          if content.startswith("---v1.0s"):
              content = content.replace("---v1.0s", "---", 1)
          elif content.startswith("---v1s"):
              content = content.replace("---v1s", "---", 1)

          # Replace tabs with spaces
          content = content.replace("\t", "  ")

          # Fix malformed colons
          content = re.sub(r":\s*:", ":", content)

          # Remove invalid lines
          content = re.sub(r"^\s*:\s*$", "", content, flags=re.MULTILINE)

          # Split lines and process further
          lines = content.split("\n")
          cleaned_lines = []
          for line in lines:
              if line.count(":") > 1 and not line.strip().startswith("-"):
                  parts = line.split(":")
                  line = ":".join(parts[:2])  # Fix duplicated keys
              cleaned_lines.append(line)

          return "\n".join(cleaned_lines).strip()

      project_id = 3020
      error_log = []

      try:
          # Retrieve all module files
          all_module_files = self.gitlab.files.get_project_files(project_id=project_id, path="modules")

          for file in all_module_files:
              file_name = file.get("name", "unknown")

              try:
                  # Fetch and decode content
                  module = self.gitlab.files.get_file_content(project_id=project_id, file_path=file['path'])
                  decoded_content = base64.b64decode(module['content']).decode('utf-8')

                  print(f"Decoded content for module {file_name}:\n{decoded_content}\n{'-' * 50}")

                  # Clean the content
                  cleaned_content = clean_yaml_content(decoded_content)

                  # Validate YAML delimiter
                  if "---" not in cleaned_content:
                      print(f"Warning: No valid YAML delimiter found for module {file_name}. Skipping.")
                      error_log.append((file_name, "No valid YAML delimiter found"))
                      continue

                  # Extract YAML content
                  yaml_parts = cleaned_content.split('---')
                  if len(yaml_parts) < 2:
                      print(f"Warning: Malformed YAML structure in module {file_name}. Skipping.")
                      error_log.append((file_name, "Malformed YAML structure"))
                      continue

                  yaml_block = yaml_parts[1]

                  try:
                      # Parse YAML content
                      yaml_content = yaml.safe_load(yaml_block)

                      # Extract study programs
                      study_programs = yaml_content.get('po_optional', []) + yaml_content.get('po_mandatory', [])
                      print(f"Study programs for module {file_name}:")
                      for program in study_programs:
                          print(f"  - {program.get('study_program', 'Unknown')}")
                  except yaml.YAMLError as e:
                      print(f"Error parsing YAML for module {file_name}: {e}")
                      error_log.append((file_name, f"YAML parsing error: {e}"))
                      continue

              except Exception as e:
                  print(f"Unexpected error for module {file_name}: {e}")
                  error_log.append((file_name, f"Unexpected error: {e}"))

          # Log error summary
          if error_log:
              print("\nSummary of problematic modules:")
              for module_name, error in error_log:
                  print(f"Module: {module_name}, Error: {error}")

      except Exception as e:
          print(f"Error while processing modules: {e}")


# ----------------------------------------------------------------------------------------------------------------------
# Start Script
# ----------------------------------------------------------------------------------------------------------------------
if __name__ == '__main__':
  unittest.main()
