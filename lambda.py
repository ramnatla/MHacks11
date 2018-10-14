import json
import requests

# Product data type definition
class product:
  def __init__(self, name, price):
    self.name = name
    self.price = price

# Gets name and price for top three products
def getTopProducts(API_KEY, base_URI, headers):
   x = requests.get(base_URI + '/public/v1/browse?limit=3', headers = headers)
   data = json.loads(x.content)
   
   product1 = product(data["Products"][0]["title"], "$" + str(data["Products"][0]["market"]["lowestAsk"]))
   product2 = product(data["Products"][1]["title"], "$" + str(data["Products"][1]["market"]["lowestAsk"]))
   product3 = product(data["Products"][2]["title"], "$" + str(data["Products"][2]["market"]["lowestAsk"]))
   
   output = product1.name + " " + product1.price + " "
   output += product2.name + " " + product2.price + " "
   output += product3.name + " " + product3.price
   
   return output
   
# Gets name and price for top three products of the query search
def getProductsByQuery(API_KEY, base_URI, headers, query):
   x = requests.get(base_URI + '/stage/v2/search?query=' + query, headers = headers)
   data = json.loads(x.content)
   
   product1 = product(data["hits"][0]["name"], "$" + str(data["hits"][0]["lowest_ask"]))
   product2 = product(data["hits"][1]["name"], "$" + str(data["hits"][1]["lowest_ask"]))
   product3 = product(data["hits"][2]["name"], "$" + str(data["hits"][2]["lowest_ask"]))
   
   output = product1.name + " " + product1.price + " "
   output += product2.name + " " + product2.price + " "
   output += product3.name + " " + product3.price
   
   return output
   
def lambda_handler(event, context):
   
   API_KEY = "B1sR9t386d6UVO6aI7KRf91gLaUywqEK1TLBGsXv"
   base_URI = 'https://gateway.stockx.com'
   headers = {'x-api-key':API_KEY}
   
   x = requests.get(base_URI + '/v1/browse?limit=3', headers = headers)
   # x = requests.get(base_URI + '/v1/browse?limit=1', headers = headers)
   #return getTopProducts(API_KEY, base_URI, headers)
   
   return getProductsByQuery(API_KEY, base_URI, headers, "nike")
   
   return json.loads(x.content)["Products"][0]["category"]
   
   return {
       "statusCode": 200,
       "body": json.dumps('Hello from Lambda!')
   }