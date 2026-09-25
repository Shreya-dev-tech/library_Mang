from datetime import datetime
import os
import pandas as pd
import streamlit as st


def set_light_modern_theme():
    st.markdown(
        """
        <style>
        /* Main page background */
        .stApp {
            background-color: #F8FAFC;
            color: #1E293B;
        }

        /* Sidebar light slate */
        section[data-testid="stSidebar"] {
            background-color: #EDF2F7 !important;
            border-right: 1px solid #E2E8F0;
        }
        section[data-testid="stSidebar"] * {
            color: #1E293B !important;
        }

        /* Headers */
        h1, h2, h3 {
            color: #0F172A !important;
            font-family: 'Segoe UI', Tahoma, sans-serif;
            font-weight: 700;
        }

        /* Input fields */
        .stTextInput input {
            background-color: #FFFFFF !important;
            color: #0F172A !important;
            border: 1px solid #CBD5E1 !important;
            border-radius: 6px;
        }

        /* Action Buttons */
        .stButton > button {
            background-color: #2563EB !important;
            color: #FFFFFF !important;
            border-radius: 6px;
            border: none;
            font-weight: 600;
        }
        .stButton > button:hover {
            background-color: #1D4ED8 !important;
        }
        </style>
        """,
        unsafe_allow_html=True
    )


def read_book():
    """This Function is majorly to read contents of the file"""
    if not os.path.exists("book_data.txt"):
        return []
    with open("book_data.txt", "r") as file:
        book_data = file.readlines()
    return book_data

def read_user():
    """Reads user records from user_data.txt"""
    if not os.path.exists("user_data.txt"):
        return []
    with open("user_data.txt", "r") as file:
        user_data = file.readlines()
    return user_data


# --- Feature Implementations ---

def add_book():
    st.subheader("📚 Add Book")
    book_data = read_book()

    with st.form("add_book_form", clear_on_submit=True):
        book_name = st.text_input("Enter Book Name:").strip().title()
        book_author = st.text_input("Enter Author's Name:").strip().title()
        book_quantity = st.text_input("Enter Quantity of Book:").strip()
        
        submitted = st.form_submit_button("Add Book")

        if submitted:
            if not book_name or not book_author or not book_quantity:
                st.error("Please fill in all fields.")
                return

            # Check if book already exists
            for line in book_data:
                parts = [p.strip() for p in line.split(",")]
                if len(parts) >= 2 and book_name.lower() == parts[1].lower():
                    st.error("The Book Already Exists. Please update quantity or check the name.")
                    return

            if not book_quantity.isdigit() or int(book_quantity) <= 0:
                st.error("INVALID quantity entered. Please enter a positive number.")
                return

            book_id = len(book_data) + 1
            with open("book_data.txt", "a") as file:
                file.write(f"{book_id},{book_name},{book_author},{book_quantity}\n")

            st.success(f"Book '{book_name}' (ID: {book_id}) Added Successfully!")


def view_book():
    st.subheader("📖 View Books")
    book_data = read_book()

    if not book_data:
        st.warning("There is no Book in Database to View.")
        return

    records = []
    for line in book_data:
        parts = [p.strip() for p in line.replace("\n", "").split(",")]
        if len(parts) >= 4:
            records.append({
                "Book ID": parts[0],
                "Book Name": parts[1],
                "Book Author": parts[2],
                "Quantity": parts[3]
            })

    st.dataframe(pd.DataFrame(records), use_container_width=True)


def search_book_ui():
    st.subheader("🔍 Search Book")
    var = st.text_input("Enter Book ID or Book Name:").strip()

    if st.button("Search"):
        if not var:
            st.warning("Please enter a search query.")
            return

        book_data = read_book()
        if not book_data:
            st.warning("There is no Book in Database to Search.")
            return

        found = False
        for line in book_data:
            parts = [p.strip() for p in line.replace("\n", "").split(",")]
            if len(parts) >= 4:
                match_id = var.isdigit() and parts[0] == var
                match_name = parts[1].lower() == var.lower()

                if match_id or match_name:
                    st.success("Book Found!")
                    st.markdown(
                        f"**Book ID:** {parts[0]} &nbsp;|&nbsp; "
                        f"**Book Name:** {parts[1]} &nbsp;|&nbsp; "
                        f"**Book Author:** {parts[2]} &nbsp;|&nbsp; "
                        f"**Quantity:** {parts[3]}"
                    )
                    found = True
                    break

        if not found:
            st.error("No matching book found.")


def register_user():
    st.subheader("👤 Register User")
    user_data = read_user()
    user_id = len(user_data) + 1
    st.info(f"Assigning User ID: **{user_id}**")

    with st.form("register_user_form", clear_on_submit=True):
        user_name = st.text_input("Enter User Name:").strip().title()
        number = st.text_input("Enter Mobile Number (10 digits):").strip()
        submitted = st.form_submit_button("Register User")

        if submitted:
            if not user_name:
                st.error("User name cannot be empty.")
            elif len(number) != 10 or not number.isdigit():
                st.error("Invalid Mobile Number! It must be exactly 10 digits.")
            else:
                with open("user_data.txt", "a") as file:
                    file.write(f"{user_id},{user_name},{number}\n")
                st.success(f"USER REGISTERED SUCCESSFULLY! (ID: {user_id}, Name: {user_name})")


def issue_book():
    st.subheader("📤 Issue Book")
    user_id=st.text_input("Enter User ID or Name:").strip()
    book_query = st.text_input("Enter Book ID or Book Name:").strip()
    issue_qty = st.text_input("Enter Quantity to Issue:").strip()

    if st.button("Issue Book"):
        if not user_id or not book_query or not issue_qty:
            st.error("Please fill in all fields.")
            return

        # 1. Validate User
        user_data = read_user()
        valid_user = False
        for line in user_data:
               parts = [p.strip() for p in line.replace("\n", "").split(",")]
               if len(parts) >= 2:
                   file_user_id=parts[0]
                   file_user_name=parts[1]
                   is_id_match= user_id.isdigit() and file_user_id == user_id
                   is_name_match= file_user_name.lower() == user_id.lower()
                   if is_id_match or is_name_match:
                       valid_user = True
                       break
        if not valid_user:
            st.error("User ID not found. Please register first.")
            return

        # 2. Validate Book
        book_data = read_book()
        target_idx = None
        book_parts = None

        for idx, line in enumerate(book_data):
            parts = [p.strip() for p in line.replace("\n", "").split(",")]
            if len(parts) >= 4:
                match_id = book_query.isdigit() and parts[0] == book_query
                match_name = parts[1].lower() == book_query.lower()
                if match_id or match_name:
                    target_idx = idx
                    book_parts = parts
                    break

        if target_idx is None:
            st.error("Book not found in library.")
            return

        # 3. Validate Quantity
        if not issue_qty.isdigit() or int(issue_qty) <= 0:
            st.error("Invalid quantity. Must be a positive integer.")
            return

        issue_qty = int(issue_qty)
        current_qty = int(book_parts[3])

        if issue_qty > current_qty:
            st.error(f"Cannot issue {issue_qty} books. Only {current_qty} available in stock.")
            return

        # 4. Update file inventory
        book_parts[3] = str(current_qty - issue_qty)
        book_data[target_idx] = f"{book_parts[0]},{book_parts[1]},{book_parts[2]},{book_parts[3]}\n"

        with open("book_data.txt", "w") as file:
            file.writelines(book_data)

        issue_date = datetime.now().strftime("%d-%m-%Y")
        st.success(f"For User **{user_id}**, book **{book_parts[1]}** (x{issue_qty}) has been issued on **{issue_date}**.")


# --- Main App Layout ---

def main():
    st.set_page_config(page_title="Library Management System", 
                       page_icon="📚", 
                       layout="centered")

    st.title("📚 Library Management System")
    st.markdown("---")

    menu_choice = st.sidebar.radio(
        "Navigation Menu",
        options=[
            "1. Add Book",
            "2. View Books",
            "3. Search Book",
            "4. Register User",
            "5. Issue Book",
            "6. Exit"
        ]
    )

    if menu_choice == "1. Add Book":
        add_book()
    elif menu_choice == "2. View Books":
        view_book()
    elif menu_choice == "3. Search Book":
        search_book_ui()
    elif menu_choice == "4. Register User":
        register_user()
    elif menu_choice == "5. Issue Book":
        issue_book()
    elif menu_choice == "6. Exit":
        st.success("THANK YOU for using our Library System! You can close this tab.")

if __name__ == "__main__":
    main()