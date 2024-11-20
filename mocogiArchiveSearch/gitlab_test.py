# ----------------------------------------------------------------------------------------------------------------------
# Imports
# ----------------------------------------------------------------------------------------------------------------------
import unittest
import base64
from gitlab import AKGitlab
from gitlab_api import GitlabAPI

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
    all_module_files = self.gitlab.files.get_project_files(project_id=project_id, path="modules")
    for file in all_module_files:
      module = self.gitlab.files.get_file_content(project_id=project_id, file_path=f"{file['path']}")
      print(module)
      decoded_content = base64.b64decode(module['content']).decode('utf-8')
      print(decoded_content)


# ----------------------------------------------------------------------------------------------------------------------
# Start Script
# ----------------------------------------------------------------------------------------------------------------------
if __name__ == '__main__':
  unittest.main()
