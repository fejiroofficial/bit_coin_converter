import graphene

import price_calculator.schema


class Query(price_calculator.schema.Query, graphene.ObjectType):
    pass


schema = graphene.Schema(query=Query)