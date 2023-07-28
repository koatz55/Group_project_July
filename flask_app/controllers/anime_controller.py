from flask_app import app
from flask import render_template, redirect, request, session
from flask_app.models.anime import Anime
from flask_app.models.user import User

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect('/user/login')
    user = User.get_by_id({"id":session['user_id']})
    if not user:
        return redirect('/user/logout')
        
    return render_template('dashboard.html', animes=Anime.get_all())

@app.route('/anime/new')
def create_anime():
    if 'user_id' not in session:
        return redirect('/user/login')

    return render_template('create.html') #template name needed

@app.route('/animes/new/process', methods=['POST'])
def process_anime():
    if 'user_id' not in session:
        return redirect('/user/login')
    if not Anime.validate_anime(request.form):
        return redirect('/animes/new')

    data = {
        'user_id': session['user_id'],
        'name': request.form['name'],
        'genre': request.form['genre'],
    }
    Anime.save(data)
    return redirect('/dashboard')

@app.route('/animes/<int:id>')
def view_anime(id):
    if 'user_id' not in session:
        return redirect('/user/login')

    return render_template('',anime=Anime.get_by_id({'id': id})) # template name needed

@app.route('/animes/edit/<int:id>')
def edit_anime(id):
    if 'user_id' not in session:
        return redirect('/user/login')
    return render_template('edit.html',anime=Anime.get_by_id({'id': id})) # template name needed

@app.route('/animes/edit/process/<int:id>', methods=['POST'])
def process_edit_anime(id):
    if 'user_id' not in session:
        return redirect('/user/login')
    if not Anime.validate_anime(request.form):
        return redirect(f'/animes/edit/{id}')

    data = {
        'id': id,
        'name': request.form['name'],
        'genre': request.form['genre'],
    }
    Anime.update(data)
    return redirect('/dashboard')

@app.route('/animes/destroy/<int:id>')
def destroy_anime(id):
    if 'user_id' not in session:
        return redirect('/user/login')

    Anime.destroy({'id':id})
    return redirect('/dashboard')

@app.route('/vote/<int:id>')
def vote(id):
    id = {
        'id':request.form
    }
    Anime.update_vote(id)
    return redirect('/animes/topten')

@app.route('/animes/topten')
def get_topten():
    if 'user_id' not in session:
        return redirect('/user/login')
    topten  = Anime.get_topten()
    return render_template('index.html', topten=topten )