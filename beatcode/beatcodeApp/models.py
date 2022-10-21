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
    category = models.CharField(
        max_length=255,
        choices=CATEGORY_CHOICES,
        unique=True)
    last_done = models.DateField()

    def __str__(self):
        return self.category

class Problem(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    name = models.CharField(max_length=255)
    category = models.ForeignKey(to=Category, on_delete=models.CASCADE, blank=True, null=True)
    ## difficulty = models. what are the difficulty levels? 

    def __str__(self):
        return self.name  

class ProblemSet(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    name = models.CharField(unique=True, max_length=255)

    def __str__(self):
        return self.name

class ProblemToProblemSet(models.Model):
    problem = models.ForeignKey(to=Problem, on_delete=models.CASCADE)
    problem_set = models.ForeignKey(to=ProblemSet, on_delete=models.CASCADE)

class Submission(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    problem = models.ForeignKey(to=Problem, on_delete=models.CASCADE)
    sub_date = models.DateField()
    runtime = models.IntegerField()
    mem_used = models.IntegerField()
    success = models.BooleanField()

class ToDo(models.Model):
    user = models.ManyToManyField(User)
    problem = models.ManyToManyField(Problem)
    progress = models.CharField(max_length=255)