# ----------------------------------------------------------------------------------------------------------------------
# Imports
# ----------------------------------------------------------------------------------------------------------------------
import urllib.parse
import yaml
from rest_api_client import RestAPIClient
from web_request import WebRequest


# ----------------------------------------------------------------------------------------------------------------------
# GitlabAPI Class
# ----------------------------------------------------------------------------------------------------------------------
class GitlabAPI(RestAPIClient):
    class Exception(Exception):
        pass

    class UsersAPI:
        def __init__(self, api: RestAPIClient):
            self.api = api

        def get_all_users(self):
            return self.api.get_json(url="users", params={}, data={'per_page': 100})

        def get_user_id_by_username(self, username: str):
            users = self.get_all_users()
            for user in users:
                if user["username"] == username:
                    return user["id"]
            return None

        def get_user_by_id(self, user_id: str):
            return self.api.get_json(url=f"users/{user_id}", params={}, data={})

        def get_user_by_email(self, user_email: str):
            users = self.get_all_users()
            for user in users:
                if user["public_email"] == user_email:
                    return user
            return None

    class TagsAPI:
        def __init__(self, api: RestAPIClient):
            self.api = api

        def set_tag_on_commit(self, project_id: str, ref: str, tag_name: str):
            return self.api.post_json(url=f"projects/{project_id}/repository/tags", data={
                "tag_name": tag_name,
                "ref": ref
            })

    class CommitsAPI:
        def __init__(self, api: RestAPIClient):
            self.api = api

        def get_commit_by_id(self, project_id: int, commit_id: str):
            return self.api.get_json(url=f"projects/{project_id}/repository/commits/{commit_id}", params={}, data={})

        def get_all_commits(self, project_id: int, ref_name: str = None):
            params = {"ref_name": ref_name} if ref_name else {}
            return self.api.get_json(url=f"projects/{project_id}/repository/commits", params=params, data={})

    class BranchesAPI:
        def __init__(self, api: RestAPIClient):
            self.api = api

        def get_all_branches(self, project_id: int):
            return self.api.get_json(url=f"projects/{project_id}/repository/branches", params={}, data={})

        def get_branch_by_name(self, project_id: int, branch_name: str):
            return self.api.get_json(url=f"projects/{project_id}/repository/branches/{branch_name}", params={}, data={})

    class ProjectsAPI:
        def __init__(self, api: RestAPIClient):
            self.api = api

        def get_all_projects(self):
            return self.api.get_json(url="projects", params={}, data={'per_page': 100})

        def get_project_by_id(self, project_id: int):
            return self.api.get_json(url=f"projects/{project_id}", params={}, data={})

        def get_project_by_name(self, project_name: str):
            projects = self.get_all_projects()
            for project in projects:
                if project["name"] == project_name:
                    return project
            return None

    class FilesAPI:
        def __init__(self, api: RestAPIClient):
            self.api = api

        def get_file_content(self, project_id: int, file_path: str, ref: str = "main"):
            encoded_file_path = urllib.parse.quote(file_path, safe='')
            url = f"projects/{project_id}/repository/files/{encoded_file_path}"
            params = {"ref": ref}
            return self.api.get_json(url=url, params=params)

        def get_project_files(self, project_id: int, path: str = "", ref: str = "main"):
            url = f"projects/{project_id}/repository/tree"
            params = {
                "path": path,
                "ref": ref,
                "recursive": False
            }
            return self.api.get_json(url=url, params=params, data={})

    def __init__(self, config_file: str = "config.yaml"):
        with open(config_file, "r") as file:
            config = yaml.safe_load(file)

        access_token = config["gitlab"]["access_token"]
        base_url = config["gitlab"]["base_url"]

        # Set up API client
        default_headers = {"PRIVATE-TOKEN": access_token}
        super().__init__(web_request=WebRequest(), default_headers=default_headers, base_url=base_url)

        self.users = self.UsersAPI(api=self)
        self.projects = self.ProjectsAPI(api=self)
        self.commits = self.CommitsAPI(api=self)
        self.branches = self.BranchesAPI(api=self)
        self.tags = self.TagsAPI(api=self)
        self.files = self.FilesAPI(api=self)
