from django.db import models
from authentication.models import CustomUser as User
import uuid

 
class Category(models.Model):
    ARRAY = 'AR'
    BINARY = 'BI'
    DYN_PROG = 'DP'
    GRAPH = 'GR'
    INTERVAL = 'IN'
    LINKED_LIST = 'LL'
    MATRIX = 'MX'
    STRING = 'ST'
    TREE = 'TR'
    HEAP = 'HE'
    
    CATEGORY_CHOICES = [
        (ARRAY, 'Array'),
        (BINARY, 'Binary'),
        (DYN_PROG, 'Dynamic Programming'),
        (GRAPH, 'Graph'),
        (INTERVAL, 'Interval'),
        (LINKED_LIST, 'Linked List'),
        (MATRIX, 'Matrix'),
        (STRING, 'String'),
        (TREE, 'Tree'),
        (HEAP, 'Heap')
    ]
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    name = models.CharField(max_length=255, choices=CATEGORY_CHOICES, unique=True)

    def __str__(self):
        return self.get_name_display()


class ProblemSet(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Problem(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    category = models.ManyToManyField(Category)
    name = models.CharField(max_length=255)
    problem_set = models.ManyToManyField(ProblemSet, blank=True)

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
