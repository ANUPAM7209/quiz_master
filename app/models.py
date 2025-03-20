from app import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)#create the user model make the user model inherit from the db.Model class translate the user table into the database
    username = db.Column(db.String(90), unique=True, nullable=False)
    password = db.Column(db.String(90), nullable=False)
    fullname = db.Column(db.String(90), nullable=False)
    qualification = db.Column(db.String, nullable=True)
    dob = db.Column(db.Date) #date of birth

    scores = db.relationship('Score', backref='user', lazy=True)# backref -> if u have the score object u can access the user object . if we dont have the backref we can't access the user object from the score object
    #lazy -> how the related object will be loaded. it must need to fetch all the records from the database. lazy=True -> fetch all the records from the database at once when we not need it . lazy=False -> fetch the records from the database when we need it.
    #db.model => tanslate the user model into the database table
    #db.session => query the database.
class Subject(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(90), nullable=False)
    description = db.Column(db.Text)

    chapters = db.relationship('Chapter', backref='subject', lazy=True)

class Chapter(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(90), nullable=False)
    description = db.Column(db.Text)
    subject_id = db.Column(db.Integer, db.ForeignKey('subject.id'), nullable=False)

    quizzes = db.relationship('Quiz', backref='chapter', lazy=True)

class Quiz(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date_of_quiz = db.Column(db.DateTime)
    time_duration = db.Column(db.Integer, nullable=False)
    chapter_id = db.Column(db.Integer, db.ForeignKey('chapter.id'), nullable=False)

    questions = db.relationship('Question', backref='quiz', lazy=True)

class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    question_statement = db.Column(db.Text, nullable=False)
    option1 = db.Column(db.String(180), nullable=False)
    option2 = db.Column(db.String(180), nullable=False)
    option3 = db.Column(db.String(180), nullable=False)
    option4 = db.Column(db.String(180), nullable=False)
    correct_option = db.Column(db.Integer, nullable=False)

    quiz_id = db.Column(db.Integer, db.ForeignKey("quiz.id"), nullable=False)

class Score(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    total_scored = db.Column(db.Integer, nullable=False)
    timestamp = db.Column(db.DateTime, default=db.func.current_timestamp())
    quiz_id = db.Column(db.Integer, db.ForeignKey('quiz.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

