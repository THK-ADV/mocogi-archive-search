import json

import gitlab
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render
from rest_framework.views import APIView
from commits.models import StudyProgram, Course, Commit, CourseCommit
from modules.read_config_file import ReadConfigFile
PERSONAL_ACCESS_TOKEN = ""
GITLAB_URL = ""
PROJECT_ID = ""


def parse_project_data():
    global PERSONAL_ACCESS_TOKEN, GITLAB_URL, PROJECT_ID
    config_reader = ReadConfigFile()
    content = config_reader.read_file()
    PERSONAL_ACCESS_TOKEN = content['gitlab']['access_token']
    GITLAB_URL = content['gitlab']['base_url']
    PROJECT_ID = content['gitlab']['project_id']


def get_study_programs():
    parse_project_data()
    # Query all StudyProgram instances and get their deLabel values
    study_programs = StudyProgram.objects.all()
    programs = [{"id": sp.id, "deLabel": sp.deLabel} for sp in
                study_programs]  # List comprehension to extract deLabel values
    print(programs)
    return programs


def get_courses_for_study_program(study_program_id, semester):
    # Retrieve the specific StudyProgram instance
    study_program = StudyProgram.objects.get(id=study_program_id)
    print('study_program: ', study_program)
    # Filter courses that have this study program associated with them
    courses = Course.objects.filter(programs=study_program, recommended_semester__in=[semester, 'Both'])
    print(len(courses))
    modules = [{"id": co.id, "title": co.title} for co in courses]
    return modules


def get_template_view(request):
    context = {
        'title': 'Select Example',
        'options': get_study_programs(),
    }
    return render(request, "my_template.html", context)


def get_file_content(file_path, commit_id):
    # Initialize GitLab connection
    gl = gitlab.Gitlab(GITLAB_URL, private_token=PERSONAL_ACCESS_TOKEN)

    # Get the project
    project = gl.projects.get(PROJECT_ID)

    # Get the file content
    file_data = project.files.get(file_path=file_path, ref=commit_id)

    # Decode the file content
    content = file_data.decode()
    commits = project.commits.list(file_path=file_path, ref=commit_id)
    print('*******************', commits)
    print(f"Commit history for '{file_path}':")
    for commit in commits:
        print(f"Commit ID: {commit.id}")
        print(f"Author: {commit.author_name}")
        print(f"Date: {commit.created_at}")
        print(f"Message: {commit.message}")
        print("-" * 50)
        return content


class get_courses_view(APIView):
    def post(self, request):
        data = json.loads(request.body)
        dep = data.get('dep')
        semester = data.get('semester')
        data = get_courses_for_study_program(dep, semester)
        return JsonResponse(data, safe=False)


class get_course_data_view(APIView):

    def post(self, request):
        data = json.loads(request.body)
        course_id = data.get('courseId')
        year = data.get('year')
        semester = data.get('semester')
        print(year, semester)
        print(type(year), type(semester))
        try:
            course = Course.objects.get(id=course_id)
            print('course: ', course)
            commit = Commit.objects.get(year=year, semester=semester)
            print('commit: ', commit)
            course_commit = CourseCommit.objects.get(course=course, commit=commit)
            print('course_commit: ', course_commit)
            file_content = get_file_content(course_commit.file_path, commit.id)
            return HttpResponse(file_content, content_type="text/plain")
        except Course.DoesNotExist:
            return JsonResponse('There Is No File For This Year.', safe=False)
        except Commit.DoesNotExist:
            return JsonResponse('There Is No File For This Year.', safe=False)
        except CourseCommit.DoesNotExist:
            return JsonResponse('There Is No File For This Year.', safe=False)
        except gitlab.exceptions.GitlabGetError as e:
            print(f"Error fetching file: {e}")
        return JsonResponse('Some Thing Went Wrong!', safe=False)
