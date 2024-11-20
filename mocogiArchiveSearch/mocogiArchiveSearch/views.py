from django.http import JsonResponse
from django.views import View
from gitlab_api import GitlabAPI
from gitlab import AKGitlab
import base64
import yaml
class ProjectDetailByIdView(View):
    def get(self, request, project_id, *args, **kwargs):
        try:
            rest_api = GitlabAPI()
            gitlab_client = AKGitlab(api=rest_api)

            project = gitlab_client.projects.get_project_by_id(project_id)

            if project:
                return JsonResponse({
                    "success": True,
                    "project": project
                }, status=200)
            else:
                return JsonResponse({
                    "success": False,
                    "message": f"Project with ID '{project_id}' not found."
                }, status=404)
        except Exception as e:
            return JsonResponse({
                "success": False,
                "error": str(e)
            }, status=500)


class GetAllProjectsView(View):
    def get(self, request, *args, **kwargs):
        try:
            rest_api = GitlabAPI()
            gitlab_client = AKGitlab(api=rest_api)

            projects = gitlab_client.projects.get_all_projects()

            if projects:
                return JsonResponse({
                    "success": True,
                    "projects": projects
                }, status=200)
        except Exception as e:
            return JsonResponse({
                "success": False,
                "error": str(e)
            }, status=500)


class GetModulesView(View):
    def get(self, request, project_id, *args, **kwargs):
        try:
            rest_api = GitlabAPI()
            gitlab_client = AKGitlab(api=rest_api)

            all_module_files = gitlab_client.files.get_project_files(project_id=project_id, path="modules")

            enriched_modules = []

            for file in all_module_files:
                module = gitlab_client.files.get_file_content(project_id=project_id, file_path=file['path'])
                study_programs = []
                decoded_content = base64.b64decode(module['content']).decode('utf-8')
                try:
                    if decoded_content.startswith("---v1.0s"):
                        decoded_content = decoded_content.replace("---v1.0s", "---", 1)

                    if "---" not in decoded_content:
                        continue
                    yaml_content = yaml.safe_load(decoded_content.split('---', 2)[1])

                    study_programs = yaml_content.get('po_optional', [])
                except yaml.YAMLError as e:
                    print(f"Error parsing YAML for module {file['name']}: {e}")
                except Exception as e:
                    print(f"Unexpected error for module {file['name']}: {e}")
                enriched_module = {
                    "path": file["path"],
                    "file_name": file.get("name", "unknown"),
                    "module_id": file.get("id", "unknown"),
                    "study_programs": study_programs,
                    "content": decoded_content
                }

                enriched_modules.append(enriched_module)

            return JsonResponse({
                "success": True,
                "modules": enriched_modules
            }, status=200)
        except Exception as e:
            return JsonResponse({
                "success": False,
                "error": str(e)
            }, status=500)
