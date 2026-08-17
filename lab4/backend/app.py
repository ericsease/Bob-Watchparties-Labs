import os
from flask import Flask, jsonify
from flask_cors import CORS
from dotenv import load_dotenv

from database import db, init_db
from models import Repo
from seed import seed

load_dotenv()

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv(
    "DATABASE_URL", "sqlite:///reporadar.db"
)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

CORS(app)
init_db(app)

# Seed on first run
with app.app_context():
    seed(db, Repo)


# ---------------------------------------------------------------------------
# Routes
# ---------------------------------------------------------------------------

@app.route("/api/repos", methods=["GET"])
def get_repos():
    repos = Repo.query.order_by(Repo.stars.desc()).all()
    return jsonify([r.to_dict() for r in repos])


if __name__ == "__main__":
    app.run(debug=True, port=5000)
