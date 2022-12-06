# imports
import openai  # OpenAI Python library to make API calls
import requests  # used to download images
import os  # used to access filepaths
from PIL import Image  # used to print and edit image
from datetime import datetime
import time

# set API key
openai.api_key = os.environ.get("OPENAI_API_KEY")

# set image directory
image_dir = os.path.join(os.pardir,'images')

# create the directory if it doesn't yet exist
if not os.path.isdir(image_dir):
    os.mkdir(image_dir)

# print the directory to save to
print(f'''image_dir={image_dir}''')

# User inputs prompt
print('What design would you like to generate? The only limit is your imagination')
prompt=input()

# User chooses number of images
print('How many images would you like to generate? The only limit is the number 5')
num_images = input()

# Choose size of image
size_options = ['256x256'
           , '512x512'
           , '1024x1024']

user_input = ''

input_message = "Pick an option:\n"

for index, item in enumerate(size_options):
    input_message += f'{index+1}) {item}\n'

input_message += 'Your choice: '

while user_input.lower() not in size_options:
    user_input = input(input_message)

print('You picked: ' + user_input)

# call the OpenAI API
generation_response = openai.Image.create(
    prompt=prompt,
    n=int(num_images),
    size="512x512",
    response_format="url",
)

# print response
print(generation_response)

# Iterate through the images and save them to files

# Create a directory for the run
run_dir = os.path.join(image_dir,'image_generation_'+datetime.now().strftime("%m%d%Y_%H%M%S"))

if not os.path.isdir(run_dir):
    os.mkdir(run_dir)

counter = 0
for image in generation_response['data']:
    
    counter += 1

    generated_image_name = f"generated_image_{counter}.png"  # any name you like; the filetype should be .png
    generated_image_filepath = os.path.join(run_dir, generated_image_name)
    generated_image_url = image["url"]  # extract image URL from response
    generated_image = requests.get(generated_image_url).content  # download the image

    with open(generated_image_filepath, "wb") as image_file:
        image_file.write(generated_image)  # write the image to the file

## Order Fulfilment

### Once the customer has settled on their design, we use Printful to create an order and send it

# User chooses which image to have printed
print('Which of these beautiful images would you like to immortalise? The limit is 1')
image_index = int(input())-1

# Pick an example image from above to simulate the customer choosing an option through the front-end
image_url = generation_response['data'][image_index]['url']

# This is not currently used but could be used in future to create a Printful class
#pf_url = 'https://api.printful.com/'

# Get API Key and create headers
pf_key = os.environ.get("PRINTFUL_API_KEY")
pf_headers = {
    'Authorization': f'Bearer {pf_key}'
}

### Get Store Details

response = requests.get(url='https://api.printful.com/stores',headers = pf_headers)
store_id = response.json()['result'][0]['id']
pf_headers.update({'X-PF-Store-Id': str(store_id)})

### Get Product Templates
# TODO: Display the templates so the user can pick which variant to use
template_response = requests.get(url='https://api.printful.com/product-templates',headers = pf_headers)
product_templates = template_response.json()['result']['items']


# Generate dummy data for customer order
customer_order = {
    "recipient": {
        "name": "C Fresh",
        "address1": "6 Boomtown Street",
        "city": "Glasgow",
        "country_code": "GB",
        "zip": "G71 7RY"
    },
    "items": [
        {
            "variant_id": 4015,
            "quantity": 1
        }
    ]
}

# Get placement options
# TOOD: Offer input to choose placement type
variant_response = requests.get(url='https://api.printful.com/products/variant/4015',headers = pf_headers)
[(x['title'],x['type']) for x in variant_response.json()['result']['product']['files']]

placement = {
    'files': [ {
        "type": "front",
        "url": image_url
            }
    ]
}    
customer_order['items'][0].update(placement)
print(customer_order)

# Create new headers object with content-type in it
post_headers = {
    "Content-Type": "application/json",
    'Authorization': f'Bearer {pf_key}',
    'X-PF-Store-Id': str(store_id)
}
post_response = requests.post(url='https://api.printful.com/orders',headers = post_headers,json=customer_order)

if post_response.status_code == 200:
    print(f'''Order created successfully. ID is {post_response.json()['result']['id']}''')
    
else:
    print(f'Sad times, order failed with code {post_response.status_code}')