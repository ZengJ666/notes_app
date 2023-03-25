from flask_app import app
from flask import render_template, redirect, request, session
from flask_app.models.note import Note
from flask_app.models.user import User


@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect('/')

    user = User.get_by_id({'id': session['user_id']})

    if not user:
        return redirect('/logout')

    return render_template('dashboard.html', user=user, my_notes=Note.notes_by_user({'id': session['user_id']}))


@app.route('/note/<int:id>/delete')
def delete_note(id):
    Note.delete_note({'id': id})
    return redirect('/dashboard')


@app.route('/note/<int:id>/edit_page')
def edit_page(id):
    if 'user_id' not in session:
        return redirect('/')
    user = User.get_by_id({'id': session['user_id']})
    return render_template('edit_note_page.html', note=Note.get_one_by_id({'id': id}), user=user)


@app.route('/note/<int:id>/update', methods=['POST'])
def update_note(id):
    if 'user_id' not in session:
        return redirect('/')
    if not Note.validate_note(request.form):
        return redirect(f'/note/{id}/edit_page')

    note_data = {
        'id': id,
        'title': request.form['title'],
        'note_content': request.form['note_content']
    }

    Note.update_note(note_data)

    return redirect('/dashboard')


@app.route('/note/create_page')
def create_page():
    if 'user_id' not in session:
        return redirect('/')

    user = User.get_by_id({'id': session['user_id']})

    return render_template('create_note.html', user=user)


@app.route('/note/create', methods=['POST'])
def create_note():
    if 'user_id' not in session:
        return redirect('/')
    if not Note.validate_note(request.form):
        return redirect('/note/create_page')

    note_data = {
        'user_id': session['user_id'],
        'title': request.form['title'],
        'note_content': request.form['note_content'],
    }

    print(note_data['user_id'])

    Note.save_note(note_data)

    return redirect('/dashboard')


@app.route('/note/<int:id>/show')
def show_one_note(id):
    if 'user_id' not in session:
        return redirect('/')

    user = User.get_by_id({'id': session['user_id']})

    return render_template("show_1_note.html", user=user, note=Note.get_one_by_id({'id': id}))
