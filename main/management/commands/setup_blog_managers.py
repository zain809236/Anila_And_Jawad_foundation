from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from main.models import BlogPost


class Command(BaseCommand):
    help = 'Set up Blog Manager group with limited permissions'

    def handle(self, *args, **kwargs):
        # Create or get Blog Manager group
        blog_manager_group, created = Group.objects.get_or_create(name='Blog Manager')

        if created:
            self.stdout.write(self.style.SUCCESS('Created Blog Manager group'))
        else:
            self.stdout.write(self.style.WARNING('Blog Manager group already exists'))

        # Get BlogPost content type
        content_type = ContentType.objects.get_for_model(BlogPost)

        # Define permissions for Blog Manager
        # They can add, change, and view blog posts but NOT delete or publish
        permissions = Permission.objects.filter(
            content_type=content_type,
            codename__in=['add_blogpost', 'change_blogpost', 'view_blogpost']
        )

        # Clear existing permissions and set new ones
        blog_manager_group.permissions.clear()
        blog_manager_group.permissions.set(permissions)

        self.stdout.write(self.style.SUCCESS(
            f'Assigned {permissions.count()} permissions to Blog Manager group:'
        ))
        for perm in permissions:
            self.stdout.write(f'  - {perm.name}')

        self.stdout.write(self.style.SUCCESS('\nBlog Manager group setup complete!'))
        self.stdout.write('\nTo create a Blog Manager user, run:')
        self.stdout.write('  python manage.py create_blog_manager <username> <email> <password>')
