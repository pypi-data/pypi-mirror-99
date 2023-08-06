# PIP URL
https://pypi.org/manage/project/pangu-task/releases/

# Description
It's a pip package which decorate method to have route or sync features.

# How to 
## sync task
```python
import time

from pangu_task import task


def init():
    print('init event!')


def callback():
    print('callback event!')


@task(init=init, callback=callback)
def click1(a, b):
    print("click1 function with ({0},{1}) start".format(a, b))
    i = 0
    while i < 10:
        print("click1 is running: {0}".format(i))
        i = i + 1
        time.sleep(1)
    print("click1 function with ({0},{1}) finished".format(a, b))
    

print("click1 is starting")
click1.delay(1, 2)
print("all done")
```

## router
```python
from pangu_task import Route


route = Route('/task')


def callback():
    print('callback finished')

@route(callback=callback)
def click1():
    print("click1 function")
```

```bash
curl http://your_host/task/click1
```
