from collections import defaultdict
from django.db.models import F
from django.contrib.auth.models import User
from rest_framework import status as rf_status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import RetrieveUpdateAPIView, DestroyAPIView
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from rest_framework.permissions import AllowAny
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

from .models import Task
from .serializers import TaskSerializer, UserSerializer, LoginSerializer




class TaskDeleteView(DestroyAPIView):
    serializer_class = TaskSerializer
    lookup_field = 'id'

    def get_queryset(self):
        # Filter tasks by the authenticated user
        return Task.objects.filter(user=self.request.user)
    
    def get_object(self):
        queryset = self.get_queryset()
        obj = queryset.get(id=self.kwargs["id"])
        return obj
        

class TaskDetailView(RetrieveUpdateAPIView):
    serializer_class = TaskSerializer
    lookup_field = 'id'

    def get_queryset(self):
        # Filter tasks by the authenticated user
        return Task.objects.filter(user=self.request.user)
    
    def get_object(self):
        queryset = self.get_queryset()
        obj = queryset.get(id=self.kwargs["id"])
        return obj
    

class AddTaskView(APIView):
    permission_classes = [IsAuthenticated]  # Ensure only authenticated users can add tasks

    def post(self, request):
        serializer = TaskSerializer(data=request.data, context={'request': request})
        print("REQUEST DATA:", request.data)
        print("USER:", request.user)

        if serializer.is_valid():
            print("VALIDATED DATA:", serializer.validated_data)
            cleaned_data = serializer.validated_data

            # Set a default value for 'category' if it's missing or empty
            if not cleaned_data.get('category'):
                cleaned_data['category'] = "Uncategorized"

            # Shift the order of all existing tasks for the logged-in user
            Task.objects.filter(user=request.user).update(order=F('order') + 1)

            # Create the new task with order = 0 and assign it to the logged-in user
            new_task = serializer.save(order=0, user=request.user)
            print("NEW TASK:", new_task)

            return Response(
                TaskSerializer(new_task).data,
                status=rf_status.HTTP_201_CREATED
            )

        return Response(
            {"errors": serializer.errors},
            status=rf_status.HTTP_400_BAD_REQUEST
        )
    

class TaskBoardView(APIView):
    permission_classes = [IsAuthenticated]  # Ensure only authenticated users can access
    print("IS AUTHENTICATED:", permission_classes)

    def get(self, request):
        # Retrieve tasks only for the logged-in user
        tasks = Task.objects.filter(user=request.user).order_by('order')
        grouped = defaultdict(list)

        for task in tasks:
            grouped[task.status].append(TaskSerializer(task).data)

        return Response(grouped)

    def post(self, request):
        # Update tasks only for the logged-in user
        data = request.data

        for status, task_list in data.items():
            for task_data in task_list:
                try:
                    # Ensure the task belongs to the logged-in user
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
            # Ensure Token is created for the user
            token, created = Token.objects.get_or_create(user=user)
            return Response({
                "token": token.key,
                "user_id": user.id  # Include user_id in the response
            }, status=rf_status.HTTP_201_CREATED)
        return Response(serializer.errors, status=rf_status.HTTP_400_BAD_REQUEST)
    

@method_decorator(csrf_exempt, name='dispatch')
class LoginView(APIView):
    permission_classes = [AllowAny] 
    
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        print(request.data)
        if serializer.is_valid():
            user = serializer.validated_data
            # Ensure Token is retrieved or created for the user
            token, created = Token.objects.get_or_create(user=user)
            return Response({"token": token.key})
        return Response(serializer.errors, status=rf_status.HTTP_400_BAD_REQUEST)
