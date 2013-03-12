
import yaml
import flask


with open('config.yaml') as f:
    config = yaml.load(f)

app = flask.Flask('quickbudget')

@app.teardown_request
def shutdown_seesion(exception=None):
    from quickbudget.db import db_session

    db_session.commit()
    db_session.remove()

from quickbudget import db, pages

db.init_db(config['database'])
pages.init_routing(app)

if __name__ == "__main__":
    host = config['host']
    debug = config['debug']
    
    app.run(host=host, debug=debug)