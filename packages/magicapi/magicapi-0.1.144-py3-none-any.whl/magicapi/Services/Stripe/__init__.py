import stripe
from magicapi import g

stripe.api_key = g.settings.stripe_secret_key
