import json
from datetime import datetime

import gitlab

from commits.models import Course, StudyProgram, Commit, CourseCommit
from modules.read_config_file import ReadConfigFile


class InitialData:
    DATA_FILE_PATH = "data.json"
    PERSONAL_ACCESS_TOKEN = ""
    GITLAB_URL = ""
    PROJECT_ID = ""

    @staticmethod
    def load_json(file_path):
        try:
            with open(file_path, "r", encoding="utf-8") as file:
                return json.load(file)
        except (FileNotFoundError, json.JSONDecodeError) as e:
            print(f"Error loading JSON: {e}")
            return []

    def parse_project_data(self):
        config_reader = ReadConfigFile()
        content = config_reader.read_file()
        self.PERSONAL_ACCESS_TOKEN = content['gitlab']['access_token']
        self.GITLAB_URL = content['gitlab']['base_url']
        self.PROJECT_ID = content['gitlab']['project_id']

    def parse_modules(self):
        print(' Start parse Modules and study Programs.')
        json_data = self.load_json(self.DATA_FILE_PATH)

        for module_data in json_data:
            semester = module_data["studyProgram"][0]["recommendedSemester"]
            recommended_semester = ''
            if not semester:
                recommended_semester = 'Both'
            else:
                for s in semester:
                    if s % 2 == 1:
                        if recommended_semester == '' or recommended_semester == 'Winter':
                            recommended_semester = 'Winter'
                        else:
                            recommended_semester = 'Both'
                    if s % 2 == 0:
                        if recommended_semester == '' or recommended_semester == 'Summer':
                            recommended_semester = 'Summer'
                        else:
                            recommended_semester = 'Both'

            module, create = Course.objects.get_or_create(id=module_data["id"], title=module_data["title"],
                                                          abbrev=module_data["abbrev"],
                                                          recommended_semester=recommended_semester)

            for study_program in module_data["studyProgram"]:
                program, sp_created = StudyProgram.objects.get_or_create(id=study_program["studyProgram"]["deLabel"],
                                                                         enLabel=study_program["studyProgram"][
                                                                             "enLabel"],
                                                                         deLabel=study_program["studyProgram"][
                                                                             "deLabel"])
                module.programs.add(program)
        print(' End parse Modules and study Programs.')

    def parse_commits(self):
        self.parse_project_data()
        print(' Start parse Commits')
        gl = gitlab.Gitlab(self.GITLAB_URL, private_token=self.PERSONAL_ACCESS_TOKEN)
        project = gl.projects.get(self.PROJECT_ID)
        commits = project.commits.list(ref_name='main', all=True)
        sorted_commits = sorted(commits, key=lambda commit: commit.committed_date, reverse=True)
        lastMonth = datetime.strptime(sorted_commits[0].committed_date, "%Y-%m-%dT%H:%M:%S.%f%z").date().month
        month = 8
        semester = 'Winter'
        if lastMonth < 9:
            month = 2
            semester = 'Summer'
        for commit in sorted_commits:
            commit_date = datetime.strptime(commit.committed_date, "%Y-%m-%dT%H:%M:%S.%f%z").date()
            # print(commit_date.month, month, commit_date.month == month)
            if commit_date.month == month:
                commit1, create = Commit.objects.get_or_create(id=commit.id, date=commit_date, year=commit_date.year,
                                                               semester=semester)
                if month == 8:
                    month = 2
                    semester = 'Summer'
                else:
                    month = 8
                    semester = 'Winter'
        print(' End parse Commits')

    def scan_commits(self):
        self.parse_project_data()
        print(' Start Scann Commits')
        commits = Commit.objects.all()
        gl = gitlab.Gitlab(self.GITLAB_URL, private_token=self.PERSONAL_ACCESS_TOKEN)
        project = gl.projects.get(self.PROJECT_ID)

        for commit in commits:
            print('************* ')
            if commit.scanned:
                continue
            items = project.repository_tree(ref=commit.id, recursive=True, get_all=True)
            ind = 0
            # Print file and folder paths at this commit

            for item in items:
                file_path = item['path']
                if item['type'] == 'blob' and '.md' in file_path and 'README' not in file_path:  # File
                    # print(f"  File: {item['path']}")
                    self.parse_file_data(commit.id, file_path)
                    ind += 1

            print('commit files= ', ind)
        print(' End Scann Commits')

    def parse_file_data(self, commit_id, file_path):
        gl = gitlab.Gitlab(self.GITLAB_URL, private_token=self.PERSONAL_ACCESS_TOKEN)
        project = gl.projects.get(self.PROJECT_ID)
        file_data = project.files.get(file_path=file_path, ref=commit_id).decode()
        if isinstance(file_data, bytes):  # Only decode if it's a bytes-like object
            file_data = file_data.decode('utf-8')
        for line in file_data.splitlines():
            if line.startswith('id:') or line.startswith('module_code:'):
                course_id = line.split(':', 1)[1].strip()
                self.add_course_commit(course_id, commit_id, file_path)
                print(f"ID: {course_id}")
                break

    def add_course_commit(self, course_id, commit_id, file_path):
        try:
            course = Course.objects.get(id=course_id)
            commit = Commit.objects.get(id=commit_id)
            CourseCommit.objects.get_or_create(id=commit_id + '-' + course_id, course=course, commit=commit,
                                               file_path=file_path)
            print(f"CourseCommit Added..")
        except Course.DoesNotExist:
            print(f"An error occurred:")
        except Commit.DoesNotExist:
            print(f"An error occurred: ")
        except CourseCommit.DoesNotExist:
            CourseCommit.objects.create(course=course, commit=commit, file_path=file_path)
            print(f"CourseCommit Added..")
        except Exception as e:
            print(f"An error occurred: {e}")
