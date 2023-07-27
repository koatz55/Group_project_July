from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import user
from flask import flash

db = "anime_schema"
class Anime:
    def __init__(self, db_data):
        self.id = db_data['id']
        self.name = db_data['name']
        self.genre = db_data['genre']
        self.created_at = db_data['created_at']
        self.updated_at = db_data['updated_at']
        self.user_id = db_data['user_id']
        self.creator = None

    def get_likes(self):
        query = """
                SELECT u.first_name, u.last_name
                FROM users u
                JOIN likes k ON u.id = k.user_id
                WHERE k.anime_id = %(anime_id)s;
                """
        data = {
            'anime_id': self.id
        }
        results = connectToMySQL(db).query_db(query, data)
        likes = []
        for row in results:
            likes.append(f"{row['first_name']} {row['last_name']}")
        return likes

    @classmethod
    def toggle_likes_for_user(cls, anime_id, user_id):
        anime = cls.get_by_id(anime_id)
        if anime:
            if user_id in anime.likes:
                anime.destroy_like(user_id)
            else:
                anime.add_like(user_id)

    @classmethod
    def check_if_like(cls, anime_id, user_id):
        query = """
            SELECT * FROM likes
            WHERE user_id = %(user_id)s AND anime_id = %(anime_id)s;
        """
        data = {'user_id': user_id, 'anime_id': anime_id}
        results = connectToMySQL(db).query_db(query, data)
        return bool(results)

    @classmethod
    def add_like(cls, anime_id, user_id):
        query = """
                INSERT INTO likes (user_id, anime_id)
                VALUES (%(user_id)s, %(anime_id)s);
                """
        data = {'user_id': user_id, 'anime_id': anime_id}
        return connectToMySQL(db).query_db(query, data)

    @classmethod
    def remove_like(cls, anime_id, user_id):
        query = """
                DELETE FROM likes
                WHERE (%(user_id)s, %(anime_id)s);
                """
        data = {'user_id': user_id, 'anime_id': anime_id}
        return connectToMySQL(db).query_db(query, data)

    @classmethod
    def get_all(cls):
        query = """
                SELECT * FROM anime
                JOIN users on anime.user_id = users.id;
                """
        results = connectToMySQL(db).query_db(query)
        animes = []
        for row in results:
            this_anime = cls(row)
            user_data = {
                "id": row['users.id'],
                "first_name": row['first_name'],
                "last_name": row['last_name'],
                "email": row['email'],
                "password": "",
                "created_at": row['users.created_at'],
                "updated_at": row['users.updated_at']
            }
            this_anime.creator = user.User(user_data)
            animes.append(this_anime)
        return animes
    
    @classmethod
    def get_by_id(cls,data):
        query = """
                SELECT * FROM animes
                JOIN users on animes.user_id = users.id
                WHERE animes.id = %(id)s;
                """
        result = connectToMySQL(db).query_db(query,data)
        if not result:
            return False

        result = result[0]
        this_anime = cls(result)
        user_data = {
                "id": result['users.id'],
                "first_name": result['first_name'],
                "last_name": result['last_name'],
                "email": result['email'],
                "password": "",
                "created_at": result['users.created_at'],
                "updated_at": result['users.updated_at']
        }
        this_anime.creator = user.User(user_data)
        return this_anime

    @classmethod
    def save(cls, form_data):
        query = """
                INSERT INTO animes (name,genre,user_id)
                VALUES (%(name)s,%(genre)s,%(user_id)s);
                """
        return connectToMySQL(db).query_db(query,form_data)

    @classmethod
    def update(cls,form_data):
        query = """
                UPDATE animes
                SET name = %(name)s,
                genre = %(genre)s,
                WHERE id = %(id)s;
                """
        return connectToMySQL(db).query_db(query,form_data)
    
    @classmethod
    def destroy(cls,data):
        query = """
                DELETE FROM animes
                WHERE id = %(id)s;
                """
        return connectToMySQL(db).query_db(query,data)
    
    @staticmethod
    def validate_anime(form_data):
        is_valid = True

        if len(form_data['name']) < 1:
            flash("Name must be at least 1 character long.")
            is_valid = False
        if len(form_data['genre']) < 3:
            flash("genre must be at least 3 characters long.")
            is_valid = False

        return is_valid