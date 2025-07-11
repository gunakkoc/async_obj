# Copyright 2025 Gun Deniz Akkoc
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# https://github.com/gunakkoc/async_obj

import random
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


print("-------- Scenario 1: Check if the async function is done and collect the result.")
# Instead of calling x.some_func(2) which would block the main thread for 3 seconds,
# Run the function via async_obj
async_x.some_func(4) # Run the function here in
print("The function has been called asynchronously.")
# Do something else while waiting for the result
while True:
    print("Doing something else...")
    sleep(1)
    if async_x.async_obj_is_done():
        print("Finished with the result: ", async_x.async_obj_get_result())
        break

print("-------- Scenario 2: wait for async function to be done and collect the result.")
# Alternatively, use the wait function to block until the function is finished
async_x.some_func(5)
print("The function has been called asynchronously.")
result = async_x.async_obj_wait()
print("Finished with the result: ", result)

print("-------- Scenario 3: wait for async function to be done and catch the propagated exception.")
#Errors are also raised whenever the result is requested either through async_obj_get_result() or async_obj_wait().
async_x.some_func("a") #trigger an error with passing a string instead of an int
print("The function has been called asynchronously.")
try:
    result = async_x.async_obj_wait()
except Exception as e:
    print("An error occurred: ", e)

