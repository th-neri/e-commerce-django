from locust import HttpUser, task, between
from random import randint

class WebsiteUser(HttpUser):
    wait_time = between(1, 5) # so locust randomly wait 1 to 5 seconds between each task

    @task(2) # the number is to give weight/priority to the task. greater numbers means more priority
    def view_products(self):
        collection_id = randint(1, 11)
        self.client.get(f'/store/products/?collection_id={collection_id}', 
                        name='/store/products') # to send a request to the endpoint

    # to view a specific product
    @task(4)
    def view_product(self):
        product_id = randint(3, 100)
        self.client.get(f'/store/products/{product_id}',
                        name='/store/products/:id')

    # to add a product to the cart
    @task(1)
    def add_to_cart(self):
        product_id = randint(3, 10)
        self.client.post(f'/store/carts/{self.cart_id}/items/',
                         name='/store/carts/items',
                         json={'product_id': product_id, 'quantity': 1}) # to send data to the server set json to a dictionary

    # this method gets called to generate a cart ID everytime the user starts browsing the website
    def on_start(self):
        response = self.client.post('/store/carts/') # to send a post request to this endpoint
        result = response.json() # to get the JSON object in the response
        self.cart_id = result['id']

    @task
    def say_hello(self):
        self.client.get('/playground/hello/')

