import os
from dotenv import load_dotenv

# относительный путь для примера, лучше использовать глобальный!
load_dotenv("./.env")

key = "USERNAME"
username = os.getenv(key, None)
username1 = os.environ.get(key, None)

print(username)
print(username1)
