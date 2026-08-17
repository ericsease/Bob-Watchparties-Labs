from database import db


class Repo(db.Model):
    __tablename__ = "repos"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    owner = db.Column(db.String(80), nullable=False)
    description = db.Column(db.String(300), nullable=False)
    language = db.Column(db.String(40), nullable=False)
    stars = db.Column(db.Integer, default=0)
    url = db.Column(db.String(200), nullable=False)

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "owner": self.owner,
            "description": self.description,
            "language": self.language,
            "stars": self.stars,
            "url": self.url,
        }
