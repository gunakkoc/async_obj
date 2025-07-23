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


print("Starting async function...")
async_dummy(4)  # Run dummy_func asynchronously
print("Started.")
print("Blocking until the function finishes...")
result = async_dummy.async_obj_wait()
print("Function finished.")
print("Result: ", result, " Expected Result: 16")


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

