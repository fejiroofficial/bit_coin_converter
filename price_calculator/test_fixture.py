convert = '''
query{{
  calculatePrice(transactionType:"{type}" margin: 0.2 exchangeRate: 360.00){{
    price
  }}
}}
'''