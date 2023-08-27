import streamlit as st 
import pymongo
import os
from PIL import Image
import easyocr
from sqlalchemy.sql import text

def main():
    st.title("Document Selector App")
    
    uploaded_file = st.file_uploader("Upload a document", type=["png", "jpeg", "gif"])
    col1, col2, col3 = st.columns([1,1,1])
    if col1.button("READ"):
        st.write("READ")
        conn = st.experimental_connection('mysql', type='sql')
        st.subheader('Sates and union territories and Transaction Count')
        df = conn.query('select * from bussiness_card_info', ttl=600)
        df=df.set_index("id")
        st.dataframe(df)

    if col2.button("UPDATE"):
        st.write("Button 2 was clicked!")
    if col3.button("DELETE"):
        st.write("Button 3 was clicked!")
        condition = st.text_input("Enter a condition for DELETE:", "")    
        if st.button('Click here for deletion of record'):  
            conn = st.experimental_connection('mysql', type='sql')
            with conn.session as s:
                s.execute(
                    text('DELETE FROM bussiness_card_info WHERE id =  (:arg1);'),
                    params=dict(arg1=int(condition) )
                        )
                s.commit()
            st.write("Entry Deleted")
            
    if uploaded_file is not None:
        st.write("You selected:", uploaded_file.name, ' ' , uploaded_file)
        pil_image = Image.open(uploaded_file)    
        st.image(pil_image)  
        reader = easyocr.Reader(['en']) # this needs to run only once to load the model into memory
        path = "Data Set\\" + uploaded_file.name
        result = reader.readtext( path  , detail = 0)
        st.write(result)
def question():
    st.write('new')       
 
if __name__ == "__main__":
    st.write('hello')
    main()


