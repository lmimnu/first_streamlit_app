import streamlit

streamlit.title("My parents new healthy diner")

streamlit.header("BreakFast favourites")

streamlit.text('🥣 Omega3 & Blueberry oatmeal')
streamlit.text(' 🥗 Kale, Spinach & Rocket Smoothhie')
streamlit.text("🐔 Hard-Boiled Free-Range Egg")
streamlit.text("🥑🍞 Avocado Toast")


import pandas
my_fruit_list= pandas.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
streamlit.dataframe(my_fruit_list)
