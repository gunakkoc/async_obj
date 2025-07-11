[![License](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)

# async_obj

A minimalist and lightweight Python wrapper to make any function -standalone or within an object- asynchronous.

If you are also tired of adding a whole bunch of code for every single case of simple threading, this small wrapper is my remedy. Requires >=Python 3.8.

`async obj` enables:
- Simply running a function in a dedicated thread.
- Ability to check whether its completed (or wait for completion) at any point.
- Receiving the returned result.
- In case of an exception, raising the exception on demand (whenever the result is requested).

Advantages:
- No compatibility concerns (e.g., `asyncio`), only depends on a few standard Python libraries.
- Simple to use with basically 2 lines of code without any decorators.
- Mimics an object or a function and does not create a copy, hence minimum impact on memory and performance.

## Minimal Example
```python
from time import sleep
from async_obj import async_obj

class my_obj(): #a dummy class for demo
    def __init__(self):
        pass
    def some_func(self, val):
        sleep(3) # Simulate some long function
        return val*val

x = my_obj()
async_x = async_obj(x) #create a virtual async version of the object x

async_x.some_func(2) # Run the original function but through the async_obj
done = async_x.async_obj_is_done() # Check if the function is done
result = async_x.async_obj_get_result() # Get the result or raise any encountered error, if the function is done
# OR
async_x.some_func(3) # Run the original function but through the async_obj
result = async_x.async_obj_wait() # Block until the function finishes and get the result or raise any encountered error

# Same functionalities are also available when wrapping a function directly
async_sleep = async_obj(sleep) #create an async version of the sleep function
async_sleep(3)
```

## Simple Demos

```python
from time import sleep
from async_obj import async_obj

class my_obj():
    def __init__(self):
        pass
    def some_func(self, val):
        sleep(3) # Simulate some long function
        return val*val

x = my_obj()
async_x = async_obj(x) #create a virtual async version of the object x

print("-------- Scenario 1: Check if the async function within the object is done and collect the result.")
# Instead of calling x.some_func(2) which would block the main thread for 3 seconds,
# Run the function via async_obj
async_x.some_func(4) # Run the function here in
print("The function has been called asynchronously.")
# Do something else while waiting for the result
while True:
    print("Doing something else...")
    sleep(1)
    if async_x.async_obj_is_done():
        result = async_x.async_obj_get_result() # can be called only once, then the result is cleared
        print("Finished with the result: ", result)
        break

print("-------- Scenario 2: wait for async function within the object to be done and collect the result.")
# Alternatively, use the wait function to block until the function is finished
async_x.some_func(5)
print("The function has been called asynchronously.")
result = async_x.async_obj_wait()
print("Finished with the result: ", result)

print("-------- Scenario 3: wait for async function within the object to be done and catch the propagated exception.")
#Errors are also raised whenever the result is requested either through async_obj_get_result() or async_obj_wait().
async_x.some_func("a") #trigger an error with passing a string instead of an int
print("The function has been called asynchronously.")
try:
    result = async_x.async_obj_wait()
except Exception as e:
    print("An error occurred: ", e)


print("-------- Scenario 4: Call a function directly (not within an object) and asynchronously with async_obj.")
def another_func(val1, val2):
    sleep(3) # Simulate some long function
    print(val1*val2)

async_func = async_obj(another_func) #create a virtual async version of the function
async_func(3, 4)
print("The function has been called asynchronously.")
while True:
    print("Doing something else...")
    sleep(1)
    if async_func.async_obj_is_done():
        result = async_func.async_obj_get_result() # can be called only once, then the result is cleared
        print("Finished with the result: ", result)
        break

print("-------- Scenario 5: Call print function asynchronously.")
async_print = async_obj(print) #create a virtual async version of the function
print("Print function has been called asynchronously.")
async_print("Hello World")
async_print.async_obj_wait() #wait for the print function to finish
print("Finished")

print("-------- Scenario 6: Call sleep function asynchronously.")
async_sleep = async_obj(sleep) #create a virtual async version of the function
async_sleep(3)
print("Sleep function has been called asynchronously.")
while True:
    print("Doing something else...")
    sleep(1)
    if async_sleep.async_obj_is_done():
        print("Finished")
        break
```

## To Be Developed
1. Providing same concurrency functionalities for `getter`, `setter` and similar extension.
2. Better support to autocompletion for IDE convenience.

