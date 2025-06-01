import requests
import os
from dotenv import load_dotenv
from langchain_huggingface import HuggingFaceEndpoint
from langchain_openai import ChatOpenAI

import time
import threading




load_dotenv()

# Get API key
api_key = os.getenv("HUGGINGFACE_API_KEY")
if not api_key:
    raise ValueError("No Hugging Face API key found. Make sure HUGGINGFACE_API_KEY is set in your .env file")


#repo_id = "bigscience/bloom-560m"
#repo_id = "mistralai/Devstral-Small-2505"

#model = HuggingFaceEndpoint(
   # repo_id="deepseek-ai/DeepSeek-R1-0528",
   #huggingfacehub_api_token=api_key,
    #max_new_tokens=100,
    #temperature=0.9
#)

from huggingface_hub import InferenceClient

client = InferenceClient(
    provider="fireworks-ai",
    api_key="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",
)

# Flag to stop the timer thread
stop_timer = False

# Function to print elapsed time every second
def print_timer():
    counter = 0
    while not stop_timer:
        print(f"⏳ {counter} seconds passed...")
        time.sleep(1)
        counter += 1

# Start timer thread
timer_thread = threading.Thread(target=print_timer)
timer_thread.start()
# Load environment variables
start_time = time.time()

completion = client.chat.completions.create(
    model="deepseek-ai/DeepSeek-R1-0528",
    messages=[
        {
            "role": "user",
            "content": "whats multiverse"
        }
    ],
)

end_time = time.time()
stop_timer = True
timer_thread.join()

print(completion.choices[0].message)
print(f"⏱️ Total time taken: {end_time - start_time:.2f} seconds")



# Use the model
#response = model.invoke("Write a one-sentence bedtime story about a unicorn in a magical forest.")
#print(response)
