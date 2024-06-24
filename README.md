# A4 – Minimal library for command-line applications.

The name comes from A4 paper.  It provides absolutely minimal (but not lousy)
support for command-line applications.

**A4** is [listed on PyPI](https://pypi.org/project/a4/).


## Simple logging

`a4.log` implements minimal logging with three major features which, in my
highly opinionated opinion, should be included in all logging libraries:

- Levels.
- Colors.
- Timestamps.

You may print all logs to stderr with `a4.log.fork=True` (default `False`).


## Yet another command-line application decorator

`a4.app` provides a decorator `Runnable` to convert a class into a runnable
command-line application. All class methods *NOT* starting with understore
are recognized as sub-commands. This pattern offers more convenience over
single-function decorators when multiple commands require shared resources.

```python
import a4
from a4.app import AppBase, Runnable

@Runnable
class MyApp(AppBase):
    def __init__(self):
        AppBase.__init__(self)

    def gen_calendar(self, args):
        """<yyyy> mmdd-mmdd [mmdd-mmdd ...]
        Generate trading calendar for one year.
        -c  <cal_id>   calendar ID, default 86
        """

        opts, args = a4.get_opts('c:', args)
        if len(args) < 2:
            self._die_usage()
        cal_id = int(opts['c'] or '86')
        self._log(f'calendar id = {cal_id}')


if __name__ == '__main__':
    MyApp().run()
```
