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

import threading
from queue import Queue
import sys
import logging

class async_obj():
    __async_obj_sub_obj__:any = None
    __async_obj_worker_thread__:threading.Thread = None
    __async_obj_target_callable__:callable = None
    __async_obj_response__:any = None
    __async_obj_thread_id__:int = None
    __async_obj_thread_result_queue__:Queue = None
    
    def __init__(self,sub_obj):
        """
        Parameters
        ----------
        sub_obj : Any object whose functions to be run in a thread
            Runs ANY function of an object in a thread.
            The completion can be checked via async_obj_is_done() function
            The result of the last async call can be obtained via async_obj_get_result() function.
            Can wait for the completion via async_obj_wait() function which also returns the result of the last async call.

        Returns
        -------
        any
            the async version of the original object.
        """
        if sys.version_info < (3, 8):
            raise RuntimeError("async_obj requires Python 3.8 or higher.")
        self.__async_obj_thread_result_queue__ = Queue()
        self.__async_obj_sub_obj__ = sub_obj
        
    def async_obj_is_done(self):
        """
        Checks if the thread is finished.

        Returns
        -------
        bool
            True if the thread is finished or not started, False otherwise.
        """
        try:
            if self.__async_obj_worker_thread__ is None:
                return True
            if not self.__async_obj_worker_thread__.is_alive():
                return True
        except:
            return True
        return False
    
    def async_obj_get_result(self):
        """
        Returns the result of the last async call.
        If the thread is not finished, it returns None.
        If the thread is finished but the result is not registered, it returns None.
        In case of an error, raises the error here.

        Returns
        -------
        any
            The result of the last async call if the thread is finished.
            If the thread is not finished, returns None.
            
        Raises
        ------
        Exception
            Any error when calling the function of the original object.
        """
        if self.async_obj_is_done() and not self.__async_obj_thread_result_queue__.empty():
            while not self.__async_obj_thread_result_queue__.empty():
                    native_id, result, err = self.__async_obj_thread_result_queue__.get()
                    if native_id == self.__async_obj_thread_id__:
                        while not self.__async_obj_thread_result_queue__.empty(): #clear the queue before returning
                            self.__async_obj_thread_result_queue__.get()
                        if err is not None:
                            raise err
                        else:
                            return result
            logging.warning("The function {func} seems to be finished but the result is not registered. Returning None.".format(func=str(self.__async_obj_target_callable__)))
            return None
        else:
            return None
    
    def async_obj_wait(self,timeout:float=None):
        """
        Waits until the thread is exited.
        
        Parameters
        ----------
        timeout : float, optional
            Time to wait in seconds. The default is None, corresponds to infinite.

        Returns
        -------
        any
            The result of the last async call if the thread is finished,
            otherwise returns None.
        """
        if self.async_obj_is_done():
            return self.async_obj_get_result()
        if timeout is None:
            self.__async_obj_worker_thread__.join()
        else:
            self.__async_obj_worker_thread__.join(timeout)
        return self.async_obj_get_result()
        
    def __async_obj_thread_func__(self,*args,**kwargs):
        try:
            result = self.__async_obj_target_callable__(*args,**kwargs)
            self.__async_obj_thread_result_queue__.put((threading.get_native_id(),result,None))
        except Exception as e:
            self.__async_obj_thread_result_queue__.put((threading.get_native_id(),None,e))

    def __async_obj_make_async__(self,*args,**kwargs):
        if not self.async_obj_is_done():
            logging.warning("Old thread is being dismissed while creating a new one for the function: {func}".format(func=str(self.__async_obj_target_callable__)))
        while not self.__async_obj_thread_result_queue__.empty(): #keep the queue clean
            self.__async_obj_thread_result_queue__.get()
        self.__async_obj_worker_thread__ = threading.Thread(target=self.__async_obj_thread_func__, args = args, kwargs=kwargs, daemon=False)
        self.__async_obj_worker_thread__.start()
        self.__async_obj_thread_id__ = self.__async_obj_worker_thread__.native_id
        return True
        
    def __getattr__(self, attr):
        if attr not in self.__dict__: 
            if hasattr(self.__async_obj_sub_obj__, attr): #otherwise mimic the original object
                dummy = getattr(self.__async_obj_sub_obj__, attr)
                if callable(dummy):
                    self.__async_obj_target_callable__ = dummy
                    return self.__async_obj_make_async__
                else:
                    return dummy
        else:
            return super().__getattr__(attr)
        
    def __call__(self, *args, **kwargs):
        if callable(self.__async_obj_sub_obj__):
            self.__async_obj_target_callable__ = self.__async_obj_sub_obj__
            return self.__async_obj_make_async__(*args, **kwargs)
        else:
            return None