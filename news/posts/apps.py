from django.apps import AppConfig


class PostsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'posts'

    # def ready(self):
    #     print('Ready....')
    #     from .posts_scheduler import posts_updater
    #     posts_updater.start()
    def ready(self):
        import posts.signals