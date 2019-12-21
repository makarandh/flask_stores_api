from conf.init import initialize_apis, app
from sqlalchemy_db import db


if __name__ == "__main__":
    db.init_app(app)
    print("Initializing...")
    initialize_apis()
    print("Running Flask server...")
    app.run(host="0.0.0.0", port=8080, debug=True)
