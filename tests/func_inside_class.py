from async_obj import async_obj
from time import sleep

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
async_dummy.dummy_func(2)  # Run dummy_func asynchronously
print("Started.")

while True:
    print("Checking whether the async function is done...")
    if async_dummy.async_obj_is_done():
        print("Async function is done!")
        print("Result: ", async_dummy.async_obj_get_result(), " Expected Result: 10")
        break
    else:
        print("Async function is still running...")
        sleep(1)


print("Starting async function...")
async_dummy.dummy_func(4)  # Run dummy_func asynchronously
print("Started.")
print("Blocking until the function finishes...")
result = async_dummy.async_obj_wait()
print("Function finished.")
print("Result: ", result, " Expected Result: 20")


print("Starting async function with an exception being expected...")
async_dummy.dummy_func(None) # pass an invalid argument to raise an exception
print("Started.")
print("Blocking until the function finishes...")
try:
    result = async_dummy.async_obj_wait()
except Exception as e:
    print("Function finished with an exception as expected: ", str(e))
else:
    print("Function finished without an exception, which is unexpected.")
