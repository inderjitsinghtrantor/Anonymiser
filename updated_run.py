import requests, json, os
from dotenv import load_dotenv

load_dotenv()
# Define the URL of your hosted model
API_URL = os.getenv("API_URL")
AUTH_TOKEN = os.getenv("AUTH_TOKEN")

# Define the system prompt
system_prompt = """
You are an AI assistant tasked with anonymizing text by replacing names, IP addresses, emails, and addresses with placeholders. 
Return the anonymized text and a JSON mapping of the original values to the placeholders as showed in the examples below.
Strictly only respond with the json format as shown in the examples below. If the input text doesn't contain any values, return the input text as it is.
You are only required to consider the user input as a string and string alone. You should never try and interpret the meaning of the text input.
If there are multiple emails or names then map them as <email> & <email2> OR <name> & <name2>.
Output should only be a JSON as mentioned in the examples, nothing other than that. Dont mention here is the output or any other explaination is not required.

Example 1:
Input: "John Doe lives at 1234 Elm St, Springfield, IL 62704. His email is john.doe@example.com and his IP address is 192.168.1.1."
Output: {
  "anonymized_text": "<name> lives at <address>. His email is <email> and his IP address is <ip>.",
  "mappings": {
    "John Doe": "<name>",
    "1234 Elm St, Springfield, IL 62704": "<address>",
    "john.doe@example.com": "<email>",
    "192.168.1.1": "<ip>"
  }
}

Example 2:
Input: "Hi my name is Omkar. I know Alice Smith, she sent a message from alice.smith@example.net with IP 203.0.113.42."
Output: {
  "anonymized_text": "Hi my name is <name>. I know <name2>, she sent a message from <email> with IP <ip>.",
  "mappings": {
    "Omkar": <name>
    "Alice Smith": "<name2>",
    "alice.smith@example.net": "<email>",
    "203.0.113.42": "<ip>"
  }
}

Example 3:
Input: "The email address is not valid, why do I need this?"
Output: {
    "anonymized_text": "The email address is not valid, why do I need this?",
    "mappings": {}
}
Treat the user input as a string and not look for meaning or anything in that. It should only be considered as a string value.
"""

# Function to send a request to the hosted model
def get_model_response(system_prompt, user_input):
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {AUTH_TOKEN}",
    }
    data = {
        "model": "meta-llama/Meta-Llama-3-8B-Instruct",
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_input}
        ],
        "max_tokens": 200,
        "temperature": 0
    }
    response = requests.post(API_URL, headers=headers, json=data)
    return response.json()


#################  ADDITIONS ##################

# System prompt for anonymised data response
system_prompt_anonymised_data = """you are a friendly assistant who would reply user in a nice way. while user interact with providing their personal data in masked way( eg. <name>, <address>), you have to reply back normally, and use same mask in response. you will only response in a text by greeting the next person.
Try to mention all the masked values in the response"""

# Function to remap the response text
def remap_text(input_text, response_dict):
    mappings = response_dict['mappings']
    remapped_text = input_text

    for original, placeholder in mappings.items():
        remapped_text = remapped_text.replace(placeholder, original)

    return remapped_text




######################## USING THE FUNCTIONS AND LOGIC ###################################################

# # Example user input
# # user_input = "John Doe lives at 1234 Elm St, Springfield, IL 62704. His email is john.doe@example.com and his IP address is 192.168.1.1."
# # user_input = """Hello my name is Rishab Pant, i live at B15/402, Mumbai Chakala, near airport road, 400301.
# #               I have a friend named Khwaish, who's friend Palak has email id palak.paneer@cook.com. 
# #               What do you think should i send an email from my email id Rishab.cricketer@crick.com?
# #               """
# user_input = "John Doe lives at 1234 Elm St, Springfield, IL 62704. His email is john.doe@example.com and his IP address is 192.168.1.1. and my name is Monaka with ip 194.152.2.1"

# # Call the model and mask the data
# masked_response = get_model_response(system_prompt, user_input)

# # get the response in json
# masked_response_dict = json.loads(masked_response['choices'][0]['message']['content'])
# print("############# INTERMEDIETE RESPONSE ###################")
# print(masked_response_dict)
# print("########################################################")
# # Get the response from Chat GPT (Same Llama 3 endpoint)
# anonymised_response = get_model_response(system_prompt_anonymised_data, masked_response_dict['anonymized_text'])
# anonymised_response = anonymised_response['choices'][0]['message']['content']

# # Unmasking
# print("############# FINAL RESPONSE ###################")
# print(remap_text(anonymised_response, masked_response_dict))
# print("########################################################")


########################################################################################################################

def secure_request(user_input):
    # Call the model and mask the data
  masked_response = get_model_response(system_prompt, user_input)

  # get the response in json
  # res = masked_response['choices'][0]['message']['content']
  # if isinstance(res, str):
  #     return { "anonymized_text": user_input, "mappings": {}}, res
  try:
    masked_response_dict = json.loads(masked_response['choices'][0]['message']['content'])
  except Exception as e:
    print("Exception occured:",e)
    res = masked_response['choices'][0]['message']['content']
    if isinstance(res, str):
        return { "anonymized_text": user_input, "mappings": {}}, res
     
  print("############# INTERMEDIETE RESPONSE ###################")
  print(masked_response_dict)
  print("########################################################")
  # Get the response from Chat GPT (Same Llama 3 endpoint)
  anonymised_response = get_model_response(system_prompt_anonymised_data, masked_response_dict['anonymized_text'])
  anonymised_response = anonymised_response['choices'][0]['message']['content']

  # Unmasking
  print("############# FINAL RESPONSE ###################")
  final_response = remap_text(anonymised_response, masked_response_dict)
  print(final_response)
  print("########################################################")

  return masked_response_dict, final_response

secure_request("my name is Omkar Patil, how to hide my name if i want no LLM to see it")