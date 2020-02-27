"""
**Tomatic** is a library that helps add automatic setup capabilities
on **Python** programs and avoids that configuration files became
bloated with unnecessary lines of code. It has originally designed to
be used in [Django](https://www.djangoproject.com/) projects working
directly in `settings.py` but can be used with any other **Python**
program.

Buckets are simple interfaces for KEY/VALUE repositories.

## Buckets

Buckets are simple interfaces for KEY/VALUE repositories that only
handle with two specific tasks:

1. Where KEY/VALUE pairs are stored.
2. How to retrieve them.

**Tomatic** comes with two buckets by default:

* `DummyBucket` : It's a test purpose bucket and to be use for
  make sure that your changes didn't break your code. A _dummy_ bucket
  returns `None` VALUE for any KEY.
* `EnvironBucket` : It's a bucket that uses operating system
  environment variables to store KEY/VALUE data. Create variables
  using `«profile»__«key»=«value` syntax and this bucket will find them.]

---

# How to use

## Tomatic setup

Load **Tomatic** module and bucket class that you want to use in
your code:

``` python
from tomatic import Tomatic
from tomatic.buckets import EnvironBucket
```

Create a **Tomatic** instance with your settings:

``` python
t = Tomatic(EnvironBucket, static_profile="HOMOLOG")
```

A _profile_ is a name that identifies which set of data you going to
use, it's like a directory on a file system.

You can turn _profile_ selection dynamic using `env_profile`
instead of  `static_profile`.

```python
t = Tomatic(EnvironBucket, env_profile="CURRENT_PROFILE")
```

In this case **Tomatic** will get profile name direct from a environment variable set in operating system:

``` shell
export CURRENT_PROFILE="HOMOLOG"
```

## Setting up KEY/VALUE pairs

When using`EnvironBucket` you need to create your KEY/VALUE pairs using the following syntax:

``` shell
export HOMOLOG__API_HOST='127.16.20.13'
export HOMOLOG__ITEMS_PER_PAGE='50'
export HOMOLOG__DEBUG='true'
```

## Using data

To set KEYS in your program, use:

``` python
API = "http://{host}/api/v1".format(t.API_HOST or "localhost")
```

The use of `or` statement is optional but it works providing a default
value when KEY doesn't have a VALUE. So, if
`HOMOLOG__API_HOST` there isn't defined, "localhost" is used.

### Forcing data types

For **Python**, environment variables are always _strings_, but you can force
a specific data type conversion adding `__«type»__` as a suffix.

To force `ITEMS_PER_PAGE`to be an integer instead of a string, use:

``` python
ITEMS_PER_PAGE = t.ITEMS_PER_PAGE__int__ or 15
```

There are currently supported types:

* Boolean (`__bool__`)
* Floating Point (`__float__`)
* Integer (`__int__`)
* JSON (`__json__`)
* String* (`__str__`).

(*) Default data type and can be omited.

**Code example:**

KEYS set as in operating system for `EnvironBucket` use:

``` shell
HOMOLOG__HOSTNAME="192.168.0.200"
HOMOLOG__MAX_RESULTS=200
HOMOLOG__DEBUG=false
HOMOLOG__HEALTH_CHECK='{"DISK_USAGE_MAX":80,"MEMORY_MIN":200}'
```

**Python** code configured to properly handle with these KEYS:

``` python
from tomatic import Tomaic, fix
from tomatic.buckets import EnvironBucket

t = Tomatic(EnvironBucket, static_profile="HOMOLOG")
...
HOSTNAME = t.HOSTNAME__str__ or "localhost"
MAX_RESULTS = t.MAX_RESULTS__int__ or 10
DEBUG = t.fix(l.DEBUG__bool__, False)

HEALTH_CHECK = t.HEALTH_CHECK__json__ or {
    "DISK_USAGE_MAX": 90,
    "MEMORY_MIN": 100,
}
```

### Handling with empty values

In **Python** a `False or True` comparison results `True`, and the same
will happen with `0 or 1`, `"" or "some name"` etc... To avoid this behavior
and force use of the first value even empty, use `fix(«tomatic value»,«default value»)`function...

``` python
from tomatic import Tomatic, fix
...
DEBUG = fix(t.DEBUG, True)
```

This forces VALUE that came from **Tomatic** use even when it's empty and
default value use only when`None` is returned.
"""
from .core import Tomatic
from .tools import fix

__version__ = "0.2"

