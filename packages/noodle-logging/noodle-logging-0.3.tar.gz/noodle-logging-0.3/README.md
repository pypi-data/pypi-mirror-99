# Noodle Logging - The tiny JSON logger for Python 3.x

Noodle Logging is a tiny package aimed at making logging from python applications into JSON easier.


#### Dependencies
1. [structlog](https://github.com/hynek/structlog)
2. [python-json-logger](https://github.com/madzak/python-json-logger)
3. [six](https://github.com/benjaminp/six)


#### Installation

```pip3 install noodle-logging```

#### Usage Examples

##### 1. Basic logging

```python
from noodle_logging.logger import log

def test():
    log.info("event", some_parameter=12, some_other_parameter="hello")

if __name__ == "__main__":
    test()
```

###### Output
```json
{"message": "event", "some_parameter": 12, "some_other_parameter": "hello", "logger": "__main__", "level": "info", "timestamp": "2019-05-28T11:59:14.975823Z"}
```

##### 2. High level Profiling - Using decorators
```python
import time

from noodle_logging.decorators import profile

@profile
def some_method(*args, **kwargs):
    time.sleep(1)
    print(some_method.__name__, "method in execution with args ", args,
          " and kwargs ", kwargs)
    time.sleep(1)

if __name__ == "__main__":
    some_method(1, 2, 3, a=2, b=3)
```

###### Output
```
{"message": "Function Profiler", "fn_name": "some_method", "fn_id": "2df1335aa93f41438412da6b517a6781", "timestamp_start": 1559044955.3319192, "fn_args": "1,2,3", "fn_kwargs": "{\"a\": 2, \"b\": 3}", "logger": "noodle_logging.decorators", "level": "info", "timestamp": "2019-05-28T12:02:35.332396Z"}
>>> some_method method in execution with args  (1, 2, 3)  and kwargs  {'a': 2, 'b': 3}
{"message": "Function Profiler", "fn_name": "some_method", "fn_id": "2df1335aa93f41438412da6b517a6781", "timestamp_start": 1559044955.3319192, "fn_args": "1,2,3", "fn_kwargs": "{\"a\": 2, \"b\": 3}", "timestamp_end": 1559044957.340735, "exec_time": 2.0088157653808594, "logger": "noodle_logging.decorators", "level": "info", "timestamp": "2019-05-28T12:02:37.340991Z"}
```

##### 3. Catching (and Logging) an exception - Using decorators
```python
from noodle_logging.decorators import log_exceptions

@log_exceptions
def some_other_method(*args, **kwargs):
    print(some_other_method.__name__, "method in execution with args ",
          args, " and kwargs ", kwargs)
    print(1 / 0)
    # Below line will not be executed.
    print("Execution completed", some_other_method.__name__)

if __name__ == "__main__":
    some_other_method(1, 2, 3, a=2, b=3, c=4)
```

###### Output
```
some_other_method method in execution with args  (1, 2, 3)  and kwargs  {'a': 2, 'b': 3, 'c': 4}
{"message": "Exception Found.", "exception": "Traceback (most recent call last):\n  File \"/Users/askar.ali/Desktop/noodle-logging-original/noodle_logging/decorators.py\", line 48, in wrapper\n    return func(*args, **kwargs)\n  File \"run.py\", line 29, in some_other_method\n    print(1/0)\nZeroDivisionError: division by zero", "fn_args": "1,2,3", "fn_kwargs": "{\"a\": 2, \"b\": 3, \"c\": 4}", "logger": "noodle_logging.decorators", "level": "error", "timestamp": "2019-05-28T12:06:10.188581Z"}
Traceback (most recent call last):
  File "run.py", line 49, in <module>
    some_other_method(1, 2, 3, a=2, b=3, c=4)
  File "/Users/askar.ali/Desktop/noodle-logging-original/noodle_logging/decorators.py", line 48, in wrapper
    return func(*args, **kwargs)
  File "run.py", line 29, in some_other_method
    print(1/0)
ZeroDivisionError: division by zero
```

##### 4. Profiling + Catching (and Logging) exceptions - Using decorators
```python
from noodle_logging.decorators import profile, log_exceptions

@profile
@log_exceptions
def noodling_around(*args, **kwargs):
    print(noodling_around.__name__, "method in execution with args ",
          args, " and kwargs ", kwargs)
    print(1 / 0)
    # This line will not be executed.
    print("Execution completed", noodling_around.__name__)

if __name__ == "__main__":
    noodling_around(1, 2, 3, a=2, b=3, c=4)

```

###### Output
```
{"message": "Function Profiler", "fn_name": "noodling_around", "fn_id": "9a3e74924b77440c9a5f1fe4c05522e6", "timestamp_start": 1559045360.7205062, "fn_args": "1,2,3", "fn_kwargs": "{\"a\": 2, \"b\": 3, \"c\": 4}", "logger": "noodle_logging.decorators", "level": "info", "timestamp": "2019-05-28T12:09:20.720621Z"}
noodling_around method in execution with args  (1, 2, 3)  and kwargs  {'a': 2, 'b': 3, 'c': 4}
{"message": "Exception Found.", "exception": "Traceback (most recent call last):\n  File \"/Users/askar.ali/Desktop/noodle-logging-original/noodle_logging/decorators.py\", line 48, in wrapper\n    return func(*args, **kwargs)\n  File \"run.py\", line 41, in noodling_around\n    print(1 / 0)\nZeroDivisionError: division by zero", "fn_args": "1,2,3", "fn_kwargs": "{\"a\": 2, \"b\": 3, \"c\": 4}", "logger": "noodle_logging.decorators", "level": "error", "timestamp": "2019-05-28T12:09:20.721559Z"}
Traceback (most recent call last):
  File "run.py", line 50, in <module>
    noodling_around(1, 2, 3, a=2, b=3, c=4)
  File "/Users/askar.ali/Desktop/noodle-logging-original/noodle_logging/decorators.py", line 26, in wrapper
    result = func(*args, **kwargs)
  File "/Users/askar.ali/Desktop/noodle-logging-original/noodle_logging/decorators.py", line 48, in wrapper
    return func(*args, **kwargs)
  File "run.py", line 41, in noodling_around
    print(1 / 0)
ZeroDivisionError: division by zero
```
