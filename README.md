# DALL-E Print

The purpose of this project is to build a basic ecommerce platform that enables users to receive user prompts, generate images based on those prompts, and then create physical products with the results.

To run the demo you need to have a Printful account (details below), and I'd suggest logging in in another tab prior to the demo.

**Prequisites:**
- Python 3.X (I used 3.7.7 to set this up)
- A Printful account (which you can find here: https://www.printful.com/)
- Printful API Token accessible from the Developer Portal: https://developers.printful.com/docs/

**Environment Variables**
This application requires you to have set the below variables in your OS:
- OPENAI_API_KEY
- PRINTFUL_API_KEY

**Instructions**
- Install the requirements.txt file using `pip install -r requirements.txt`
- Navigate to src/
- Run `streamlit run dalle_print.py`

**Other Demos**
Depending on your audience you may want to use one of the other formats for this demo, which I created when doing initial discovery
- Dall-E Print.ipynb: Notebook containing most of the code that informed the functions and some experiments such as using the Dall-E Variations endpoint than didn't make it into the final version
- main.py: Command-line version of the demo