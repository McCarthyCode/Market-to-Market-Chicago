# Market to Market Chicago

## Installation (Debian-based systems)

Make sure `python3` and `pip3` are installed on your system and install `virtualenv`.

    $ sudo apt install -y python3 python3-pip && pip3 install virtualenv

`virtualenv`'s default installation directory is `$HOME/.local/bin`. Add it to your `PATH` if it is not already there.

    $ echo "export PATH=$PATH:$HOME/.local/bin" >> ~/.bashrc && source ~/.bashrc

In the project's root directory, run the following to create a new virtual environment.

    $ virtualenv -p python3 .env

Activate the newly created environment.

    $ source env/bin/activate

At any point within the virtual environment, run `deactivate` to deactivate.

    (env) $ deactivate

Go back to the virtual environment and install project dependencies.

    (env) $ pip install -r requirements.txt

Generate a secret key and pipe the output to a file. Change the newly created file's permissions to `rw-------`, or `0600`. Note that you will need to add the file to `.gitignore` if you keep it somewhere other than `$BASE_DIR/auth`. Also, your directory structure will likely differ from the one used by `SECRET_KEY_FILE` in `mtm/settings.py`. Change the path to `secret.txt` in `SECRET_KEY_FILE` in `mtm/settings.py` to match your system's directory structure.

    $ mkdir auth
    $ python bin/generate_secret_key.py > auth/secret.txt
    $ sudo chmod 0600 auth/secret.txt

Alternatively, export it as an environment variable and edit `mtm/settings.py` to read the string that way.

    $ export SECRET_KEY=$(python bin/generate_secret_key.py)

In `settings.py`, change

    HOME = os.environ.get('HOME')
    SECRET_KEY_FILE = '%s/mtm/auth/secret.txt' % HOME
    with open(SECRET_KEY_FILE, 'r', encoding='utf8') as f:
        content = f.readline()
    SECRET_KEY = content

to

    SECRET_KEY = os.environ.get('SECRET_KEY')

No method is more secure than the other as an attacker can access the key both ways if they gain access to the system running the project.

Make and apply migrations.

    (env) $ python manage.py makemigrations
    (env) $ python manage.py migrate

## Running

### Development Mode

To run in development mode, activate the virtual environment and execute the following:

    (env) $ python manage.py runserver localhost:8000

### Production Mode

To run in production mode, follow [these steps](https://www.digitalocean.com/community/tutorials/how-to-set-up-django-with-postgres-nginx-and-gunicorn-on-ubuntu-18-04) after choosing your distribution.
