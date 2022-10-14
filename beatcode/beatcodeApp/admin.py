from django.contrib import admin
from .models import *

admin.site.register(User)
admin.site.register(Category)
admin.site.register(Problem)
admin.site.register(ProblemSet)
admin.site.register(Submission)
admin.site.register(InSet)
admin.site.register(ToDo)