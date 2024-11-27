# ----------------------------------------------------------------------------------------------------------------------
# Imports
# ----------------------------------------------------------------------------------------------------------------------
from gitlab_api import GitlabAPI
# ----------------------------------------------------------------------------------------------------------------------
# Classes
# ----------------------------------------------------------------------------------------------------------------------
class AKGitlab:

  class Exception(Exception):
    pass

  class DataObject:

    class CompareState:
      not_equal = 0  # the items are not equal at all
      id_is_equal = 1  # the id is equal, but the data itself are not equal
      equal = 2  # the items are identical


  class Users(DataObject):

    def __init__(self, api: GitlabAPI, data: dict):
      self.api = api
      self.data = data

    def get_all_users(self):
      return self.api.users.get_all_users()

    def get_user_id_by_username(self, username: str):
      return self.api.users.get_user_id_by_username(username=username)

    def get_user_by_id(self, user_id: str):
      return self.api.users.get_user_by_id(user_id=user_id)

    def get_user_by_email(self, user_email: str):
      return self.api.users.get_user_by_email(user_email=user_email)

  class Tags(DataObject):

    def __init__(self, api: GitlabAPI, data: dict):
      self.api = api
      self.data = data

    def set_tag_on_commit(self, project_id: str, ref: str, tag_name: str):
      return self.api.tags.set_tag_on_commit(project_id=project_id, ref=ref, tag_name=tag_name)

  class Commits(DataObject):

    def __init__(self, api: GitlabAPI, data: dict):
      self.api = api
      self.data = data

    def get_commit_by_id(self, project_id: int, commit_id: str):
      return self.api.commits.get_commit_by_id(project_id=project_id, commit_id=commit_id)

    def get_all_commits(self, project_id: int, ref_name: str = None):
      return self.api.commits.get_all_commits(project_id=project_id, ref_name=ref_name)

  class Branches(DataObject):

    def __init__(self, api: GitlabAPI, data: dict):
      self.api = api
      self.data = data

    def get_all_branches(self, project_id: int):
      return self.api.branches.get_all_branches(project_id=project_id)

    def get_branch_by_name(self, project_id: int, branch_name: str):
      return self.api.branches.get_branch_by_name(project_id=project_id, branch_name=branch_name)

  class Projects(DataObject):

    def __init__(self, api: GitlabAPI, data: dict):
      self.api = api
      self.data = data

    def get_all_projects(self):
      return self.api.projects.get_all_projects()

    def get_project_by_id(self, project_id: int):
      return self.api.projects.get_project_by_id(project_id=project_id)

    def get_project_by_name(self, project_name: str):
      return self.api.projects.get_project_by_name(project_name=project_name)

  class Files(DataObject):

    def __init__(self, api: GitlabAPI, data: dict):
      self.api = api
      self.data = data

    def get_project_files(self, project_id: int, path: str = "", ref: str = "main", page: int = 0, per_page: int = 100):
      return self.api.files.get_project_files(project_id=project_id, path=path, ref=ref, page=page, per_page=per_page)

    def get_file_content(self, project_id: int, file_path: str, ref: str = "main"):
      return self.api.files.get_file_content(project_id=project_id, file_path=file_path, ref=ref)

  def __init__(self, api: GitlabAPI):
    self.api = api
    self.data = {}
    self.users = self.Users(self.api, self.data)
    self.commits = self.Commits(self.api, self.data)
    self.branches = self.Branches(self.api, self.data)
    self.projects = self.Projects(self.api, self.data)
    self.tags = self.Tags(self.api, self.data)
    self.files = self.Files(self.api, self.data)
