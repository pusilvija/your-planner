from collections import defaultdict

from django.db.models import F
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from django.utils.decorators import method_decorator

from rest_framework import status as rf_status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import RetrieveUpdateAPIView, DestroyAPIView
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.decorators import api_view, permission_classes

from .models import Task
from .serializers import TaskSerializer, UserSerializer, LoginSerializer


class TaskDeleteView(DestroyAPIView):
    serializer_class = TaskSerializer
    lookup_field = 'id'

    def get_queryset(self):
        return Task.objects.filter(user=self.request.user)
    
    def get_object(self):
        queryset = self.get_queryset()
        obj = queryset.get(id=self.kwargs["id"])
        return obj
        

class TaskDetailView(RetrieveUpdateAPIView):
    serializer_class = TaskSerializer
    lookup_field = 'id'

    def get_queryset(self):
        return Task.objects.filter(user=self.request.user)
    
    def get_object(self):
        queryset = self.get_queryset()
        obj = queryset.get(id=self.kwargs["id"])
        return obj
    

class AddTaskView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = TaskSerializer(data=request.data, context={'request': request})

        if serializer.is_valid():
            cleaned_data = serializer.validated_data

            if not cleaned_data.get('category'):
                cleaned_data['category'] = "Uncategorized"

            Task.objects.filter(user=request.user).update(order=F('order') + 1)
            new_task = serializer.save(order=0, user=request.user)

            return Response(
                TaskSerializer(new_task).data,
                status=rf_status.HTTP_201_CREATED
            )

        return Response(
            {"errors": serializer.errors},
            status=rf_status.HTTP_400_BAD_REQUEST
        )
    

class TaskBoardView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        tasks = Task.objects.filter(user=request.user).order_by('order')
        grouped = defaultdict(list)

        for task in tasks:
            grouped[task.status].append(TaskSerializer(task).data)

        return Response(grouped)

    def post(self, request):
        data = request.data

        for status, task_list in data.items():
            for task_data in task_list:
                try:
                    task = Task.objects.get(id=task_data["id"], user=request.user)
                    task.status = status
                    task.order = task_data["order"]
                    task.save()
                except Task.DoesNotExist:
                    continue

        return Response({"message": "Tasks updated successfully."}, status=rf_status.HTTP_200_OK)
    
    
@method_decorator(csrf_exempt, name='dispatch')
class RegisterView(APIView):
    permission_classes = [AllowAny] 

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            token, created = Token.objects.get_or_create(user=user)
            return Response({
                "token": token.key,
                "user_id": user.id
            }, status=rf_status.HTTP_201_CREATED)
        return Response(serializer.errors, status=rf_status.HTTP_400_BAD_REQUEST)
    

@method_decorator(csrf_exempt, name='dispatch')
class LoginView(APIView):
    permission_classes = [AllowAny] 
    
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data
            token, created = Token.objects.get_or_create(user=user)
            return Response({"token": token.key})
        return Response(serializer.errors, status=rf_status.HTTP_400_BAD_REQUEST)
    

class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        request.user.auth_token.delete()
        return Response({"message": "Logged out successfully"}, status=200)


class TasksPageView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        tasks = Task.objects.filter(user=request.user).order_by('order')
        serialized_tasks = TaskSerializer(tasks, many=True).data
        return Response(serialized_tasks, status=rf_status.HTTP_200_OK)

    def post(self, request):
        data = request.data 
        errors = []

        for task_data in data:
            try:
                task = Task.objects.get(id=task_data["id"], user=request.user)

                for field, value in task_data.items():
                    if field != "id":
                        setattr(task, field, value)

                task.save()
            except Task.DoesNotExist:
                errors.append({"id": task_data["id"], "error": "Task does not exist"})
            except Exception as e:
                errors.append({"id": task_data.get("id"), "error": str(e)})

        if errors:
            return Response({"errors": errors}, status=rf_status.HTTP_400_BAD_REQUEST)

        return Response({"message": "Tasks updated successfully."}, status=rf_status.HTTP_200_OK)
