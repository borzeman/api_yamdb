import datetime
import random
import jwt # import jwt library
import os
from dotenv import load_dotenv

load_dotenv()
token = os.getenv('SECRET_KEY')
print(token)
print(type(token))

SECRET_KEY = "python_jwt"
# json data to encode
json_data = {
    "sender": "CodeFires JWT",
    "message": "JWT is awesome.  You should try it!",
    "date": str(datetime.datetime.now().day/7)
}
# encode the data with SECRET_KEY and 
# algorithm "HS256" -> Symmetric Algorithm
encode_data = jwt.encode(payload=json_data, \
                        key=SECRET_KEY, algorithm="HS256")
print(type(encode_data)) # print the encoded token
print(str(datetime.datetime.now().day))
print(str(datetime.datetime.min.day))
print(random.randint(1000000, 99999999))
