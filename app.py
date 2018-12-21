import stripe
import os
from cachetools import cached, TTLCache
from flask import Flask, render_template
app = Flask(__name__)

# Get the Stripe Secret Key from an OS variable
stripe.api_key = os.getenv('STRIPE_KEY')
stripe_public_key = os.getenv('STRIPE_PUBLIC_KEY')

# Create a TTLCache 'cache' to prevent spamming Stripe.
# The cache has a TTL of 30 mins as Products are unlikey to change often.
# Caching is great https://medium.com/the-python-corner/how-to-make-your-code-faster-by-using-a-cache-in-python-fb169fbcbb0b
cache = TTLCache(maxsize=10, ttl=1800)

# Our default route when someone hits our domain name
@app.route("/")
def index():
    return render_template('index.html', plans=get_plans())

# Route used to serve the success splash page when Stripe redirects back
@app.route("/success")
def success():
    return render_template('success.html')

@cached(cache)
def get_plans():
    '''
    We need to get the Product Pricing plans from Stripe
    Get the 'Bean Box' Product and store its Id.

    This function uses the cache to prevent spamming Stripe.

    :return: A list of dictionaries containing the Stripe Plan objects
    '''

    print('Calling Stripe to get Products and Pricing Plans')

    product_id = [
        product['id']
        for product in stripe.Product.list(limit=3)['data']
        if product['name'] == 'Bean Box'
    ][0]

    # Get the plans for the 'Bean Box' Product
    plans = [plan for plan in stripe.Plan.list(product=product_id)]

    return plans

