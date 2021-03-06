from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views import View

from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from computeserver.tasks import execute_nf

from celery.result import AsyncResult

class TaskView(APIView):
    def get(self, request, **kwargs):
        result = execute_nf.delay()
        return JsonResponse({'task_uid':result.id, 'state': result.state}, status=200, safe=False)

class TaskViewCheck(APIView):
    def get(self, request, **kwargs):
        task_uid = kwargs.get('task_uid', None)
        result = AsyncResult(task_uid)
        print(result)
        return JsonResponse({'state':result.state}, status=200, safe=False)

class CopyRunView(APIView):
    def get(self, request, **kwargs):
        result = execute_nf.delay()
        return JsonResponse({'task_uid':result.id, 'state': result.state}, status=200, safe=False)
