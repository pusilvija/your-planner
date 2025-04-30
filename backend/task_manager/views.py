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
from .forms import TaskForm
from django.db.models import F
from rest_framework import status

from rest_framework.generics import RetrieveUpdateAPIView, CreateAPIView, DestroyAPIView


class TaskDeleteView(DestroyAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    lookup_field = 'id'


class TaskDetailView(RetrieveUpdateAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    lookup_field = 'id'


class AddTaskView(APIView):
    def post(self, request):
        # Deserialize the incoming data
        serializer = TaskSerializer(data=request.data)
        if serializer.is_valid():
            # Check if all fields are empty
            cleaned_data = serializer.validated_data
            if all(not value for value in cleaned_data.values()):
                return Response(
                    {"error": "Task data cannot be empty."},
                    status=rf_status.HTTP_400_BAD_REQUEST
                )

            # Set a default value for 'category' if it's missing or empty
            if not cleaned_data.get('category'):
                cleaned_data['category'] = "Uncategorized"

            # Shift all existing tasks' order up by 1
            Task.objects.update(order=F('order') + 1)

            # Create the new task with order = 0
            new_task = serializer.save(order=0)

            return Response(
                TaskSerializer(new_task).data,
                status=rf_status.HTTP_201_CREATED
            )

        # Return validation errors
        return Response(
            {"errors": serializer.errors},
            status=rf_status.HTTP_400_BAD_REQUEST
        )


class TaskBoardView(APIView):
    def get(self, request):
        tasks = Task.objects.all().order_by('order')
        grouped = defaultdict(list)

        for task in tasks:
            grouped[task.status].append(TaskSerializer(task).data)

        return Response(grouped)

    def post(self, request):
        data = request.data

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
