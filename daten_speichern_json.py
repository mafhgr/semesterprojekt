'''
def save_books(books):
    with open('books.json', 'w') as file:
        json.dump(books, file, indent=4)

def load_books():
    with open('books.json', 'r') as file:
        books = json.load(file)
    return books

#books einlesen
books = load_books()

#buch hinzufügen
books.append({...})

#speichern
save_books(books)
'''