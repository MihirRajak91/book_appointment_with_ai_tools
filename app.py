import streamlit as st
from user_info_form import validate_email, validate_phone_number  
from book_appointment import create_database, save_user, save_appointment, parse_date, fetch_all_users, fetch_all_appointments  
from mistal_with_vectors import get_pdf_text, get_text_chunks, create_vector_store, query_document  
create_database()

st.title("Appointment System with Document Chat")

# Initialize session state variables
if "user_id" not in st.session_state:
    st.session_state.user_id = None

# Navigation
menu = st.sidebar.radio("Navigation", ["User", "Admin"])

if menu == "User":
    # Step 1: Collect User Info
    st.header("Step 1: Enter Your Information")
    with st.form("user_info_form"):
        name = st.text_input("Full Name")
        phone = st.text_input("Phone Number")
        email = st.text_input("Email Address")
        submit_user_info = st.form_submit_button("Submit")

    if submit_user_info:
        if not name or not validate_phone_number(phone) or not validate_email(email):
            st.error("Please enter valid details.")
        else:
            st.session_state.user_id = save_user(name, phone, email)
            st.success(f"User information saved! User ID: {st.session_state.user_id}")

    # Step 2: Choose Action
    if st.session_state.user_id:
        st.header("Step 2: Choose an Action")
        action = st.radio("What would you like to do?", ["Book an Appointment", "Chat with a Document"])

        if action == "Book an Appointment":
            st.subheader("Book an Appointment")
            appointment_date_input = st.text_input("Enter appointment date (e.g., 'Next Monday', '2024-12-01')")
            if st.button("Book Appointment"):
                appointment_date = parse_date(appointment_date_input)
                if appointment_date:
                    save_appointment(st.session_state.user_id, appointment_date)
                    st.success(f"Appointment booked for {appointment_date}!")
                else:
                    st.error("Invalid date. Please try again.")

        elif action == "Chat with a Document":
            st.subheader("Upload a PDF to Chat")
            uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")
            if uploaded_file:
                # Step 1: Extract text from PDF
                text = get_pdf_text(uploaded_file)
                st.write("PDF Uploaded! Processing...")
                
                # Step 2: Split text into chunks and create vector store
                chunks = get_text_chunks(text)
                vector_store = create_vector_store(chunks)
                
                # Step 3: Query the document
                query = st.text_input("Enter your question:")
                if st.button("Ask"):
                    response = query_document(query, vector_store)
                    st.write("Response:", response)

    else:
        st.warning("Please submit your information first to proceed.")

elif menu == "Admin":
    st.header("Admin View")
    st.subheader("Users Information")
    users = fetch_all_users()
    if users:
        for user in users:
            st.write(f"ID: {user[0]}, Name: {user[1]}, Phone: {user[2]}, Email: {user[3]}")
    else:
        st.write("No users found.")

    st.subheader("Appointments Information")
    appointments = fetch_all_appointments()
    if appointments:
        for appointment in appointments:
            st.write(
                f"Appointment ID: {appointment[0]}, Name: {appointment[1]}, Phone: {appointment[2]}, "
                f"Email: {appointment[3]}, Date: {appointment[4]}"
            )
    else:
        st.write("No appointments found.")
