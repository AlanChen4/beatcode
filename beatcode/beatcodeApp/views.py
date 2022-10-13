from django.http import JsonResponse
from django.views import View


class Home(View):

    def get(self, request, *args, **kwargs):
        return JsonResponse({'foo': 'bar'})
