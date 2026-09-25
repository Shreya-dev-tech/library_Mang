import streamlit as st
import colorama
from colorama import Fore, Back, Style, init
import datetime 
from datetime import datetime 
import os 

st.set_page_config(
    page_title="Library Management System",
    layout="wide"
)

import streamlit as st

st.set_page_config(page_title="Library Management System", page_icon="📚", layout="centered")

st.markdown("<h1 style='text-align: center;'>📚 LIBRARY MANAGEMENT SYSTEM 📚</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: gray;'>Centralized Book Catalog & Member Management</p>", unsafe_allow_html=True)
st.divider()

def menu():
    init(autoreset=True)
    print(Fore.CYAN + '''╔══════════════════════════════════════════════╗
║                                              ║
║        📚  LIBRARY MANAGEMENT SYSTEM  📚     ║
║                                              ║
╚══════════════════════════════════════════════╝''')
    print(Style.BRIGHT+Fore.YELLOW+"""
     1. Add Book
     2.View Books
     3.Search Book
     4.Register User
     5.Issue Book
     6.Exit """)

def read_book():
     """"This Function is majorly to read contents of the file """

     with open ("book_data.txt" ,"r") as file :
         book_data=file.readlines()
     return book_data

def add_book():
    """"This is a function to add a book in Libary Managment System """
    book_data=read_book()
    print(Fore.GREEN + "--- ADD BOOK ---")
    book_name = input("Enter Book Name : ").strip().title()
    for i in book_data :
        if book_name in i :
            print(Fore.RED+ "The Book Already Exists")
            print(Fore.RED + "Terminating The Function .... \n please Update Function ")
            return None 
    book_id = len(book_data) + 1

    # while True :
    #     book_id=input("Enter Book ID : ").strip()
    #     if book_id .isdigit():
    #         book_id=int(book_id)
    #         break
    #     else:
    #         print(Fore.RED + "INVAILD Book ID \n Enter Only Numbers ")
    
    book_author=input("Enter a author's name : ").strip().title()
    print(Fore.GREEN + "Book ID --" , book_id)

    error_message=Fore.RED + "INVALID quantity entered \n Pls Try Again "
    while True:
        book_qauntity =input("Enter Qauntity Of Book : ").strip()
        if book_qauntity .isdigit():
            if int(book_qauntity) > 0 :
                book_qauntity = int(book_qauntity)
                break
            else:
                print(error_message)
        else:
            print(error_message)
    print(Fore.GREEN + f'{"Book Added Successfully ":^100}')
    with open("book_data.txt" ,"a") as file :
        file.write(f"{book_id},{book_name},{book_author},{book_qauntity} \n")

def user():
    with open ("user_data.txt" ,"r") as file :
             user_data=file.readlines()
    return user_data
    
user_data = user()

def view_book():
    book_data=read_book()
    print(Fore.GREEN + "--- VIEW BOOK ---")
    if len(book_data) ==  0 :
        print(Fore.RED + "There is no Book in Database to View ")
    else:
        for i in book_data :
            i = i.replace("\n", "")
            i = i.split(",")
            print(Fore.CYAN + f"Book ID : {i[0]} | Book Name : {i[1]} | Book Author : {i[2]} | Book Qauntity : {i[-1] }")

def search_book(var):
    print(Fore.GREEN + "--- SEARCH BOOK ---")
    book_data= read_book()
    if len(book_data) == 0 :
        print(Fore.RED + "There is no Book in Database to Search ")
    else :
        for i in book_data :
             i = i.replace("\n", "")
             i = i.split(",")
             if var.isdigit() :
                 if i[0].strip()== var.strip():
                     print("\n")
                     print(Fore.CYAN + f"Book ID : {i[0]} | Book Name : {i[1]} | Book Author : {i[2]} | Book Qauntity : {i[-1] }")
                     return i 
             else:
                    if i[1].strip().lower() ==  var.strip().lower() :
                        print("\n")
                        print(Fore.CYAN + f"Book ID : {i[0]} | Book Name : {i[1]} | Book Author : {i[2]} | Book Qauntity : {i[-1] }")
                        return i
                    
def issue_book():
    print(Fore.GREEN + "--- ISSUE BOOK ---")
    user_data = user()
    book_data = read_book()
    user_id = input("Enter User Id : ")
    for i in user_data :
        i = i.replace("\n", "")
        i = i.split(",")
        if user_id.isdigit() :
            if i[0].strip()== user_id.strip():
                print(Fore.YELLOW + "User Id Accepted ")
        else:
            print(Fore.RED + "Error Try Again")
    var=input("Enter Book ID or Book Name : ")
    book_details = search_book(var)
    quantity = input("Enter Qauntity : ")
    if quantity in book_data :
         i = i.replace("\n", "")
         i = i.split(",")
         quantity = i[-1] - quantity 
         
    print(Fore.GREEN + f"For the User {user_id} book {book_details[1]} has been issued on {datetime.now().strftime("%d-%m-%Y")}")


def register_user():
    print(Fore.GREEN + "--- REGISTER USER ---")
    user_id = len(user_data) + 1
    print("User ID : " ,user_id)
    user_name=input("Enter User Name : ").strip().title()
    number=input("Enter a Mobile Number : ")
    if len(number) !=10 :
        print(Fore.RED + "Invalid Format ")
    else:
        print(Fore.GREEN + "USER REGISTERED SUCCESSFULLY ")
    with open("user_data.txt" , "a") as file :
       file.write(f"{user_id} , {user_name} , {number}\n")
       #user_id.append(f"{user_id} , {user_name} , {number}\n")

def exit():
    print(Fore.GREEN + "--- EXIT ---")
    print(Fore.GREEN+ "THANK YOU for using our LIBRARY System !!")



while True :
    menu()
    choice = input("Enter Your Choice between 1 to 6 : ")
    if choice == "1" :
        add_book()
    elif choice == "2":
        view_book()
    elif choice == "3":
        var=input("Enter Book Name or Book ID  : ")
        search_book(var)
    elif choice == "4":
        register_user()
    elif choice == "5":
        issue_book()
    elif choice == "6":
        exit()
        break
    else :
        print(Fore.RED+ "Invalid Choice , Enter Again ")