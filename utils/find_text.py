def getPrice(response):
    text = response
    result = text.find("270.000")
    return text[result:result + 7]
