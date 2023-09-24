import streamlit as st 
import pymongo
import os
from PIL import Image
import easyocr
from sqlalchemy.sql import text
import numpy as np

def main():
    st.title("Document Selector App")
    st.markdown("<div id='target'></div>", unsafe_allow_html=True)
    uploaded_file = st.file_uploader("Upload a document", type=["png", "jpeg", "gif"])
    if uploaded_file is not None:
        st.write("You selected:", uploaded_file.name, ' ' , uploaded_file)
        pil_image = Image.open(uploaded_file)
        if pil_image.mode != 'RGB':
            image = pil_image.convert('L')
        # Define the new size (width, height)
        new_size = (1000, 900)
        resized_image = image.resize(new_size)
        resized_image.save("output.jpg")
        st.image(pil_image)  
        reader = easyocr.Reader(['en']) # this needs to run only once to load the model into memory
        path = "output.jpg"
        result = reader.readtext( path  , detail = 0)
        st.write(result)
        if st.button('Click here for saving the records'):  
            conn = st.experimental_connection('mysql', type='sql')
            with conn.session as s:
                s.execute(
                    text('insert into bussiness_card_info (card_holder_name , designation, address , mobile_number, Email_address, url , company_name) values (:arg1, :arg2, :arg3, :arg4 , :arg5, :arg6 , :arg7)'),
                params=dict(arg1= result[0], arg2= result[1],  arg3= result[2],  arg4= result[4],  arg5= result[5], arg6= result[6], arg7= result[7])
                        )
                s.commit()
            st.write("Entry saved")
    
    col1, col2, col3 = st.columns([1,1,1])
    if col1.button("READ"):
        #st.write("READ")
        conn = st.experimental_connection('mysql', type='sql')
        st.subheader('All the bussiness card related Information')
        df = conn.query('select * from bussiness_card_info')
        df=df.set_index("id")
        st.dataframe(df)

    if col2.button("UPDATE"):
        st.write("Button 2 was clicked!")
    options = ["designation", "company_name","card_holder_name","designation","mobile_number","Email_address","url","area","city","state","pincode"]
    condition = st.text_input("Enter record id to UPDATE:", "")    
    column = st.selectbox("Select an option:", options)
    value= st.text_input("Enter New Value:", "")
    if st.button('Click here for updating of record'):  
            conn = st.experimental_connection('mysql', type='sql')
            with conn.session as s:
                sql = 'update bussiness_card_info set ' + column + ' = "' + value +'" WHERE id =  '+ condition +' ;'
                st.write(sql)
                s.execute(
                    text(sql),
                    params=dict(arg1=int(condition) ,arg2 = column , arg3 = value )
                        )
                s.commit()
            st.write("Entry updated")
        

    if col3.button("DELETE"):
        st.write("Button 3 was clicked!")
    condition1 = st.text_input("Enter a Record ID for DELETE:", "")    
    if st.button('Click here for deletion of record'):  
        conn = st.experimental_connection('mysql', type='sql')
        with conn.session as s:
            s.execute(
                text('DELETE FROM bussiness_card_info WHERE id =  (:arg1);'),
                params=dict(arg1=int(condition1) )
                )
            s.commit()
            st.write("Entry Deleted")
            
    
def question():
    st.write('new')       
 
if __name__ == "__main__":
    main()


