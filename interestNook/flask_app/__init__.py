from flask import Flask
import os
from dotenv import load_dotenv
load_dotenv('secret.env')
secret_key = os.getenv('secret_key')
print(secret_key)
app = Flask(__name__)
app.secret_key = "secret_key"