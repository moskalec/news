from apscheduler.schedulers.background import BackgroundScheduler

from posts.models import UserPostRelation


def update_posts():
    print('....deleted...!!!!')
    UserPostRelation.objects.all().delete()


def start():
    scheduler = BackgroundScheduler()
    scheduler.add_job(update_posts, 'interval', hours=24)
    print('..working...')
    scheduler.start()
