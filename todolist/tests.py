from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from .models import Task, SubTask


class TodoListViewTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user('test@user.name')
        self.user_another = User.objects.create_user('test@user_another.name')
        self.task_list = [
            Task.objects.create(name='Task {}'.format(i), owner=self.user) for i in range(1, 11)]
        self.sub_task_list = [SubTask.objects.create(
            name='Sub task {}'.format(i), owner=self.user, task=self.task_list[0], status=False) for i in range(1, 4)]
        self.client.force_login(self.user)

    def tearDown(self):
        self.user.delete()
        self.user_another.delete()

    def test_task_list(self):
        url = reverse('task-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK, msg=response.json())

        self.client.force_login(self.user_another)
        response = self.client.get(url)
        response_json = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK, msg=response_json)
        self.assertEqual(response_json, [])

    def test_task_detail(self):
        url = reverse('task-detail', args=[self.task_list[0].id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK, msg=response.json())

        self.client.force_login(self.user_another)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN, msg=response.json())

    def test_task_delete(self):
        url = reverse('task-detail', args=[self.task_list[0].id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        self.client.force_login(self.user_another)
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND, msg=response.json())

    def test_task_update(self):
        data = {
            'name': 'New task name'
        }
        url = reverse('task-detail', args=[self.task_list[0].id])
        response = self.client.put(url, data)
        response_json = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK, msg=response_json)
        self.assertEqual(response_json['name'], data['name'])

        self.client.force_login(self.user_another)
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN, msg=response.json())

    def test_task_create(self):
        data = {
            'name': 'New task list'
        }
        url = reverse('task-list')
        response = self.client.post(url, data)
        response_json = response.json()
        self.assertEqual(response.status_code, status.HTTP_201_CREATED, msg=response_json)
        self.assertEqual(response_json['name'], data['name'])

        self.client.logout()
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED, msg=response.json())

    def test_sub_task_create(self):
        data = {
            'name': 'Sub task 1',
            'task': {'id': self.task_list[0].id}
        }
        url = reverse('subtask-create')
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED, msg=response.json())

        self.client.force_login(self.user_another)
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN, msg=response.json())

        self.client.logout()
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED, msg=response.json())

    def test_sub_task_update(self):
        data = {
            'name': 'New name sub task',
            'status': True
        }
        url = reverse('subtask-detail', args=[self.sub_task_list[0].id])
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK, msg=response.json())

        self.client.force_login(self.user_another)
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN, msg=response.json())

    def test_sub_task_delete(self):
        url = reverse('subtask-detail', args=[self.sub_task_list[0].id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        self.client.force_login(self.user_another)
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND, msg=response.json())
