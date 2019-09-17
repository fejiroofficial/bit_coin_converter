import graphene
import requests
import json
from graphql import GraphQLError
from graphene_django import DjangoObjectType
from collections import namedtuple


class CalculatePriceType(graphene.ObjectType):
    price = graphene.String()


class Query(graphene.AbstractType):
    calculate_price = graphene.Field(CalculatePriceType,
                                    transaction_type=graphene.String(required=True),
                                    margin=graphene.Float(required=True),
                                    exchange_rate=graphene.Float(required=True))

    def resolve_calculate_price(self, info, **kwargs):
        """
        Computes conversion rate

        Returns:
            tuple(price)
        """
        transaction_type = kwargs.get('transaction_type').lower()
        margin = kwargs.get('margin')
        exchange_rate = kwargs.get('exchange_rate')

        url = "https://api.coindesk.com/v1/bpi/currentprice.json"
        response = requests.get(url)
        data = response.text
        parsed = json.loads(data)
        rate = parsed["bpi"]["USD"]["rate_float"]

        margin_computed_value = margin/100 * rate

        if transaction_type == 'sell':
            rate = rate - margin_computed_value
        elif transaction_type == 'buy':
            rate = rate + margin_computed_value
        else:
            raise GraphQLError('This type of transaction must either be a buy or a sell')

        rate = rate * exchange_rate
        ValueObject = namedtuple('Product', 'price')
        return ValueObject(price=rate)
