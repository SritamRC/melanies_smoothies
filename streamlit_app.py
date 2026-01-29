  # Import python packages
import streamlit as st
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
my_dataframe = session.table("smoothies.public.fruit_options").select(col("FRUIT_NAME"))
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
        smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/watermelon")
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



