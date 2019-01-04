import stripe
from stripe.error import StripeError
import os
import json
from cachetools import cached, TTLCache
from flask import Flask, render_template, request, jsonify
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
    return render_template('index.html', plans=get_plans(), stripe_public_key=stripe_public_key)


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

# Terminal  specific endpoints below

# Get the terminal connection token
@app.route('/terminal_connection_token', methods=['POST'])
def terminal_connection_token():
    token = stripe.terminal.ConnectionToken.create()
    return jsonify(token)

# Use the backend to create a PaymentIntent for processing
@app.route("/buy")
def buy():
    # retrieve the Plan object
    plan = stripe.Plan.retrieve(request.args.get('plan_id'))

    # Create a payment intent using the plan amount and pass it's client secret to the front end
    payment_intent = stripe.PaymentIntent.create(
        amount = plan.amount,
        currency = 'usd', # Hard code currency to USD as terminal not available in Europe yet
        allowed_source_types = ['card_present'],
        capture_method = 'manual'
    )

    return render_template('collect_payment.html', client_secret=payment_intent.client_secret)

# Endpoint for capturing PaymentIntents
@app.route("/capture/<payment_intent_id>")
def capture(payment_intent_id):
    try:
        # Get the PaymentIntent from Stripe
        payment_intent = stripe.PaymentIntent.retrieve(payment_intent_id)
        # Capture the charge
        payment_intent.capture()

        # Return a success message
        resp = jsonify(success=True)
        resp.status_code = 200

        return resp
    except StripeError as se:
        print('Error capturing the Payment intent from Stripe: {}'.format(se._message))
        raise