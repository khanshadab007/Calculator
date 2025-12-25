"""
Use of __init__.py (8-mark answer)

** The __init__.py file is used to tell Python that a directory should be treated as a package. 
Without it, Python may not recognize the folder as an 
importable package (especially in older versions and structured projects).

** It also controls what gets imported when `from package import *` is used,
by defining the __all__ list.
This helps hide internal functions and expose only the public API.

** __init__.py can be used to simplify imports by re-exporting classes or functions,
so users can import directly from the package instead of deep module paths.

** Additionally, it can store package-level constants, configuration values,
or lightweight initialization code, though it should never be used to start the
application or hold heavy logic.

"""