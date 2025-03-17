import streamlit as st
import json
import os

# File to store library data
LIBRARY_FILE = "library.json"

def load_library():
    if os.path.exists(LIBRARY_FILE):
        with open(LIBRARY_FILE, "r") as file:
            return json.load(file)
    return []

def save_library(library):
    with open(LIBRARY_FILE, "w") as file:
        json.dump(library, file, indent=4)

def add_book(library, title, author, year, genre, read_status):
    library.append({
        "title": title,
        "author": author,
        "year": int(year),
        "genre": genre,
        "read": read_status
    })
    save_library(library)

def remove_book(library, title):
    library[:] = [book for book in library if book["title"].lower() != title.lower()]
    save_library(library)

def search_books(library, query, search_by="title"):
    return [book for book in library if query.lower() in book[search_by].lower()]

def display_statistics(library):
    total_books = len(library)
    read_books = sum(1 for book in library if book["read"])
    percentage_read = (read_books / total_books * 100) if total_books > 0 else 0
    return total_books, percentage_read

# Load existing library
db = load_library()

# Streamlit UI
st.set_page_config(page_title="Personal Library Manager", page_icon="📚")
st.markdown("""
    <style>
    body {
        background-color: #f4f4f4;
    }
    .title-text {
        color: #4a4a4a;
        text-align: center;
    }
    </style>
""", unsafe_allow_html=True)

st.title("📚 Personal Library Manager")
st.image("library-hero.jpg", width=600)

menu = st.sidebar.radio("Menu", ["Add Book", "Remove Book", "Search Book", "Display All Books", "Statistics"])

if menu == "Add Book":
    st.header("➕ Add a New Book")
    title = st.text_input("Book Title")
    author = st.text_input("Author")
    year = st.number_input("Publication Year", min_value=1000, max_value=2025, step=1)
    genre = st.text_input("Genre")
    read_status = st.checkbox("Have you read this book?")
    
    if st.button("Add Book"):
        if title and author and year and genre:
            add_book(db, title, author, year, genre, read_status)
            st.success(f"'{title}' has been added to your library!")
        else:
            st.error("Please fill in all fields.")

elif menu == "Remove Book":
    st.header("🗑 Remove a Book")
    book_titles = [book["title"] for book in db]
    if book_titles:
        book_to_remove = st.selectbox("Select a book to remove", book_titles)
        if st.button("Remove Book"):
            remove_book(db, book_to_remove)
            st.success(f"'{book_to_remove}' has been removed.")
    else:
        st.warning("No books available to remove.")

elif menu == "Search Book":
    st.header("🔍 Search for a Book")
    search_by = st.radio("Search by", ["title", "author"])
    search_query = st.text_input("Enter search term")
    
    if search_query:
        results = search_books(db, search_query, search_by)
        if results:
            for book in results:
                st.write(f"**{book['title']}** by {book['author']} ({book['year']}) - {book['genre']} - {'Read' if book['read'] else 'Unread'}")
        else:
            st.warning("No books found.")

elif menu == "Display All Books":
    st.header("📖 Your Library")
    if db:
        for book in db:
            st.write(f"**{book['title']}** by {book['author']} ({book['year']}) - {book['genre']} - {'Read' if book['read'] else 'Unread'}")
    else:
        st.info("No books in your library yet.")

elif menu == "Statistics":
    st.header("📊 Library Statistics")
    total, percentage = display_statistics(db)
    st.write(f"Total Books: **{total}**")
    st.write(f"Percentage Read: **{percentage:.2f}%**")

st.sidebar.markdown("---")
st.sidebar.write("📌 Your book collection, organized and accessible.")
