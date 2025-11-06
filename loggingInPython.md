# Logging In Python
## Logging - Logging Facility In Python
- simple examplel
```py
import logging
logger = logging.getLogger(__name__)
logger.info(<log>)
# INFO: __main__: <log>
```
- this enables modules to create & use module level loggers
- standard logging library is implemented in hierarchical manner
    - logs are delivered to higher level log handlers
    - highest level logger is known as "root logger"
    - this enables down stream control from high level code over logs
- standard logging library is composed of
    1. `Logger`s: used by application code for logging
    2. `Handler`s: used to send log records to appropriate destinations
    3. `Filter`s: used to determine which log records to output
    4. `Formatter`s:
        - used to specify layout of log records 
        - reponsible for converting `logging.LogRecord` objects to strings
### Logger Objects
- should never be instantiated directly
- `class logging.Logger`
    - `level`
        - defaults to "NOTSET" if self isn't the root logger & to "WARNING" otherwise
        - "NOTSET" will cause all events to delegate to parent loggers
        - if set as "NOTSET", events less sever than it will be ignored
    - `propagate` (if `True`)
        - defaults to `True` by `logging.getLogger`
        - events will be passed to handlers of ancestor loggers after being handled by handlers of self
        - this will continue until one of the loggers has propagate set as `False`
        - it is encouraged to attach handlers once at the highest level possible to avoid duplicates
    - `handlers`
        - `logging.addHandler`
        - `logging.removeHandler`
        - `logging.hasHandlers`
    - `logging.Logger.setLevel`: used to set or change `level` of self
    - `debug`, `info`, `warning`, `error` & `critical`
        - used to log with corresponding levels
        - msg is format string using `%` syntax
        - `args` & `kwargs` can be used in order to fill place holders
        - `exc_info`, `stack_info`, `stacklevel` & `extra` are special keyword arguments
    - `log`: used to log at given level
    - `exception`
        - used to log at "debug" level with added information of raised exception
        - should be called inside exception handlers
    - `filters`
        - `logging.addFilter`
        - `logging.removeFilter`
    - `filter`
        - used to apply filters of self on given record
        - returns `True` if record should be processed
        - all filters all called until one of them returns `False`
        - otherwise the record will be passed to handlers
    - `handle`
        - used to handle given record by passing it to all handlers of self & its ancestors
        - passing to ancestors stops when `False` value of propagate is found
#### Logging Levels
|level|numeric value|desc|
|-|-|-|
|DEBUG|10|detailed information, usually for developers|
|INFO|20|confirmation for as expected behaviour|
|WARNING|30|indication for unexpected behaviour or near future problem while application is still safe|
|ERROR|40|indication for problems causing application to not behave as expected|
|ERROR|50|indication for problems that cause application to stop running|
### Module Level Functions
- `logging.getLogger`
    - returns logger with specified name if name is given, otherwise the root logger
    - calls to with same name will return reference to the same logger
    - name is usually dot separated & corresponds to the current logging hierarchy
- `logging.{debug,info,warning,error,critical,log,exception}`: wrappers for methods of root logger