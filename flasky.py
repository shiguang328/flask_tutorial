import os

COV = None
if os.environ.get('FLASK_COVERAGE'):
    import coverage
    # branch选项用于开启分支覆盖，检查每个添加语句的True和False分支是否执行;
    # include选项用于过滤分析范围，不指定将覆盖所有代码，给测试添加很多杂项
    COV = coverage.coverage(branch=True, include='app/*')
    COV.start()

import sys
import click
from flask_migrate import Migrate, MigrateCommand
from app import create_app, db
from app.models import User, Follow, Role, Permission, Post, Comment

app = create_app(os.getenv('FLASK_CONFIG') or 'default')
from flask_script import Manager, Shell
manager = Manager(app, db)
migrate = Migrate(app, db)


@app.shell_context_processor
def make_shell_context():
    return dict(db=db, User=User, Follow=Follow, Role=Role,
                Permission=Permission, Post=Post, Comment=Comment)
manager.add_command('shell', Shell(make_context=make_shell_context))
manager.add_command('db', MigrateCommand)


# @app.cli.command()
# @click.option('--coverage/--no-coverage', default=False,
#               help='Run tests under code coverage.')
@manager.command
def test():
    """Run the unit tests."""
    # if coverage and not os.environ.get('FLASK_COVERAGE'):
    #     import subprocess
    #     os.environ['FLASK_COVERAGE'] = '1'
    #     sys.exit(subprocess.call(sys.argv))

    import unittest
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=2).run(tests)
    if COV:
        COV.stop()
        COV.save()
        print('Coverage Summary:')
        COV.report()
        basedir = os.path.abspath(os.path.dirname(__file__))
        covdir = os.path.join(basedir, 'tmp/coverage')
        COV.html_report(directory=covdir)
        print('HTML version: file://%s/index.html' % covdir)
        COV.erase()


if __name__ == '__main__':
    manager.run()
    # test()