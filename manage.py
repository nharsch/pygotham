"""Management commands."""

from flask_migrate import MigrateCommand
from flask_script import Manager

from pygotham.factory import create_app
from pygotham.manage import CreateAdmin, CreateEvent, CreateUser

manager = Manager(create_app(__name__, ''))
manager.add_command('create_admin', CreateAdmin())
manager.add_command('create_event', CreateEvent())
manager.add_command('create_user', CreateUser())
manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()
