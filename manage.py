import os
from flask_script import Manager, Shell
from flask_migrate import Migrate, MigrateCommand
from seed_db import Seed
from app import app, db


app.config.from_object(os.environ['APP_SETTINGS'])

migrate = Migrate(app, db)
manager = Manager(app)

manager.add_command('db', MigrateCommand)
manager.add_command('seed', Seed())

if __name__ == '__main__':
    manager.run()
