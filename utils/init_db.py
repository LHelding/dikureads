import psycopg2
import os
from dotenv import load_dotenv
import pandas as pd
import ctypes

load_dotenv()

def insert_authors(dataset):
    ## Fetch unique authors from the dataset
    df = pd.read_csv('dataset/GoodReads_100k_books.csv')
    authors_list = []
    for author in df['author'].unique():
        author.strip()
        author.strip('"')

        authors_list += author.split(",")

    ## slow af but works, better way to do this?
    unqiue_authors = list(set(authors_list))
    for author in unqiue_authors:
        cur.execute('INSERT INTO authors (author_name) VALUES (%s)', (author,))

def insert_genre(dataset):
    ## Fetch unique genre from the dataset
    df = pd.read_csv('dataset/GoodReads_100k_books.csv')
    genre_list = []
    for genre in df['genre'].unique():
        genre = str(genre)
        genre.strip()
        genre.strip('"')

        genre_list += genre.split(",")

    ## slow af but works, better way to do this?
    unqiue_genre = list(set(genre_list))
    for genre in unqiue_genre:
        cur.execute('INSERT INTO genre (genre_name) VALUES (%s)', (genre,))

def insert_books(dataset):
    df = pd.read_csv('dataset/GoodReads_100k_books.csv')
    df.dropna(subset=['isbn'], inplace=True)
    books = list(
    map(lambda x: tuple([str(x.isbn), x.title, int(x.pages), float(x.rating), x.bookformat, x.desc]),
        df[['isbn', 'title', 'pages', 'rating', 'bookformat', 'desc']].to_records(index=False))
    )

    args_str = ','.join(cur.mogrify("(%s, %s, %s, %s, %s, %s)", i).decode('utf-8') for i in books)
    cur.execute("INSERT INTO Books (isbn, title, pages, avg_rating, format, descr) VALUES " + args_str)


if __name__ == '__main__':
    conn = psycopg2.connect(
        host=os.getenv('DB_HOST'),
        database=os.getenv('DB_NAME'),
        user=os.getenv('DB_USERNAME'),
        password=os.getenv('DB_PASSWORD')
    )
    with conn.cursor() as cur:

        with open('utils/books.sql') as db_file:
            cur.execute(db_file.read())
        
        #insert_genre('dataset/GoodReads_100k_books.csv')
        #insert_authors('dataset/GoodReads_100k_books.csv')
        insert_books('dataset/GoodReads_100k_books.csv')



        conn.commit()

    conn.close()
