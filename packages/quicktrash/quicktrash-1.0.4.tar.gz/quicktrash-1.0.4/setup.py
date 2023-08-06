from setuptools import setup

ld=\
"""
Example
---------------
Command:
`python3 -m quicktrash file0.txt file1.pdf folder`

Output:
```
/home/user/.quicktrash/0x2/home/user/Documents/file0.txt
/home/user/.quicktrash/0x2/home/user/Documents/file1.pdf
/home/user/.quicktrash/0x2/home/user/Documents/folder
```

Python Examples
---------------
Using context:
```python
import quicktrash

with quicktrash.Trash("example-trashdir") as trash:
    trash.recycle("example-file.txt")
```
Using next()
```python
import quicktrash

tr = quicktrash.Trash("example-trashdir")
trlet:quicktrash.Trashlet = next(tr)
trlet.recycle("example-file.txt")
```
"""

setup(
    name='quicktrash',
    packages=["quicktrash"],
    version='1.0.4',
    description="EzPz Recycling",
    long_description=ld,
    long_description_content_type="text/markdown",
    author='Perzan',
    author_email='PerzanDevelopment@gmail.com',
    install_requires=["filelock~=3.0"]
)