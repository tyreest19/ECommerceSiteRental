import os
import stripe
from app import create_app
from app import stripe_keys

stripe.api_key = stripe_keys['secret_key']

config_name = os.getenv('FLASK_CONFIG')
app = create_app(config_name)

if __name__ == '__main__':
    app.run()