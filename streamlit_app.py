import streamlit
import pandas as pd
import snowflake.connector
import requests
from urllib.error import URLError


streamlit.title("My Parents New Healthy Diner") 

streamlit.header('Breakfast Favorites')
streamlit.text('🥣 Omega 3 & Blueberry Oatmeal')
streamlit.text('🥗 Kale, Spinach & Rocket Smoothie')
streamlit.text('🐔 Hard-Boiled Free-Range Egg')
streamlit.text('🥑🍞 Avocado Toast')

streamlit.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')


my_fruit_list = pd.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
my_fruit_list = my_fruit_list.set_index('Fruit')
# Let's put a pick list here so they can pick the fruit they want to include 
fruits_selected = streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index), ['Avocado', 'Strawberries'])

fruits_to_show = my_fruit_list.loc[fruits_selected,:]
streamlit.dataframe(fruits_to_show)

def get_fruityvice_data(fruit_choice):
  
  fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + fruit_choice)
  return pd.json_normalize(fruityvice_response.json())
  

streamlit.header("Fruityvice Fruit Advice!")

try:
  
  fruit_choice = streamlit.text_input('What fruit would you like information about?')
  #streamlit.write('The user entered ', fruit_choice)
  if not fruit_choice:
    streamlit.error("Please select a fruit to get information")
  else:
    
    fun_value = get_fruityvice_data(fruit_choice)
    streamlit.dataframe(fun_value)
    
except URLError as e:
  
  streamlit.stop()
  
  
streamlit.text("The fruit load list contains:")
  
def get_fruit_load_list(my_cnx):
  
  my_cur = my_cnx.cursor()
  my_cur.execute("select * from pc_rivery_db.public.fruit_load_list")
  return my_cur.fetchall()

if streamlit.button('Get Fruit Load List'):
  
  my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
  my_data_rows = get_fruit_load_list(my_cnx)
  streamlit.dataframe(my_data_rows)
  my_cnx.close()

def insert_row_snowflake(new_fruit, my_cnx):
  
  my_cur = my_cnx.cursor()
  my_cur.execute("Insert into pc_rivery_db.public.fruit_load_list values ('" + ???? + "')")
  return "Thanks for adding " + new_fruit

add_my_fruit = streamlit.text_input('What fruit would you like to add?')

if streamlit.button('Add a Fruit to the List'):
  
  my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
  fun_value = insert_row_snowflake(add_my_fruit, my_cnx)
  streamlit.text(fun_value)
  my_cnx.close()


