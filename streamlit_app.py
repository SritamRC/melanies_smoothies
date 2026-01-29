  # Import python packages
import streamlit as st
import pandas as pd
# from snowflake.snowpark.context import get_active_session
from snowflake.snowpark.functions import col
import requests
# Write directly to the app




st.title(f":cup_with_straw: Customize Your Smoothie :cup_with_straw:")
st.write(
  """Choose the fruits you want in your custom smoothie.
  """
)

name_on_order = st.text_input("Name on Smoothie")
if name_on_order:
    st.write("The name on your smoothi will be: ", name_on_order)    


# session = get_active_session()
cnx = st. connection("snowflake")
session = cnx. session ()
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'),col('SEARCH_ON'))
# Convert the Snowpark Dataframe to a Pandas Dataframe so we can use the LOC function
pd_df=my_dataframe.to_pandas()
# st.dataframe(pd_df)
# st.stop()
# my_dataframe = session.table("smoothies.public.fruit_options").select(col("FRUIT_NAME"))
# st.dataframe(data=my_dataframe, use_container_width=True)

ingredients_list = st.multiselect(
    "Choose upto 5 ingrediants: ",
    my_dataframe,
    max_selections = 5
)



ingrediant_string= ''
if ingredients_list:
    for each_fruit in ingredients_list:
       ingrediant_string+= each_fruit +' '
      
       search_on=pd_df.loc[pd_df['FRUIT_NAME'] == each_fruit, 'SEARCH_ON'].iloc[0]
       st.write('The search value for ', each_fruit,' is ', search_on, '.')
      
       st.subheader(each_fruit + ' Nutrition Information')
       smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/" + each_fruit)
       sf_df = st.dataframe(data=smoothiefroot_response.json(), use_container_width=True)    


    
# values ('"""+ingrediant_string+ """','"""+name_on_order+"""')"""
    my_insert_stmnt= """ INSERT INTO smoothies.public.orders(order_uid, ingredients, name_on_order)
    VALUES (smoothies.public.order_seq.nextval, ?, ?)

               """
    
    st.write(my_insert_stmnt)
    insert_time = st.button('Submit Order')

    if insert_time:
        session.sql(my_insert_stmnt, params=[ingrediant_string, name_on_order]).collect()
        st.success('Your Smoothie is ordered,'+name_on_order, icon= "✅")



