from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from .models import Task
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token


class UserTests(APITestCase):
    def test_register_user(self):
        url = reverse('register')
        data = {
            "username": "testuser",
            "password": "testpassword123",
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn("token", response.data)

    def test_login_user(self):
        user = User.objects.create_user(username="testuser", password="testpassword123")
        url = reverse('login')
        data = {
            "username": "testuser",
            "password": "testpassword123",
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("token", response.data)


class TaskTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="testpassword123")
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')

    def test_create_task(self):
        url = reverse('add-new-task')
        data = {
            "name": "Test Task",
            "status": "Pending",
            "category": "Work",
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Task.objects.count(), 1)
        self.assertEqual(Task.objects.first().name, "Test Task")

    def test_get_tasks(self):
        Task.objects.create(name="Test Task", status="to do", user=self.user)
        url = reverse('tasks-page')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["name"], "Test Task")

    def test_update_task(self):
        task = Task.objects.create(name="Test Task", status="to do", user=self.user)
        url = reverse('task-detail', args=[task.id])
        data = {
            "name": "Updated Task",
            "status": "done",
        }
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        task.refresh_from_db()
        self.assertEqual(task.name, "Updated Task")
        self.assertEqual(task.status, "done")

    def test_delete_task(self):
        task = Task.objects.create(name="Test Task", status="to do", user=self.user)
        url = reverse('task-delete', args=[task.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Task.objects.count(), 0)
