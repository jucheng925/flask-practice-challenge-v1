from config import app, api, db
from models import Post, Comment
from sqlalchemy import func
from flask_restful import Resource

# create routes here:

# Challenge 1
class SortedPosts(Resource):
    def get(self):
        #ascending order (A->Z)
        posts = Post.query.order_by(Post.title).all()

        # descending order (Z => A)
        # posts = Post.query.order_by(Post.title.desc()).all()
        posts_dict = [post.to_dict() for post in posts]

        return posts_dict, 200

api.add_resource(SortedPosts, '/api/sorted_posts')

# Challenge 2
class PostsByAuthor(Resource):
    def get(self, author_name):

        # case insensitive
        posts = Post.query.filter(func.lower(Post.author) == func.lower(author_name)).all()
        
        # Strict case equality
        # posts = Post.query.filter_by(author = author_name).all()
        posts_dict = [post.to_dict() for post in posts]

        return posts_dict, 200

api.add_resource(PostsByAuthor, '/api/posts_by_author/<author_name>')

# Challenge 3
class SearchPostsByTitle(Resource):
    def get(self, title):
        # case insensitive and contains the titleword
        posts = Post.query.filter(Post.title.ilike(f'%{title}%')).all()

        posts_dict = [post.to_dict() for post in posts]

        return posts_dict, 200

api.add_resource(SearchPostsByTitle, '/api/search_posts/<title>')

# Challenge 4
class PostsOrderedByComments(Resource):
    def get(self):

        # Works but not the proper way, will give a warning
        # posts = Post.query.order_by(db.session.query(func.count(Post.comments))).all()
        
        # Joining the two models together
        query = db.session.query(Post).join(Comment)

        posts = query.group_by(Post).order_by(func.count(Comment.id).desc()).all()

        posts_dict = [post.to_dict() for post in posts]

        return posts_dict, 200

api.add_resource(PostsOrderedByComments, '/api/posts_ordered_by_comments')

# Challenge 5
class MostPopularCommenter(Resource):
    def get(self):
        comments = Comment.query.all()
        commenters_dict = {}
        for comment in comments:
            if comment.commenter in commenters_dict:
                commenters_dict[comment.commenter] += 1
            else:
                commenters_dict[comment.commenter] = 1
        
        most_popular_commenter = max(commenters_dict, key=lambda x: commenters_dict[x])

        response = {'commenter' : most_popular_commenter}
        return response, 200


api.add_resource(MostPopularCommenter, '/api/most_popular_commenter')

class PostByCommenter(Resource):
    def get(self, commenter):

        # LONG WAY - both still works
        # posts = Post.query.all()
        # posts_by_commenter = []
        # for post in posts:
        #     comments = Comment.query.filter(Comment.post_id == post.id, Comment.commenter == commenter).all()
        #     if comments:
        #         posts_by_commenter.append(post)

        # resp = [post.to_dict() for post in posts_by_commenter]
        # return resp, 200
        

        # Using db.session.query and join method - shorter way
        query = db.session.query(Post).join(Comment).filter(Comment.commenter == commenter).all()
        resp = [post.to_dict() for post in query]
        return resp, 200

api.add_resource(PostByCommenter, '/api/post_by_commenter/<commenter>')


if __name__ == "__main__":
  app.run(port=5555, debug=True)