
# Appointment System with Document Chat

Welcome to the **Appointment System with Document Chat**, an application designed to combine efficient appointment scheduling with document-based conversational AI. Users can book appointments and interact with PDF documents through an intuitive interface.

---

## Features

### 1. User Registration
- Collect user details: Name, Phone Number, Email.
- Input validation ensures all entries are correctly formatted.

### 2. Appointment Booking
- Accepts appointment dates in natural language (e.g., "Next Monday").
- Stores and manages appointment data in a secure database.

### 3. PDF Document Interaction
- Upload a PDF file to extract and query its content.
- The system splits PDF text into chunks for efficient search.

### 4. Admin Dashboard
- View and manage all registered users and scheduled appointments.

---

## Tech Stack

- **Python**: Core programming language.
- **Streamlit**: Web application framework.
- **SQLite**: Database for storing user and appointment data.
- **PyPDF2**: PDF text extraction.
- **FAISS**: Efficient similarity search for text chunks.
- **LangChain**: Manages text splitting and interaction.
- **Dateparser**: Parses natural language date inputs.

---

## Code Structure

### 1. `app.py`
- **Purpose**: Manages the user interface and navigation.
- **Key Functions**:
  - User registration and validation.
  - PDF document upload and interaction.
  - Appointment booking and query handling.

### 2. `book_appointment.py`
- **Purpose**: Handles database interactions and appointment logic.
- **Key Functions**:
  - Database creation (`create_database`).
  - Save and retrieve user and appointment data (`save_user`, `save_appointment`, etc.).
  - Parse and validate appointment dates (`parse_date`).

### 3. `mistal_with_vectors.py`
- **Purpose**: Processes PDF documents for querying.
- **Key Functions**:
  - Extracts text from PDFs (`get_pdf_text`).
  - Splits text into manageable chunks (`get_text_chunks`).
  - Creates a vector store for efficient queries (`create_vector_store`).

### 4. `user_info_form.py`
- **Purpose**: Validates user input.
- **Key Functions**:
  - Validates email and phone number formats (`validate_email`, `validate_phone_number`).

---

## Getting Started

### Prerequisites
- Python 3.8+
- Required libraries: Streamlit, PyPDF2, LangChain, FAISS, Dateparser, Requests.

### Installation

1. Clone the repository:
   ```bash
   git clone <repository-url>
   ```
2. Navigate to the project directory:
   ```bash
   cd <project-folder>
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

### Running the Application

1. Ensure the database is set up:
   ```bash
   python book_appointment.py
   ```
2. Launch the application:
   ```bash
   streamlit run app.py
   ```

---

## Usage

### For Users:
1. Enter your personal information (name, phone, email).
2. Choose between booking an appointment or interacting with a PDF document.
3. Upload PDFs or enter natural language queries to schedule appointments.

### For Admins:
1. View all registered users and scheduled appointments in the Admin dashboard.

---

## Future Improvements
- Add user authentication.
- Enhance natural language understanding for queries.
- Improve PDF parsing for complex layouts (e.g., tables and images).
