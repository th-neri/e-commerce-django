from django.shortcuts import render
from .tasks import notify_customers

# Create your views here.
def say_hello(request):
    notify_customers.delay('Hello')
    return render(request, 'hello.html', {'name': 'Neri'})

    # to send a email with something attacked like a pic or something then it's better to use EmailMessage
    # try:
    #     message = EmailMessage('subject', 'message', 'from@neri.com', ['to@neri.com'])
    #     message.attach_file('playground/static/images/<image>')
    #     message.send()

    # like the EmailMessage but with this i can store email messages in template files using django-templated-mail
    #  try:
    #     message = BaseEmailMessage(
    #         template_name='emails/hello.html',
    #         context={'name': 'Neri'}
    #     )
    #     message.send(['to@neri.com'])
    #    except BadHeaderError:
    #       pass
