import stripe
from stripe.error import StripeError
import os

# Set the Stripe API Key
stripe.api_key = os.getenv('STRIPE_KEY')

def add_products_and_plans():
    '''
    A function that will add the products and plans to the
    Stripe account specified by the Stripe API Key
    '''

    # Attempt to add the Bean box Product
    try:
        product = stripe.Product.create(
            name='Bean Box',
            type='service',
            statement_descriptor='Bean Box Subscription',
            unit_label='Box'
        )

        print('Added Product {product} to Stripe'.format(product=product.name))

    except StripeError as se:
        print('Call to Stripe to setup a Product encountered an error.')
        raise

    # Attempt to add the Bean Box Plans
    try:
        plans = [
            {
                'name': 'Bean Box Bronze',
                'amount': 1000,
                'description': 'Enough Coffee for one person for 2 weeks. Includes 1 bag of beans.',
                'type': 'bronze'
            },
            {
                'name': 'Bean Box Silver',
                'amount': 1500,
                'description': 'Enough Coffee for two people for 2 weeks. Includes 2 bag of beans.',
                'type': 'silver'
            },
            {
                'name': 'Bean Box Gold',
                'amount': 2000,
                'description': 'Enough Coffee for four people for 2 weeks. Includes 4 bag of beans.',
                'type': 'gold'
            }
        ]

        for plan in plans:
            created_plan = stripe.Plan.create(
                product=product.id,
                nickname=plan['name'],
                amount=plan['amount'],
                currency='eur',
                interval='week',
                interval_count=2,
                metadata={
                    "description": plan['description'],
                    "type": plan['type']
                }
            )

            print('Added Plan {plan_name} for Product {product_name} to Stripe'.format(plan_name=created_plan.nickname, product_name=product.name))

    except StripeError as se:
        print(
            'Call to Stripe to create plans for Product {product_id} encountered an error'.format(
                product_id=product.id
            ))
        raise


if __name__ == '__main__':
    # Add the Products and plans to Stripe
    add_products_and_plans()

