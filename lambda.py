import json
import requests

# Product data type definition
class product:
  def __init__(self, name, price):
    self.name = name
    self.price = price

# Gets name and price for top three products
def getTopProducts(API_KEY, base_URI, headers, price, priceChoice):
   x = requests.get(base_URI + '/public/v1/browse?limit=3', headers = headers)
   data = json.loads(x.content)
   
   product1 = product(data["Products"][0]["title"], "$" + str(data["Products"][0]["market"]["lowestAsk"]))
   product2 = product(data["Products"][1]["title"], "$" + str(data["Products"][1]["market"]["lowestAsk"]))
   product3 = product(data["Products"][2]["title"], "$" + str(data["Products"][2]["market"]["lowestAsk"]))
   productArray = [product1, product2, product3]
   
   if (price == "true"):
       return "The lowest asking price of the " + productArray[int(priceChoice)].name + " is " + productArray[int(priceChoice)].price
   
   return "The " + product1.name + ", the " + product2.name + ", and the " + product3.name
   
# Gets name and price for top three products of the query search
def getProductsByQuery(API_KEY, base_URI, headers, query, price, priceChoice):
   x = requests.get(base_URI + '/stage/v2/search?query=' + query, headers = headers)
   data = json.loads(x.content)
   
   product1 = product(data["hits"][0]["name"], "$" + str(data["hits"][0]["lowest_ask"]))
   product2 = product(data["hits"][1]["name"], "$" + str(data["hits"][1]["lowest_ask"]))
   product3 = product(data["hits"][2]["name"], "$" + str(data["hits"][2]["lowest_ask"]))
   productArray = [product1, product2, product3]
   
   if (price == "true"):
       return "The lowest asking price of the " + productArray[int(priceChoice)].name + " is " + productArray[int(priceChoice)].price
   
   return "the " + product1.name + ", the " + product2.name + ", and the " + product3.name + ". "

# Gives a recommendation on what product to buy based on user query and maximum price willing to pay
def searchRecommendation(API_KEY, base_URI, headers, query, threshold):
    x = requests.get(base_URI + '/stage/v2/search?query=' + query, headers = headers)
    data = json.loads(x.content)
    
    nextLowest = 500
    for shoe in data["hits"]:
       if (shoe["lowest_ask"] > 0 and shoe["lowest_ask"] < int(threshold)):
           uuid = shoe["objectID"]
           y = requests.get(base_URI + '/public/v1/products/' + uuid + '?includes=market', headers = headers)
           newData = json.loads(y.content)
           
           title = newData["Product"]["title"]
           condition = newData["Product"]["condition"]
           year = newData["Product"]["year"]
           price = shoe["lowest_ask"]
           
           return "We recommend buying a pair of " + condition + " " + title + " made in " + year + " for a price of $" + str(price)
           
       elif (shoe["lowest_ask"] > 0 and shoe["lowest_ask"] < nextLowest):
            nextLowest = shoe["lowest_ask"]
            
    return "Sorry, I couldn't find a product that met your threshold. The lowest selling point for this product is $" + str(nextLowest)
           

# Lambda Function
def lambda_handler(event, context):
   API_KEY = "B1sR9t386d6UVO6aI7KRf91gLaUywqEK1TLBGsXv"
   base_URI = 'https://gateway.stockx.com'
   headers = {'x-api-key':API_KEY}
   
   if (event["request"]["type"] == "LaunchRequest"):
      output = "Welcome to Hexagon's Stock X API program. You can search for products on the Stock X Wesbite, get prices from top results from your favorite brands, and get personalized recommendations!"
      
   elif (event["request"]["intent"]["name"] == "TopResults"):
      output = getTopProducts(API_KEY, base_URI, headers, "false", "") + " are currently trending on Stock X. "
      output += " If you'd like to hear the price for one of these products, please say first choice, second choice, or third choice"
      
   elif (event["request"]["intent"]["name"] == "SearchQuery"):
      query = event["request"]["intent"]["slots"]["query"]["resolutions"]["resolutionsPerAuthority"][0]["values"][0]["value"]["id"]
      output = "Your search for " + query + " returned " + getProductsByQuery(API_KEY, base_URI, headers, query, "false", "")
      output += "If you'd like to hear the price for one of these products, please say first choice, second choice, or third choice, along with the specified brand"
      
   elif (event["request"]["intent"]["name"] == "UserResponseWithPrice"):
       choice = event["request"]["intent"]["slots"]["num"]["resolutions"]["resolutionsPerAuthority"][0]["values"][0]["value"]["id"]
       output = getTopProducts(API_KEY, base_URI, headers, "true", choice)
       
   elif (event["request"]["intent"]["name"] == "PersonalRec"):
       query = event["request"]["intent"]["slots"]["query"]["resolutions"]["resolutionsPerAuthority"][0]["values"][0]["value"]["id"]
       threshold = event["request"]["intent"]["slots"]["threshold"]["resolutions"]["resolutionsPerAuthority"][0]["values"][0]["value"]["id"]
       output = searchRecommendation(API_KEY, base_URI, headers, query, threshold)
       
   elif (event["request"]["intent"]["name"] == "SearchQueryPrice"):
       query = event["request"]["intent"]["slots"]["query"]["resolutions"]["resolutionsPerAuthority"][0]["values"][0]["value"]["id"]
       choice = event["request"]["intent"]["slots"]["num"]["resolutions"]["resolutionsPerAuthority"][0]["values"][0]["value"]["id"]
       output = getProductsByQuery(API_KEY, base_URI, headers, query, "true", choice)
       
   elif (event["request"]["intent"]["name"] == "EndSession"):
       return {
    "version": "1.0",
    "sessionAttributes": {
    },
    "response": {
        "outputSpeech": {
        "type": "PlainText",
        "text": "Hope you had a great time using Hexagon's StockX API program for MHacks 2018!"
        },
        "shouldEndSession": "true"
        }
    }
    
   else:
      output = "I don't understand what that means, please try again"
   
   return {
    "version": "1.0",
    "sessionAttributes": {
    },
    "response": {
        "outputSpeech": {
        "type": "PlainText",
        "text": output
        },
        "shouldEndSession": "false"
    }
    }