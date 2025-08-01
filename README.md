[![License](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](https://opensource.org/licenses/Apache-2.0) ![PyPI - Version](https://img.shields.io/pypi/v/async_obj)

# async_obj

A minimalist and lightweight Python wrapper to make any function -standalone or within an object- asynchronous.

If you are also tired of adding a whole bunch of code for every single case of simple threading, this small wrapper is my remedy. Requires >=Python 3.8.

`async obj` enables:
- Simply running a function in a dedicated thread.
- Check for completion of the function.
- Block until the function finishes.
- Receiving the returned result.
- In case of an exception, raising the exception on demand (whenever the result is requested).

Advantages:
- No compatibility concerns (e.g., `asyncio`), only depends on a few standard Python libraries.
- Essentially a 2 liner, no decorators or keywords.
- Mimics an object or a function and does not create a copy, hence minimum impact on memory and performance.

## Installation
Easiest way is to use `pip`, only requirement is Python >=3.8.

```bash
pip install async_obj
```

## Examples

- Run a function asynchronous and check for completion. Then collect the result.
```python
from async_obj import async_obj
from time import sleep

def dummy_func(x:int):
    sleep(3)
    return x * x

#define the async version of the dummy function
async_dummy = async_obj(dummy_func)

print("Starting async function...")
async_dummy(2)  # Run dummy_func asynchronously
print("Started.")

while True:
    print("Checking whether the async function is done...")
    if async_dummy.async_obj_is_done():
        print("Async function is done!")
        print("Result: ", async_dummy.async_obj_get_result(), " Expected Result: 4")
        break
    else:
        print("Async function is still running...")
        sleep(1)
```

---
- Alternatively, block until the function is completed, also retrieve any results.

```python
print("Starting async function...")
async_dummy(4)  # Run dummy_func asynchronously
print("Started.")
print("Blocking until the function finishes...")
result = async_dummy.async_obj_wait()
print("Function finished.")
print("Result: ", result, " Expected Result: 16")
```

---
- Raise propagated exceptions, whenever the result is requested either with `async_obj_get_result()` or with `async_obj_wait()`.

```python
print("Starting async function with an exception being expected...")
async_dummy(None) # pass an invalid argument to raise an exception
print("Started.")
print("Blocking until the function finishes...")
try:
    result = async_dummy.async_obj_wait()
except Exception as e:
    print("Function finished with an exception: ", str(e))
else:
    print("Function finished without an exception, which is unexpected.")
```
---
- Same functionalities are available for functions within class instances.
```python
class dummy_class:
    x = None

    def __init__(self):
        self.x = 5

    def dummy_func(self, y:int):
        sleep(3)
        return self.x * y

dummy_instance = dummy_class()
#define the async version of the dummy function within the dummy class instance
async_dummy = async_obj(dummy_instance)

print("Starting async function...")
async_dummy.dummy_func(4)  # Run dummy_func asynchronously
print("Started.")
print("Blocking until the function finishes...")
result = async_dummy.async_obj_wait()
print("Function finished.")
print("Result: ", result, " Expected Result: 20")
```

## To Do
1. Providing same concurrency functionalities for `getter`, `setter` and similar extension.
2. Improve autocompletion support for better IDE convenience.
