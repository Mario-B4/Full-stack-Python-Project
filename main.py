from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

@app.route('/index')
def index():
    return render_template ("index.html")

@app.route('/services', methods=['GET', 'POST'])
def services():
    if request.method == 'POST':
        # Check if any rows were selected for removal
        if 'remove' in request.form:
            # Get the selected row IDs
            selected_rows = request.form.getlist('row')
            # Connect to the database
            connection = sqlite3.connect('services.db')
            cursor = connection.cursor()
            # Remove the selected rows from the database
            for row_id in selected_rows:
                cursor.execute('DELETE FROM services WHERE id = ?', (row_id,))
            connection.commit()
            connection.close()

            return redirect('services.db')

        else:
            name = request.form['name']
            price = request.form['price']
            description = request.form['description']

            # Connect to the database
            connection = sqlite3.connect('services.db')
            cursor = connection.cursor()

            # Insert the new entry into the database
            cursor.execute('INSERT INTO services (name, price, description) VALUES (?, ?, ?)', (name, price, description))
            connection.commit()
            connection.close()

            return redirect('/services')

    else:
        # Connect to the database
        connection = sqlite3.connect('services.db')
        cursor = connection.cursor()

        # Get all services from the database
        cursor.execute('SELECT * FROM services ORDER BY id DESC')
        table = cursor.fetchall()

        connection.close()

        return render_template('services.html', services=table)
    

@app.route('/projects')
def projects():
    return render_template ("projects.html")

@app.route('/contacts')
def contacts():
    return render_template ("contacts.html")


@app.route('/aboutus')
def about():
    return render_template ("aboutus.html")

@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404


if __name__ == '__main__':
    app.run(debug=True)
