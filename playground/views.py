from django.core.cache import cache # this has API for accessing the cache
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.shortcuts import render
from rest_framework.views import APIView
import requests
import logging

logger = logging.getLogger(__name__) # playground.views

class HelloView(APIView):
    # @method_decorator(cache_page(5 * 60)) # use method decorator for classes and cache decorator for functions
    def get(self, request):
        try: 
            logger.info('Calling httpbin')
            response = requests.get('https://httpbin.org/delay/2')
            logger.info('Received the response')
            data = response.json()
        except requests.ConnectionError:
            logger.critical('httpbin is offline')
        return render(request, 'hello.html', {'name': 'Mosh'})
