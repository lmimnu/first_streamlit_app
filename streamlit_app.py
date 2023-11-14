import streamlit

streamlit.title("My parents new healthy diner")

streamlit.header("BreakFast favourites")

streamlit.text('🥣 Omega3 & Blueberry oatmeal')
streamlit.text(' 🥗 Kale, Spinach & Rocket Smoothhie')
streamlit.text("🐔 Hard-Boiled Free-Range Egg")
streamlit.text("🥑🍞 Avocado Toast")

import pandas
streamlit.header("🥣 🥗 Build your own fruit smoothie 🥑🍞")
my_fruit_list= pandas.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
my_fruit_list = my_fruit_list.set_index('Fruit')

# Let's put a pick list here so they can pick the fruit they want to include 
fruits_selected = streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index),[])

fruits_to_show = my_fruit_list.loc[fruits_selected]
# Display the table on the page. 
streamlit.dataframe(fruits_to_show)

# New section to display fruity vice Api response. 

streamlit.header("🥣 Fruityvice fruit advice 🥑")
import requests

fruit_choice = streamlit.text_input('What fruit would you like information about?','Kiwi')
streamlit.write('The user entered ', fruit_choice)

fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + fruit_choice)
#streamlit.text(fruityvice_response.json()) # Just displays the content
# normalize or parsing the json output what does the next line do? 
fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
# displays the parsed output in a readble format- what does this do?
streamlit.dataframe(fruityvice_normalized)

import snowflake.connector
my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
my_cur = my_cnx.cursor()
#my_cur.execute("SELECT CURRENT_USER(), CURRENT_ACCOUNT(), CURRENT_REGION()")
my_cur.execute("SELECT * from fruit_load_list")
#my_data_row = my_cur.fetchone()
my_data_rows = my_cur.fetchall()
#streamlit.text("Hello from Snowflake:")
#streamlit.text("The Fruit load list contains:")
#streamlit.text(my_data_row)

streamlit.header("The Fruit load list contains:")
streamlit.dataframe(my_data_rows)
# allow the end user to add the fruit
add_my_fruit = streamlit.text_input('What fruit would you like to add?','Jackfruit')
streamlit.write('Thanks for adding:', add_my_fruit)
