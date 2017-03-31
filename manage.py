import os
from flask_script import Manager, Shell
from flask_migrate import Migrate, MigrateCommand
from app import app, db


app.config.from_object(os.environ['APP_SETTINGS'])

migrate = Migrate(app, db)
manager = Manager(app)

manager.add_command('db', MigrateCommand)
# manager.add_command("shell", Shell())

if __name__ == '__main__':
    manager.run()
