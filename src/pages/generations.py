import streamlit as st
import openai
import os


# set API key
openai.api_key = os.environ.get("OPENAI_API_KEY")
# Get API Key and create headers
pf_key = os.environ.get("PRINTFUL_API_KEY")
# Set fake customer details for later
# TODO: Add screen for them to input these

st.title('Choose your image')


st.subheader('There can be only one')

st.text("")
images = sorted(os.listdir('images'))

if len(images) == 0:
    st.write("No images generated, please start again")

else:
    col1,col2,col3 = st.columns(3)

    col1.image(os.path.join(os.curdir,'images',images[0]))
    col2.image(os.path.join(os.curdir,'images',images[1]))
    col3.image(os.path.join(os.curdir,'images',images[2]))

    selected_image = st.radio('Select the option you choose',[f'Option {images.index(x) + 1}' for x in images ],index=1)

    st.write(f'You selected {selected_image}. Click submit to generate clothing')

    if st.button('Submit', key='selectionSubmit'):
        with open(os.path.join(os.curdir,'selection.txt'),'w') as file:
                file.write(selected_image[-1])

        st.write('Selection saved. Choose your clothing and submit your order!')

    else:
        st.write('Click above to submit your design')