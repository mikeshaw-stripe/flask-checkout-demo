from flask_frozen import Freezer
from app import app
import stripe
import os

stripe.api_key = os.getenv('STRIPE_KEY')
freezer = Freezer(app)

if __name__ == '__main__':

    # This will Generate a static site in a build folder in the project dir.

    freezer.freeze()

    # Because app.py has a route "/success" flask_frozen creates
    # a 'success' file instead of 'success.html'. Need to fix this
    # as flask_frozen doesn't have a fix

    # https://github.com/Frozen-Flask/Frozen-Flask/issues/41

    os.rename(
        os.path.join(os.getcwd(), 'build', 'success'),
        os.path.join(os.getcwd(), 'build', 'success.html')
    )

    print("Flask App Successfully Frozen")
