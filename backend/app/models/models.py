from app import db

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    collections = db.relationship('Collection', backref='user', lazy=True)

    def __repr__(self):
        return f'<User {self.username}>'


class Collection(db.Model):
    __tablename__ = 'collections'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    description = db.Column(db.Text)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    videos = db.relationship('Video', backref='collection', lazy=True)

    def __repr__(self):
        return f'<Collection {self.name}>'


class Video(db.Model):
    __tablename__ = 'videos'
    id = db.Column(db.Integer, primary_key=True)
    youtube_id = db.Column(db.String(32), unique=True, nullable=False)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    collection_id = db.Column(db.Integer, db.ForeignKey('collections.id'), nullable=False)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    transcripts = db.relationship('Transcript', backref='video', lazy=True)

    def __repr__(self):
        return f'<Video {self.youtube_id}>'


class Transcript(db.Model):
    __tablename__ = 'transcripts'
    id = db.Column(db.Integer, primary_key=True)
    video_id = db.Column(db.Integer, db.ForeignKey('videos.id'), nullable=False)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, server_default=db.func.now())

    def __repr__(self):
        return f'<Transcript Video ID {self.video_id}, Language {self.language}>'

