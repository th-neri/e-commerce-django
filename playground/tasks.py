from time import sleep
from celery import shared_task

# defining a task using celery
@shared_task
def notify_customers(message):
    print('Sending 10K emails...')
    print(message)
    sleep(10)
    print('Emails were successfully sent!')