import streamlit
import pandas
import requests
import snowflake.connector
from urllib.error import URLError


streamlit.title("My parents new healthy diner:")

streamlit.header("BreakFast favourites")

streamlit.text('🥣 Omega3 & Blueberry oatmeal')
streamlit.text(' 🥗 Kale, Spinach & Rocket Smoothhie')
streamlit.text("🐔 Hard-Boiled Free-Range Egg")
streamlit.text("🥑🍞 Avocado Toast")

# import pandas
streamlit.header("🥣 🥗 Build your own fruit smoothie 🥑🍞")
my_fruit_list= pandas.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
my_fruit_list = my_fruit_list.set_index('Fruit')

# Let's put a pick list here so they can pick the fruit they want to include 
fruits_selected = streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index),[])

fruits_to_show = my_fruit_list.loc[fruits_selected]
# Display the table on the page. 
streamlit.dataframe(fruits_to_show)


# New reapeatble code block function for fruity vice
def get_fruityvice_data(this_fruit_choice):
    fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + this_fruit_choice)
    # normalize or parsing the json output what does the next line do? 
    fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
    return fruityvice_normalized

# New section to display fruity vice Api response. 
# import requests

streamlit.header("🥣 Fruityvice fruit advice 🥑")
try:
  fruit_choice = streamlit.text_input('What fruit would you like information about?')
  if not fruit_choice:
      streamlit.error("Please select a fruit to get the information.")
  else: 
      back_from_function =get_fruityvice_data(fruit_choice)
    # displays the parsed output in a readble format- what does this do?
      streamlit.dataframe(back_from_function)
except URLError as e:
  streamlit.error()

#fruit_choice = streamlit.text_input('What fruit would you like information about?','Kiwi')
#streamlit.write('The user entered ', fruit_choice)

#fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + fruit_choice)
#streamlit.text(fruityvice_response.json()) # Just displays the content
# normalize or parsing the json output what does the next line do? 
#fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
# displays the parsed output in a readble format- what does this do?
#streamlit.dataframe(fruityvice_normalized)

# dont run naything past here for troublshotting
#streamlit.stop()

# import snowflake.connector
# my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
# my_cur = my_cnx.cursor()
#my_cur.execute("SELECT CURRENT_USER(), CURRENT_ACCOUNT(), CURRENT_REGION()")
#my_cur.execute("SELECT * from fruit_load_list")
#my_data_row = my_cur.fetchone()
#my_data_rows = my_cur.fetchall()
#streamlit.text("Hello from Snowflake:")
#streamlit.text("The Fruit load list contains:")
#streamlit.text(my_data_row)

streamlit.header("view our Fruit list - Add your favorites!")
# snowflake related functions
#my_cur = my_cnx.cursor()
#my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
def get_fruit_load_list():
    with my_cnx.cursor() as my_cur:
        my_cur.execute("SELECT * from fruit_load_list")
        return my_cur.fetchall()

# add a button to load the fruit
if streamlit.button('Get fruit load list'):
    my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
    my_data_rows = get_fruit_load_list()
    my_cnx.close()
    streamlit.dataframe(my_data_rows)

#streamlit.stop()
# allow the end user to add the fruit
def insert_row_snowflake(new_fruit):
    with my_cnx.cursor() as my_cur:
        my_cur.execute("insert into fruit_load_list values ('"+ new_fruit +"')")
        return "Thanks for adding the fruit:" + new_fruit
add_my_fruit = streamlit.text_input('What fruit would you like to add?')
# add a button to load the fruit
if streamlit.button('Add a fruit to the list'):
    my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
    back_from_function = insert_row_snowflake(add_my_fruit)
    my_cnx.close()
    streamlit.text(back_from_function)
streamlit.stop()
#streamlit.write('Thanks for adding:', add_my_fruit)

# this will not worki correcty temporary
my_cur.execute("insert into fruit_load_list values ('from streamlit')")
