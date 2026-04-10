from django.apps import AppConfig

class HrConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'hr'

    def ready(self):
        import os

        # Prevent running twice
        if os.environ.get('RUN_MAIN') != 'true':
            return

        from django.core.management import call_command

        # Run migrations
        try:
            call_command('migrate')
        except Exception as e:
            print("Migration error:", e)

        # Create superuser
        from django.contrib.auth import get_user_model
        User = get_user_model()

        if not User.objects.filter(username='admin').exists():
            User.objects.create_superuser(
                username='admin',
                email='admin@example.com',
                password='admin123'
            )
