import os
from datetime import datetime

from flask import Flask, render_template, request, redirect, url_for, flash
from sqlalchemy import or_

from data_models import db, Author, Book


# Create Flask application
app = Flask(__name__)
# Needed for using flash() messages (session encryption)
app.config["SECRET_KEY"] = "-secret-key_for_flash"

# Compute absolute path to current directory
basedir = os.path.abspath(os.path.dirname(__file__))

# Configure SQLite database URI
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{os.path.join(basedir, 'data/library.sqlite')}"

# Initialize SQLAlchemy with this app
db.init_app(app)

@app.route("/", methods=["GET"])
def home_page():
    """Home page: list, sort and search books."""
    sort = request.args.get("sort", "title")
    direction = request.args.get("direction", "asc")
    search = request.args.get("search", "").strip()

    # Base query joins books with authors
    query = Book.query.join(Author)

    # Apply keyword search if given
    if search:
        pattern = f"%{search}%"
        query = query.filter(
            or_(
                Book.title.ilike(pattern),
                Author.name.ilike(pattern),
                Book.isbn.ilike(pattern),
            )
        )

    # Choose sort column
    if sort == "author":
        sort_column = Author.name
    else:
        sort_column = Book.title

    # Apply sort direction
    if direction == "desc":
        query = query.order_by(sort_column.desc())
    else:
        query = query.order_by(sort_column.asc())
    books = query.all()

    return render_template("home.html", books=books, search=search, sort=sort, direction=direction)


@app.route('/add_author', methods=['GET', 'POST'])
def add_author():
    """Add a new author to the library."""
    if request.method == 'POST':
        name = request.form.get('name')
        birth_date_str = request.form.get('birth_date')
        date_of_death_str = request.form.get('date_of_death')

        # Basic validation for required birth date
        if not birth_date_str:
            error_message = "Birth date is required."
            return render_template(
                "add_author.html",
                success_message=None,
                error_message=error_message
            )

        # Convert string dates to Python date objects
        birth_date = datetime.strptime(birth_date_str, '%Y-%m-%d').date()
        date_of_death = datetime.strptime(date_of_death_str, '%Y-%m-%d').date() if date_of_death_str else None

        # Create and save the new author
        new_author = Author(
            name=name,
            birth_date=birth_date,
            date_of_death=date_of_death
        )

        db.session.add(new_author)
        db.session.commit()

        flash("Author added successfully!", "success")
        return redirect(url_for("home_page"))

    return render_template("add_author.html")


@app.route('/add_book', methods=['GET', 'POST'])
def add_book():
    """Add a new book to the library."""
    if request.method == "POST":
        isbn = request.form.get("isbn")
        title = request.form.get("title")
        publication_year = request.form.get("publication_year")
        author_id = request.form.get("author_id")

        # Convert numeric fields from string to int
        if publication_year:
            publication_year = int(publication_year)
        if author_id:
            author_id = int(author_id)

        # Create and save the new book
        new_book = Book(
            isbn=isbn,
            title=title,
            publication_year=publication_year,
            author_id=author_id
        )
        db.session.add(new_book)
        db.session.commit()

        flash("Book added successfully!", "success")
        return redirect(url_for("home_page"))

    # Load authors for the dropdown in the form
    authors = Author.query.all()
    return render_template("add_book.html", authors=authors)

@app.route('/book/<int:book_id>/delete', methods=['POST'])
def delete_book(book_id):
    """Delete a book and its author if no books remain."""
    book = Book.query.get(book_id)

    # If book does not exist, show error
    if not book:
        flash("Book not found.", "error")
        return redirect(url_for("home_page"))

    # Keep reference to the author before deleting the book
    author = book.author

    # Delete book and commit
    db.session.delete(book)
    db.session.commit()

    # Check if the author still has any books
    remaining_books = Book.query.filter_by(author_id=author.id).count()

    if remaining_books == 0:
        db.session.delete(author)
        db.session.commit()
        flash(f"Book and author '{author.name}' deleted.", "success")
    else:
        flash("Book deleted successfully.", "success")

    return redirect(url_for("home_page"))


if __name__ == "__main__":
    app.run(debug=True)