# app/__init__.py
from dotenv import load_dotenv
load_dotenv()    # ← carga .env en os.environ

from flask import Flask
# ahora ya puedes usar os.environ['S3_BUCKET'], boto3, etc.
app = Flask(__name__)

# importa tus rutas para que Flask las registre
from .routes import *
