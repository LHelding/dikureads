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
    
    authors_dict = {}

    ## slow af but works, better way to do this?
    unqiue_authors = list(set(authors_list))
    for author in unqiue_authors:
        cur.execute('INSERT INTO authors (author_name) VALUES (%s) RETURNING author_id', (author,))
        author_id = cur.fetchone()
        authors_dict[author] = author_id[0]

    return authors_dict

def insert_genre(dataset):
    ## Fetch unique genre from the dataset
    df = pd.read_csv('dataset/GoodReads_100k_books.csv')
    genre_list = []
    for genre in df['genre'].unique():
        genre = str(genre)
        genre.strip()
        genre.strip('"')

        genre_list += genre.split(",")

    genre_dict = {}
    ## slow af but works, better way to do this?
    unqiue_genre = list(set(genre_list))
    for genre in unqiue_genre:
        cur.execute('INSERT INTO genre (genre_name) VALUES (%s) RETURNING genre_id', (genre,))
        genre_id = cur.fetchone()
        genre_dict[genre] = genre_id[0]
    return genre_dict

def insert_books(dataset, authors_dict, genre_dict):
    df = pd.read_csv('dataset/GoodReads_100k_books.csv')
    df.dropna(subset=['isbn'], inplace=True)
    books = list(
    map(lambda x: tuple([str(x.isbn), x.title, int(x.pages), float(x.rating), x.bookformat, x.desc, x.img, x.author, x.genre]),
        df[['isbn', 'title', 'pages', 'rating', 'bookformat', 'desc', 'img', 'author', 'genre']].to_records(index=False))
    )

    args_str = ','.join(cur.mogrify("(%s, %s, %s, %s, %s, %s, %s)", i[:-2]).decode('utf-8') for i in books)
    cur.execute("INSERT INTO Books (isbn, title, pages, avg_rating, format, descr, img) VALUES " + args_str)

    for book in books:
        authors = list(set(book[7].strip().strip('"').split(",")))
        genre = list(set(str(book[8]).strip().strip('"').split(",")))
        for author in authors:
            author_id = authors_dict.get(author)
            if author_id:
                cur.execute('INSERT INTO written_by (book, author) VALUES (%s, %s)', (book[0], author_id))
            
        for gen in genre:
            genre_id = genre_dict.get(gen)
            if genre_id:
                cur.execute('INSERT INTO Book_Genre (book, genre) VALUES (%s, %s)', (book[0], genre_id))


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
            
        with open('utils/users.sql') as db_file:
            cur.execute(db_file.read())
        
        genre_dict = insert_genre('dataset/GoodReads_100k_books.csv')
        authors_dict = insert_authors('dataset/GoodReads_100k_books.csv')
        insert_books('dataset/GoodReads_100k_books.csv', authors_dict, genre_dict)



        conn.commit()

    conn.close()
