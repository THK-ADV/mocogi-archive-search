import uuid

from django.db import models


def generate_uuid():
    return str(uuid.uuid4())


class Commit(models.Model):
    id = models.CharField(
        max_length=50,
        primary_key=True,
        default=generate_uuid,
        editable=False
    )
    date = models.DateField()
    semester = models.CharField(max_length=10, default='Winter')
    year = models.IntegerField()
    scanned = models.BooleanField(default=False)

    def __str__(self):
        return f"Commit {self.id} - {self.year}, Sem {self.semester}"


class Course(models.Model):
    id = models.CharField(
        max_length=50,
        primary_key=True,
        default=generate_uuid,
        editable=False
    )
    title = models.CharField(max_length=150, default='')
    abbrev = models.CharField(max_length=50, default='')
    recommended_semester = models.CharField(max_length=10, default='Both')
    commits = models.ManyToManyField(
        Commit,
        through='CourseCommit',
        related_name='courses'
    )
    programs = models.ManyToManyField(
        'StudyProgram',
        related_name='courses_programs'
    )


def __str__(self):
    return f"Course {self.id} - {self.title}"


class StudyProgram(models.Model):
    id = models.CharField(
        max_length=50,
        primary_key=True,
        default=generate_uuid,
        editable=False
    )
    enLabel = models.CharField(max_length=200)
    deLabel = models.CharField(max_length=200)

    def __str__(self):
        return f"Course {self.id} - {self.enLabel}"


class CourseCommit(models.Model):
    id = models.CharField(
        max_length=100,
        primary_key=True,
        default=generate_uuid,
        editable=False
    )
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    commit = models.ForeignKey(Commit, on_delete=models.CASCADE)
    file_path = models.CharField(max_length=200)

    def __str__(self):
        return f"CourseCommit {self.id} - {self.course.id} - {self.commit.id}"
