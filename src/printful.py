import requests 
import os

pf_url = 'https://api.printful.com/'

# Get API Key and create headers
pf_key = os.environ.get("PRINTFUL_API_KEY")

def get_authorization_token(pf_key):
    
    pf_authorization = {
        'Authorization': f'Bearer {pf_key}'
    }
    return pf_authorization 

def get_store_id(pf_key):
    response = requests.get(url='https://api.printful.com/stores',headers = get_authorization_token(pf_key))
    store_id = response.json()['result'][0]['id']
    # TODO: Hardcoded to get your store, need to change to select which one
    return str(store_id)

def get_pf_headers(pf_key):
    pf_headers = get_authorization_token(pf_key)
    pf_headers.update({'X-PF-Store-Id': get_store_id(pf_key)})
    return pf_headers

def get_product_templates(pf_key):
    #print(get_pf_headers(pf_key))
    template_response = requests.get(url='https://api.printful.com/product-templates',headers = get_pf_headers(pf_key))
    product_templates = template_response.json()['result']['items']
    return product_templates 

def get_variants(pf_key,variant_id):
    variant_response = requests.post(url=f'https://api.printful.com/products/variant/{variant_id}'
                                    ,headers = get_pf_headers(pf_key))
    return variant_response

# TODO: This function doesn't work and needs to be fixed
def get_mockups(pf_key,product_id):
    mockup_response = requests.post(f'https://api.printful.com/mockup-generator/create-task/{product_id}'
                                    ,headers = get_pf_headers(pf_key))
    task_key = mockup_response.json()['result']['task_key']

    mockup_result = None
    while mockup_result is None:
        try:
            # connect
            mockup_result = requests.get(f'https://api.printful.com/mockup-generator/task?task_key={task_key}'
                                        ,headers=get_pf_headers(pf_key))
        except:
            pass
    return mockup_result

def get_post_headers(pf_key):
    post_headers = {
    "Content-Type": "application/json",
    'Authorization': f'Bearer {pf_key}',
    'X-PF-Store-Id': get_store_id(pf_key)
    }
    return post_headers

# TODO: Add mockup generation into prototype so they can see the mocked up shirt


if __name__ == "__main__":

    variant_list = []
    for template in get_product_templates(pf_key):
        print(template)
        variants = template['available_variant_ids'][0]

        for variant in variants[:2]:
            print(f'Getting variant {variant}')
            variant_list.append(get_variants(pf_key,variant_id=variant).json()['result']['variant'])


    variant_list_trimmed = variant_list[:3]

    image_urls = [(x['id'],x['image']) for x in variant_list_trimmed]

    print(image_urls)

    '''
    products = set()
    [products.add(x['product_id']) for x in variant_list_trimmed]

    mockups = []
    for product in list(products):
        print(product)
        mockup_response = get_mockups(pf_key,product)
        print(mockup_response.json())
        task_key = mockup_response.json()['result']['task_key']

        mockup_result = None
        while mockup_result is None:
            try:
                # connect
                mockup_result = requests.get(f'https://api.printful.com/mockup-generator/task?task_key={task_key}'
                                            ,headers=get_pf_headers(pf_key))
            except:
                pass
        
        mockups.append(mockup_result.json())

    for m in mockups:
        print(m)


'''