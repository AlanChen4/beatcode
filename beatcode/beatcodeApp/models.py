from django.db import models

class User(models.Model):
    uid = models.IntegerField(primary_key=True)
    leetcode_username = models.TextField(unique=True)
    password = models.TextField()
    last_login = models.DateField()
    is_active = models.BooleanField()
    is_admin = models.BooleanField()
    is_superuser = models.BooleanField()
 
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

    cat = models.TextField(
        max_length = 255,
        choices=CATEGORY_CHOICES,
        unique=True)
    last_done = models.DateField()

class Problem(models.Model):
    pid = models.IntegerField(primary_key=True)
    cat = models.ManyToManyField(Category)
    name = models.TextField()
    ## difficulty = models. what are the difficulty levels?
    
class ProblemSet(models.Model):
    psid = models.IntegerField(primary_key=True)
    name = models.TextField()

class Submission(models.Model):
    sid = models.IntegerField(primary_key=True)
    uid = models.ForeignKey(to=User, on_delete=models.CASCADE)
    pid = models.ForeignKey(to=Problem, on_delete=models.CASCADE)
    sub_date = models.DateField()
    runtime = models.IntegerField()
    mem_used = models.IntegerField()
    success = models.BooleanField()
    
class InSet(models.Model):
    pid = models.ForeignKey(Problem, on_delete=models.CASCADE)
    psid = models.ForeignKey(ProblemSet, on_delete=models.CASCADE) 


class ToDo(models.Model):
    uid = models.ManyToManyField(User)
    pid = models.ManyToManyField(Problem)
    progress = models.TextField()