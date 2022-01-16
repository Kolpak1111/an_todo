from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Article(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title =db.Column(db.String(100), nullable=False)
    text = db.Column(db.Text, nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)
    re_title =db.Column(db.String(100))
    re_text = db.Column(db.Text)

    def __repr__(self):
        return '<Article %r>' % self.id


@app.route('/')
def index():
    articles = Article.query.order_by(Article.date.desc()).all()
    return render_template('index.html', articles=articles)


@app.route('/<int:id>')
def index_dtl(id):
    article = Article.query.get(id)
    return render_template('dtl_index.html', article=article)


@app.route('/<int:id>/delete')
def index_delete(id):
    article = Article.query.get_or_404(id)

    try:
        db.session.delete(article)
        db.session.commit()
        return redirect('/')
    except:
        return "ERROR"


@app.route('/<int:id>/update', methods=['POST', 'GET'])
def index_update(id):
    article = Article.query.get(id)
    if request.method == "POST":
        article.title = request.form['title']
        article.text = request.form['text']

        try:
           db.session.commit()
           return redirect('/')
        except:
            return 'ERROR'
    else:
        return render_template('index_update.html', article=article)


@app.route('/add_todo', methods=['POST', 'GET'])
def add_todo():
    if request.method == "POST":
        title = request.form['title']
        text = request.form['text']

        article = Article(title=title, text=text)

        try:
           db.session.add(article)
           db.session.commit()
           return redirect('/')
        except:
            return 'ERROR'
    else:
        return render_template('add_todo.html')


if __name__ == "__main__":
    app.run(debug=True)