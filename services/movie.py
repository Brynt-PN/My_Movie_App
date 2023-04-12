from models.movie import Movie as MovieModel
from schemas.movie import Movie as M

class MovieServices():
    
    def __init__(self, db) -> None:
        self.db = db

    def get_movie(self):
        result = self.db.query(MovieModel).all()
        return result
    
    def get_movie_id(self, id: int):
        result = self.db.query(MovieModel).filter(MovieModel.id == id).first()
        return result
    
    def get_movie_category(self, category):
        result = self.db.query(MovieModel).filter(MovieModel.category == category).all()
        return result
    
    def post_movie(self, movie: M):
        new_movie = MovieModel(**movie.dict())
        self.db.add(new_movie)
        self.db.commit()
        return

    def put_movie(self, id: int, movie: M):
        result = self.db.query(MovieModel).filter(MovieModel.id == id).first()
        result.title = movie.title
        result.overview = movie.overview
        result.year = movie.year
        result.rating = movie.rating
        result.category = movie.category
        self.db.commit()
        return 
    
    def delete_movie(self, id: int):
        result = self.db.query(MovieModel).filter(MovieModel.id == id).first()
        self.db.delete(result)
        self.db.commit()
        return