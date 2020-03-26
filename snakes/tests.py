from django.test import TestCase
from django.contrib.auth.models import User

from .models import Snake


class SnakeTests(TestCase):

    @classmethod
    def setUpTestData(cls):
        # Create a user
        testuser1 = User.objects.create_user(
            username='testuser1', password='abc123'
        )
        testuser1.save()

    
        # Create a snake
        test_snake = Snake.objects.create(
            owner=testuser1, name='Test Snake', description='test snake description'
        )

    
    def test_snake_content(self):
        snake = Snake.objects.get(id=1)
        owner = f'{snake.owner}'
        name = f'{snake.name}'
        description = f'{snake.description}'
        self.assertEqual(owner, 'testuser1')
        self.assertEqual(name, 'Test Snake')
        self.assertEqual(description, 'test snake description')
