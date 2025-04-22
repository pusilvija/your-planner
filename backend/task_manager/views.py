from .models import Task
from collections import defaultdict

from rest_framework.response import Response
from .models import Task
from .serializers import TaskSerializer
from rest_framework.views import APIView

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status as rf_status
from .models import Task
from .serializers import TaskSerializer
from collections import defaultdict

from rest_framework.generics import RetrieveAPIView


class TaskDetailView(RetrieveAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    lookup_field = 'id'  


class TaskBoardView(APIView):
    def get(self, request):
        tasks = Task.objects.all().order_by('order')
        grouped = defaultdict(list)

        for task in tasks:
            grouped[task.status].append(TaskSerializer(task).data)

        return Response(grouped)

    def post(self, request):
        data = request.data  # expected: { "to do": [{id, order}], ... }

        for status, task_list in data.items():
            for task_data in task_list:
                try:
                    task = Task.objects.get(id=task_data["id"])
                    task.status = status
                    task.order = task_data["order"]
                    task.save()
                except Task.DoesNotExist:
                    continue

        return Response({"message": "Tasks updated successfully."}, status=rf_status.HTTP_200_OK)
