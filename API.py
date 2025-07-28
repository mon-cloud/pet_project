import os  
from dotenv import load_dotenv
# Load các biến từ .env
load_dotenv()
# Lấy giá trị biến
key = os.getenv("abc")
print(key)