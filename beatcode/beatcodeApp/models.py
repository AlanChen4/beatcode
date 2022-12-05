from django.db import models
from authentication.models import CustomUser as User
import uuid
 
class Category(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name


class ProblemSet(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Problem(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    category = models.ManyToManyField(Category, blank=True)
    name = models.CharField(max_length=255)
    problem_set = models.ManyToManyField(ProblemSet, blank=True)
    difficulty = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.name  


class Submission(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    problem = models.ForeignKey(to=Problem, on_delete=models.CASCADE)
    sub_date = models.DateField()
    runtime = models.IntegerField()
    mem_used = models.IntegerField()
    success = models.BooleanField()

    def __str__(self):
        return f"{self.user.email}: {self.problem.name}"


class ToDo(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.CASCADE, blank=True, null=True)
    problem = models.ForeignKey(to=Problem, on_delete=models.CASCADE, blank=True, null=True)
    complete = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.email}: {self.problem.name}: {'Complete' if self.complete else 'Incomplete'}"
