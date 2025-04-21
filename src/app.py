from flask import Flask, render_template, send_from_directory, request, redirect, url_for, flash
import os
from models.series import Series
from models.book import Book
from utils.file_handler import FileHandler

app = Flask(__name__)

app.secret_key = "5a8cd760bac219525b6c61addcb935d2ab79b556d47030651062d410e75d6623"

# Configuration
BOOKS_FOLDER = os.path.join('static', 'books')
if not os.path.exists(BOOKS_FOLDER):
    os.makedirs(BOOKS_FOLDER)
file_handler = FileHandler(BOOKS_FOLDER)

# Stockage temporaire (à remplacer par une base de données)
series_list = []
books_list = []

for i in series_list:
    print(series_list[i]) 
    
for i in books_list:
    print(books_list[i])

@app.route('/')
def index():
    # Charger les séries depuis le système de fichiers
    series_names = file_handler.get_series_list()
    series_list.clear()
    
    for idx, name in enumerate(series_names):
        series = Series(id=idx+1, title=name)
        books = file_handler.get_books_in_series(name)
        for book_idx, book_name in enumerate(books):
            book = Book(id=book_idx+1, title=book_name, series_id=idx+1,
                       file_path=os.path.join(name, book_name))
            series.add_book(book)
            books_list.append(book)
        series_list.append(series)
    
    return render_template('series/index.html', series=series_list)

@app.route('/series/<int:series_id>')
def view_series(series_id):
    series = next((s for s in series_list if s.id == series_id), None)
    if series is None:
        flash('Série non trouvée', 'error')
        return redirect(url_for('index'))
    return render_template('series/view.html', series=series)

@app.route('/book/<int:book_id>/view')
def view_book(book_id):
    book = next((b for b in books_list if b.id == book_id), None)
    if book is None:
        flash('Livre non trouvé', 'error')
        return redirect(url_for('index'))
    return render_template('books/view.html', book=book)

@app.route('/book/<int:book_id>')
def download_book(book_id):
    book = next((b for b in books_list if b.id == book_id), None)
    if book:
        print(f"Tentative de téléchargement - Chemin du livre : {book.file_path}")
        print(f"Dossier des livres : {BOOKS_FOLDER}")
        try:
            # Vérifier si le fichier existe
            file_path = os.path.join(BOOKS_FOLDER, book.file_path)
            if not os.path.exists(file_path):
                raise FileNotFoundError(f"Le fichier {file_path} n'existe pas")

            directory = os.path.dirname(file_path)
            filename = os.path.basename(file_path)

            return send_from_directory(
                directory,
                filename,
                as_attachment=True,
                download_name=f"{book.title}.pdf"
            )
        except Exception as e:
            print(f"Erreur lors du téléchargement : {str(e)}")
            flash('Erreur lors du téléchargement du fichier', 'error')
            return redirect(url_for('view_book', book_id=book_id))
    return "Livre non trouvé", 404

@app.route('/series/new', methods=['GET'])
def new_series():
    # Récupérer les livres non classés
    unassigned_books = file_handler.get_unassigned_books()
    return render_template('series/new.html', unassigned_books=unassigned_books)

@app.route('/series/create', methods=['POST'])
def create_series():
    series_name = request.form.get('series_name')
    selected_books = request.form.getlist('books[]')

    if not series_name:
        flash('Le nom de la série est requis', 'error')
        return redirect(url_for('new_series'))
    
    try:
        # Créer le dossier de la série
        file_handler.create_series_folder(series_name)
        
        # Déplacer les livres sélectionnés
        for book in selected_books:
            file_handler.move_book_to_series(book, series_name)
        
        flash(f'Série "{series_name}" créée avec succès', 'success')
        return redirect(url_for('index'))
    
    except Exception as e:
        flash(f'Erreur lors de la création de la série: {str(e)}', 'error')
        return redirect(url_for('new_series'))

if __name__ == '__main__':
    app.run(debug=True)