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
        self.vote_count = db_data['vote_count']
        self.creator = None

    @classmethod
    def get_all(cls):
        query = """
                SELECT * FROM animes
                """
        results = connectToMySQL(db).query_db(query)
        print('results',results)
        animes = []
        for key in results:
            animes.append(cls(key))
            print('animes',animes)
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
                "password": '',
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
    def update(cls,form_data):
        query = """
                UPDATE anime_schema.animes set vote_count = vote_count + 1 
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
    
    @classmethod
    def get_top_ten(cls):
        query ="""
                select name, vote_count
                group by vote_count
                order by desc
                limit 10;
                """
        return connectToMySQL(db).query_db(query)

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
    
