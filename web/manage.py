# manage.py

import subprocess
import sys
import unittest

import coverage
from flask.cli import FlaskGroup

from web.domain import create_app, db

app = create_app()
cli = FlaskGroup(create_app=create_app)

# code coverage
COV = coverage.coverage(
    branch=True,
    include="web/*",
    omit=["web/tests/*", "web/domain/config.py", "web/domain/*/__init__.py"],
)
COV.start()


@cli.command()
def create_db():
    db.drop_all()
    db.create_all()
    db.session.commit()


@cli.command()
def drop_db():
    """Drops the db tables."""
    db.drop_all()


@cli.command()
def create_admin():
    """Creates the admin user."""
    pass
    # db.session.add(User(email="ad@min.com", password="admin", admin=True))
    # db.session.commit()


@cli.command()
def create_data():
    """Creates sample data."""
    pass


@cli.command()
def test_unitest():
    """Runs the unit tests without test coverage."""
    tests = unittest.TestLoader().discover("web/tests", pattern="test*.py")
    result = unittest.TextTestRunner(verbosity=2).run(tests)
    if result.wasSuccessful():
        sys.exit(0)
    else:
        sys.exit(1)


@cli.command()
def test_pytest_with_plugins():
    """Runs pytest with plugins on the web."""
    subprocess.run(["pytest", "--ignore=migrations", "--black", "--isort", "--flakes"])


@cli.command()
def test_pytest():
    """Runs pytest on the web."""
    subprocess.run(["pytest"])


@cli.command()
def cov():
    """Runs the unit tests with coverage."""
    tests = unittest.TestLoader().discover("web/tests")
    result = unittest.TextTestRunner(verbosity=2).run(tests)
    if result.wasSuccessful():
        COV.stop()
        COV.save()
        print("Coverage Summary:")
        COV.report()
        COV.html_report()
        COV.erase()
        sys.exit(0)
    else:
        sys.exit(1)


if __name__ == "__main__":
    cli()
