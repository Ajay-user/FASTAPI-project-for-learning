from fastapi import Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials


class TokenBearer(HTTPBearer):
    def __init__(self, *, bearerFormat = None, scheme_name = None, description = None, auto_error = True):
        # super().__init__(bearerFormat=bearerFormat, scheme_name=scheme_name, description=description, auto_error=auto_error)
        super().__init__(auto_error=auto_error)

    async def __call__(self, request:Request):
        auth_credentials = await super().__call__(request)  # scheme='Bearer' credentials='xxxxxxxxxxxxxxxxxxx'
        scheme, credentials = auth_credentials

        
        return auth_credentials




class AccessTokenHandler(TokenBearer):
    pass

class RefreshTokenHandler(TokenBearer):
    pass










# MRO -- inheritance

### **How Method Resolution Works**
# 1. Python first looks for the method in the **class of the instance itself** (i.e., `ChildA` in your case).
# 2. If not found, it searches the **parent class** (`Root`).
# 3. If not found in the parent, it continues moving up the inheritance chain (including `object`, the base class of all Python classes).
# 4. The order of lookup follows **depth-first, left-to-right** (if multiple inheritance is involved).



# #### **Class Definitions**
# ```python
# class Root:
#     def __init__(self):
#         self.name = 'root'

#     def __call__(self, *args, **kwds):
#         print("hello from root", kwds['param'])
#         self.cb()  # Calls cb() method from the instance

#     def cb(self):
#         print("From root : CB")

# class ChildA(Root):  # Inherits from Root
#     def cb(self):  # Overrides the cb method in Root
#         print("From child: A")

# # Creating an instance of ChildA
# obj = ChildA()

# # Calling the instance like a function
# obj(param="test")
# ```

# ### **Step-by-Step Execution**
# 1. When `obj(param="test")` is executed:
#    - The `__call__` method in `Root` is invoked because `ChildA` **inherits** it but doesn’t override it.
#    - Inside `__call__`, `print("hello from root", kwds['param'])` executes first.
#    - Then, `self.cb()` is executed.
   
# 2. Now, Python must resolve which `cb()` method to call:
#    - Since `obj` is an instance of `ChildA`, Python **first looks for `cb()` in `ChildA`**.
#    - The method **is found** in `ChildA`, so it gets executed.
#    - Output will be:
#    ```
#    hello from root test
#    From child: A
#    ```

### **Method Resolution Order (MRO)**
# You can inspect the MRO using:
# ```python
# print(ChildA.mro())
# ```
# This will return:
# ```
# [<class '__main__.ChildA'>, <class '__main__.Root'>, <class 'object'>]
# ```
# This confirms that Python searches `ChildA` first, then `Root`, then `object`.

# ### **Summary**
# - `ChildA` inherits everything from `Root`, including `__call__`.
# - When `__call__` is executed, it **calls `self.cb()`**.
# - Python searches **first** in `ChildA`, finds its overridden `cb()`, and executes it.

