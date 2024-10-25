# Import python packages
import streamlit as st
#from snowflake.snowpark.context import get_active_session
#Snowpark COLUMN 
from snowflake.snowpark.functions import col
import requests

# Write directly to the app
st.title("Customize Your Smoothie :cup_with_straw:")



st.write(
    """
    Choose fruits you want in your custom Smoothie!
    """
)

#Get Name and Display
name_on_order = st.text_input('Name of Smoothie:')
st.write('The name of the Smoothie will be: ', name_on_order)



#Displaying Files
cnx = st.connection("snowflake")
session = cnx.session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'))
#st.dataframe(data=my_dataframe, use_container_width=True)

#multiselect
ingredients_list = st.multiselect(
    'Choose up to 5 ingredients: ',
    my_dataframe,
    max_selections=5 #max fruits is 5
)

if ingredients_list:
    #st.write(ingredients_list)
    #st.text(ingredients_list)

    ingredients_string=''
    for fruit_chosen in ingredients_list:
        ingredients_string+=fruit_chosen + ' '
        st.subheader(fruit_chosen + 'Nutrition Information')
        fruityvice_response = requests.get("https://fruityvice.com/api/fruit/watermelon")
        fv_df = st.dataframe(data=fruityvice_response.json(), use_container_width=true)

    
    st.write(ingredients_string)
    
    #code validator
    my_insert_stmt = """ insert into smoothies.public.orders(ingredients,name_on_order)
            values ('""" + ingredients_string + """','""" + name_on_order + """')"""

    #st.write(my_insert_stmt)
    #st.stop()

    time_to_insert = st.button('Submit Order')
    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        st.success('Your Smoothie is ordered!', icon="✅")


#New section to display fuirtyvice nutrition information



