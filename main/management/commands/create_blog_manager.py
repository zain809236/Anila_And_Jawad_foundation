from django.core.management.base import BaseCommand
from django.contrib.auth.models import User, Group


class Command(BaseCommand):
    help = 'Create a new Blog Manager user'

    def add_arguments(self, parser):
        parser.add_argument('username', type=str, help='Username for the blog manager')
        parser.add_argument('email', type=str, help='Email for the blog manager')
        parser.add_argument('password', type=str, help='Password for the blog manager')
        parser.add_argument('--first-name', type=str, default='', help='First name')
        parser.add_argument('--last-name', type=str, default='', help='Last name')

    def handle(self, *args, **kwargs):
        username = kwargs['username']
        email = kwargs['email']
        password = kwargs['password']
        first_name = kwargs.get('first_name', '')
        last_name = kwargs.get('last_name', '')

        # Check if user already exists
        if User.objects.filter(username=username).exists():
            self.stdout.write(self.style.ERROR(f'User {username} already exists!'))
            return

        # Create user
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name,
            is_staff=True  # Allow access to admin interface
        )

        # Add to Blog Manager group
        try:
            blog_manager_group = Group.objects.get(name='Blog Manager')
            user.groups.add(blog_manager_group)
            self.stdout.write(self.style.SUCCESS(f'Created Blog Manager user: {username}'))
            self.stdout.write(f'Email: {email}')
            self.stdout.write(f'Password: {password}')
            self.stdout.write('\nThis user can:')
            self.stdout.write('  - Access blog management at /blog-management/')
            self.stdout.write('  - Create and edit blog posts')
            self.stdout.write('  - NOT publish or delete posts')
        except Group.DoesNotExist:
            self.stdout.write(self.style.ERROR(
                'Blog Manager group does not exist! Run: python manage.py setup_blog_managers'
            ))
            user.delete()
