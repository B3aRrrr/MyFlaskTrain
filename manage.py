#!/usr/bin/env python
import os 
from flask_script import Manager,Shell
from flask_migrate import Migrate

from app import create_app,db
from app.models import User,Role

app = create_app(os.getenv("FLASK_CONFIG") or 'default')
manager = Manager(app)
migrate = Migrate(app, db, command='migrate')

def make_shell_context():
    return dict(app=app,db=db,User=User,Role=Role)

manager.add_command("shell",Shell(make_context=make_shell_context)) 

@manager.command
def test():
    """Запускает модульные тесты."""
    import unittest
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=2).run(tests)

if __name__ == "__main__":
    manager.run()