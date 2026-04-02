# Vercel Serverless Function Giriş Noktası
import sys
import os

# root dizini path'e ekliyoruz ki backend/app import edilebilsin
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "backend"))

from app.main import app
