#!python

# import and intialize Flask
from flask import Flask, Response
app = Flask(__name__)

# import and initialize Sommelier
from src.sommelier import Sommelier
sommelier = Sommelier()

@app.route('/')
def sommelier_index():
    response_body, keyed_args_dict = sommelier.index()
    return Response(response_body, **keyed_args_dict)

@app.route('/wines', defaults = {'page_num': 1}, methods = ['GET'])
@app.route('/wines/<int:page_num>', methods = ['GET'])
def sommelier_wines(page_num):
    response_body, keyed_args_dict = sommelier.wine_page(page_num)
    return Response(response_body, **keyed_args_dict)

@app.route('/wine/<wine_id>', methods = ['GET'])
def sommelier_wine(wine_id):
    response_body, keyed_args_dict = sommelier.wine(wine_id)
    return Response(response_body, **keyed_args_dict)

@app.route('/authors', defaults = {'page_num': 1}, methods = ['GET'])
@app.route('/authors/<int:page_num>', methods = ['GET'])
def sommelier_authors(page_num):
    response_body, keyed_args_dict = sommelier.author_page(page_num)
    return Response(response_body, **keyed_args_dict)

@app.route('/author/<author_id>', methods = ['GET'])
def sommelier_author(author_id):
    response_body, keyed_args_dict = sommelier.author(author_id)
    return Response(response_body, **keyed_args_dict)

if __name__ == '__main__':
    app.run(debug=True)

