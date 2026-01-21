# Import python packages
import streamlit as st
from snowflake.snowpark.functions import col
import requests
import pandas as pd

# Write directly to the app
st.title("\U0001F964CustomizeYourSmoothie!\U0001F964")
st.write(
  """Choose the fruits you want in your custom Smoothie
  """
)

NAME_ON_ORDER = st.text_input('Name on Smoothie')
st.write('The Name on your Smoothie will be:',NAME_ON_ORDER)

cnx = st.connection("snowflake")
session = cnx.session()

my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'),col('SEARCH_ON'))
#st.dataframe(data=my_dataframe, use_container_width=True)
#st.stop()

#Convert the snowpark Dataframe to a Pandas Dataframe so we can use the LOC function
pd_df=my_dataframe.to_pandas()
st.dataframe(pd_df)
st.stop()


ingredients_list = st.multiselect(
    'Choose uo to 5 ingredients:'
    ,my_dataframe
    ,max_selections = 5
)
if ingredients_list:
    ingredients_string =''
    
    for fruit_chosen in ingredients_list:
        ingredients_string += fruit_chosen +' '
        st.subheader(fruit_chosen+' Nutrition Information')
        smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/" + fruit_chosen)
        sf_df = st.dataframe(data=smoothiefroot_response.json(),use_container_width=True)
      
        my_insert_stmt = """insert into smoothies.public.orders(INGREDIENTS,NAME_ON_ORDER)
            values('"""+ ingredients_string +"""','"""+NAME_ON_ORDER+"""')"""

    st.write(my_insert_stmt)
    #st.stop()
    time_to_insert = st.button('Submit Order')

    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        st.success('Your Smoothie is ordered, '+NAME_ON_ORDER+' !', icon="✅")


