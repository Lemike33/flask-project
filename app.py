from flask import Flask, render_template, url_for, request, redirect, session, make_response
from flask_sqlalchemy import SQLAlchemy
from datetime import date

app = Flask(__name__)  # create object 'app' on class Flask
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///job.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'a my great very secret key'  # use for session
db = SQLAlchemy(app)


class Job(db.Model):  # create Table Job
    id = db.Column(db.Integer, primary_key=True)
    company = db.Column(db.String(120), nullable=False)
    description = db.Column(db.Text, nullable=False)
    date_start = db.Column(db.Date, nullable=False)
    date_end = db.Column(db.Date, nullable=False)

    def __repr__(self):
        return '<Job %r>' % self.id


@app.route('/')  # decorator for routing url page
@app.route('/home')
def index():  # function for routing

    return render_template("index.html")
    # return "Total visits: {}".format(session.get('visits'))


@app.route('/about')
def about():  # function for routing
    jobs = Job.query.order_by(Job.date_start.desc()).all()
    count = db.session.query(Job).count()  # counter of row in table Job
    if 'visits' in session:  # counter for total visits  current page
        session['visits'] = session.get('visits') + 1
    else:
        session['visits'] = 1
    return render_template("about.html", jobs=jobs, count=count, visits=session.get('visits'))

@app.route('/about/clear')
def count_clear():  #
    session.pop('visits', None)  # удаление данных о посещениях
    return redirect('/about')


@app.route('/about/<int:id>')
def detail(id):  # function for routing
    job = Job.query.get(id)
    return render_template("about_detail.html", job=job)


@app.route('/create-job', methods=['POST', 'GET'])
def create_job():
    if request.method == 'POST':
        company = request.form['company']
        description = request.form['description']
        date_start = date.fromisoformat(request.form['date_start'])
        date_end = date.fromisoformat(request.form['date_end'])

        job = Job(company=company, description=description, date_start=date_start, date_end=date_end)

        try:
            db.session.add(job)
            db.session.commit()
            return redirect('/about')
        except:
            return 'Fault'

    else:
        return render_template("create-job.html")


@app.route('/about/<int:id>/del')
def job_delete(id):
    job = Job.query.get_or_404(id)

    try:
        db.session.delete(job)
        db.session.commit()
        return redirect('/about')
    except:
        return "При удалении произошла ошибка"


@app.route('/about/<int:id>/update', methods=['POST', 'GET'])
def post_update(id):
    job = Job.query.get(id)
    if request.method == "POST":
        job.company = request.form['company']
        job.description = request.form['description']
        job.date_start = date.fromisoformat(request.form['date_start'])
        job.date_end = date.fromisoformat(request.form['date_end'])

        try:
            db.session.commit()
            return redirect('/about')
        except:
            return "При редактировании статьи произошла ошибка"
    else:
        return render_template("job_update.html", job=job)


if __name__ == '__main__':  # start site in project directory
    app.run(debug=True)
