from dotenv import load_dotenv
import os
import voltage

from utils import unwrap

client = voltage.Client()

load_dotenv()
client.run(unwrap(os.getenv('TOKEN')))
