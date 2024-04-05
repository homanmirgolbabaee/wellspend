import streamlit as st
import pandas as pd
import plotly.express as px
from database_core import add_to_users_collection, init_weaviate_client , generate_unique_user_id , read_all_objects



# Initialize session state for login status and active page
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'active_page' not in st.session_state:
    st.session_state.active_page = 'Login'
    
    
# Placeholder data - Replace with actual data queries from your database
user_purchases = pd.DataFrame({
    'Product': ['Cheese', 'Bread', 'Eggs', 'Milk', 'Gooseberries'],
    'Amount': [50, 30, 20, 10, 40],
    'Health Score': [3, 5, 4, 4, 8],  # Example health score, 1-10
    'Category': ['Dairy', 'Bakery', 'Pantry', 'Dairy', 'Fruits']
})

# Placeholder for user data - replace with actual data retrieval and update mechanisms
user_profile = {
    'Name': 'Adam',
    'Email': 'adam@example.com',
    'Financial Goal': '$500 savings on groceries',
    'Health Goal': 'Increase fruit and veg intake',
    'Receive Notifications': True,
}

def manage_user_profile():
    st.title("👤 User Profile")
    with st.form("user_profile", clear_on_submit=False):
        st.subheader("Edit your profile information:")
        col1, col2 = st.columns(2)
        with col1:
            name = st.text_input("Name", user_profile['Name'])
            email = st.text_input("Email", user_profile['Email'])
        with col2:
            financial_goal = st.text_input("Financial Goal", user_profile['Financial Goal'])
            health_goal = st.text_input("Health Goal", user_profile['Health Goal'])
        
        receive_notifications = st.checkbox("Receive Notifications", user_profile['Receive Notifications'])
        RN = 1

        submitted = st.form_submit_button("Save Changes")

        if submitted:
            st.success("Profile updated successfully!")
            user_id = generate_unique_user_id(name, email)  # This is a placeholder function; implement accordingly
            user_id = "ROOT"
            client = init_weaviate_client()
            add_to_users_collection(client = client, name=name, financial_goal=financial_goal, email=email, health_goal=health_goal, notification_status=RN , user_id=user_id)
        
    if st.button("database"):
        read_all_objects()

''' 

### REPLIT COMMIT STARTS HERE ###
import streamlit as st
import pandas as pd
from fpdf import FPDF
import base64
import tempfile

def generate_pdf(table):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    for i, row in enumerate(table.itertuples(), 1):
        pdf.cell(0, 10, f'{i}. Category: {row.Category} - Item: {row.Item} - Price: {row.Price}', ln=True)
    # Save the PDF to a temporary file and return its path
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.pdf')
    pdf.output(temp_file.name)
    return temp_file.name

def download_link(object_to_download, download_filename, download_link_text):
    # Generates a link to download the given object_to_download
    if isinstance(object_to_download, pd.DataFrame):
        object_to_download = object_to_download.to_csv(index=False)
    b64 = base64.b64encode(object_to_download.encode()).decode()
    return f'<a href="data:file/txt;base64,{b64}" download="{download_filename}">{download_link_text}</a>'

def upload_receipt():
    st.title("📄 Upload Receipt")
    uploaded_file = st.file_uploader("Choose a file", type=['png', 'jpg', 'jpeg'])
    if uploaded_file is not None:
        st.image(uploaded_file, caption='Uploaded Receipt', use_column_width=True)
        with st.spinner('Processing...'):
            # Placeholder for OCR processing - replace with actual OCR/model code
            # For now, simulate data extraction
            extracted_data = {
                'Category': ['Groceries', 'Electronics'],
                'Item': ['Apples', 'Headphones'],
                'Price': [5.50, 199.99]
            }
            df_extracted = pd.DataFrame(extracted_data)
            st.success("Receipt processed successfully!")
            st.dataframe(df_extracted)

            # Assuming you have a function to append or update the extracted data to a database or a file
            # update_database(df_extracted)

            # Generate and display download link for the report (PDF)
            if st.button('Download Report as PDF'):
                pdf_path = generate_pdf(df_extracted)
                with open(pdf_path, "rb") as pdf_file:
                    base64_pdf = base64.b64encode(pdf_file.read()).decode('utf-8')
                pdf_display = f'<embed src="data:application/pdf;base64,{base64_pdf}" width="700" height="1000" type="application/pdf">'
                st.markdown(pdf_display, unsafe_allow_html=True)
                st.markdown(download_link(df_extracted, 'report.csv', 'Download CSV Report'), unsafe_allow_html=True)

# Remember to call upload_receipt somewhere in your app to display it.






### REPLIT COMMIT ENDS HERE ###

'''

def upload_receipt():
    st.title("📄 Upload Receipt")
    uploaded_file = st.file_uploader("Choose a file", type=['png', 'jpg', 'jpeg'])
    if uploaded_file is not None:
        st.image(uploaded_file, caption='Uploaded Receipt', use_column_width=True)
        with st.spinner('Processing...'):
            # Placeholder for actual processing
            st.success("Receipt processed successfully!")

def view_dashboard():
    st.title('📊 Your Dashboard')
    dashboard_mode = st.selectbox("Switch Dashboard Mode", ["Financial", "Health"])
    
        
        
    if dashboard_mode == "Financial":
        st.subheader("Financial Insights")
        fig = px.bar(user_purchases, x='Product', y='Amount', title="Spending by Product")
        st.plotly_chart(fig)
    elif dashboard_mode == "Health":
        st.subheader("Health Insights")
        health_fig = px.scatter(user_purchases, x='Product', y='Health Score', size='Amount', color='Category', title="Health Score of Purchases")
        st.plotly_chart(health_fig)

def app_settings():
    st.title("⚙️ Settings")
    st.write("Application settings and configurations will be managed here.")

def app_login():
    st.title("🔑 Login")
    st.write("User authentication will be managed here.")
    
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")
    
    if st.button("Login",key="maloo"):
        if email == "example@example.com" and password == "password":
            st.success("Login successful!")
            
            st.session_state.logged_in = True  # Update session state to logged in
            st.experimental_rerun()  # Immediately rerun the app to update UI
            
            
        else:
            st.error("Invalid email or password. Please try again.")
            
def app_logout():
    if st.button("Logout",key="logout-btn"):
        st.session_state.logged_in = False  # Reset login status
        st.experimental_rerun()  # Rerun the app to reflect logout on the UI
        
def app_insights():
    st.title("💡 Insights")
    st.write("Financial and health insights will be detailed here.")


def render_navigation():
    """Render the navigation bar with buttons for immediate switching."""
    if st.session_state.logged_in:
        pages = ["Dashboard", "Upload Receipt", "User Profile", "Insights", "Settings", "Logout"]
    else:
        pages = ["Login"]
    
    with st.sidebar:
        st.title("Navigate")
        for page in pages:
            if st.button(page):
                st.session_state.active_page = page
                st.experimental_rerun()  # Rerun the app with the new active_page

def main():
    render_navigation()

    if st.session_state.logged_in:
        if st.session_state.active_page == "Dashboard":
            view_dashboard()
        elif st.session_state.active_page == "Upload Receipt":
            upload_receipt()
        elif st.session_state.active_page == "User Profile":
            manage_user_profile()
        elif st.session_state.active_page == "Insights":
            app_insights()
        elif st.session_state.active_page == "Settings":
            app_settings()
        elif st.session_state.active_page == "Logout":
            app_logout()
    else:
        app_login()

if __name__ == "__main__":
    main()
