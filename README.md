![Tomatic logo](tomatic_logo.png)

**Tomatic** is a library that helps add automatic setup capabilities on **Python** programs and avoids that configuration files became bloated with unnecessary lines of code. It has originally designed to be used in [Django](https://www.djangoproject.com/) projects working directly in `settings.py` but can be used with any other Python program.


Requirements
--
Requires at least **Python 3.6** due use of type hints ([PEP484](https://www.python.org/dev/peps/pep-0484/)).

Installing
--
Use `pip` to install **Tomatic**, running:

``` shell
pip install tomatic
```

Or you can clone or download this repository for manual install.

Using
--

Let's get an simple use handling with [PortgeSQL](https://www.postgresql.org/) database configuration on a **Django** project...

**You have two setups and one problem...**

One for local development using a local instance of **PostgreSQL**:

``` python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'app_database',
        'USER': 'app_user',
        'PASSWORD': '12345',
        'HOST': 'localhost',
        'PORT': '',
    }
}
```

And, for **QA**, that uses a different setup on another database server:


``` python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'mastercontrol_qa',
        'USER': 'mc_app_user',
        'PASSWORD': '53f2c97dfbf533411874a0f2f551ee9c',
        'HOST': '172,16.20.13',
        'PORT': 5432,
    }
}
```

There are so many ways to handle with this like you can keep two or more copies of `settings.py`, setup two databases on it, use an environment variables etc... But in all cases you will need to stop development to it.

**Solving the problem with Tomatic**

By the way, this example is using `EnvironBucket` , and it works using environment variables to store KEY/VALUE pairs.

Firstly, add it into `settings.py`:

``` python
from tomatic import Tomatic
from tomatic.buckets import EnvironBucket

t = Tomatic(EnvironBucket, env_profile="TARGET")
```
Then setup database using both KEYS from **Tomatic** and your development settings:

``` python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': t.DB_NAME or 'app_database',
        'USER': t.DB_USER or 'app_user',
        'PASSWORD': t.DB_PASSWD or '12345',
        'HOST': t.DB_HOST or 'localhost',
        'PORT': t.DB_PORT or '',
    }
}
```

Here, if KEY isn't set (or empty) the language will automatically try the value that follows on expression.

The, you need to create a file containing values used to connect in **QA** database server:

``` shell
# .qa-env
QA__DB_NAME='mastercontrol_qa'
QA__DB_USER='mc_app_user'
QA__DB_PASSWD='53f2c97dfbf533411874a0f2f551ee9c'
QA__DB_HOST='172.16.20.13'
QA__DB_PORT='9876'

export QA__DB_NAME QA__DB_USER QA__DB_PASSWD QA__DB_HOST QA__DB_PORT
```

**Runing your Django application**

Now, to run your application for local development just run:

``` shell
python ./manage.py runserver
```

But, for do the same using **QA** settings, run:

``` shell
source .qa-env
```
To load environment variables (only needed at first time) and...

``` shell
TARGET=QA python ./manage.py runserver
```

The **TARGET** value is used by **Tomatic** to build the name of environment variables used to setup `DATABASES` dictionary of `setting.py` file. If value isn't set **Tomatic** return `None` and value that follows in expression is used.

Tips
--
1. You can enforce **Tomatic**  to doesn't accept `None` values adding `raise_if_none` argument:

    ``` python
    from django.core.exceptions import ImproperlyConfigured 

    from tomatic import Tomatic
    t = Tomatic(
        EnvironBucket,
        env_profile="TARGET",
        raise_if_none=ImproperlyConfigured
        )            
    ```
	So, if a KEY returns an empty value, `ImproperlyConfigured` exception will be raised.
	
2. You can remove sensitive data from `settings.py` file and put them as system variables as a static profile:
	``` python    
    t = Tomatic(
        EnvironBucket,
        static_profile="DEFAULT",
        raise_if_none=ImproperlyConfigured
        )
	```
	And access them by environment variables starting with `DEFAULT__` prefix.

3. Environment variables on **Python** are always strings but is possible to force data type conversion by adding a type suffix when getting values:

    * `__bool__` to convert VALUE to boolean
    
    * `__float__` to convert VALUE to floating point;
    
    * `__int__` to convert VALUE to integer;
    
    * `__json__` to convert VALUE to dictionary (or a list) and
    
    * `__str__` to convert VALUE to string (default behavior).
    
	Few examples:

  | Environment variable | Data type forced | Result |
  | --------------------- | ------------------ | ------ |
  | `DEFAULT__DEBUG='true`' | `t.DEBUG__bool__`  | `True` |
  | `DEFAULT__LOWEST_PRICE='49.90'` | `t.LOWEST_PRICE__float__` | `49.9` |
  | `DEFAULT__PAGE_LIMIT='10'` | `t.PAGE_LIMIT__int__ `| `10` |
  | `DEFAULT__ALLOWED_HOSTS='["127.0.0.1", "192.168."]'` | `t.ALLOWED_HOSTS__json__` | `["127.0.0.1", "192.168.",]` |

---
And for more details, please, read the [full documentation](https://plainspooky.github.io/tomatic/index.html).
