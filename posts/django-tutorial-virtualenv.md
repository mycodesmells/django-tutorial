# Django Tutorial - Virtualenv

One of the first things that you should have in mind when starting your project is how to organize its environment. Nowadays no project can live without any dependencies, and managing them is often a very important thing that you need to take care of. Let's dive into django - Python's beloved web framework - and find out how to manage dependencies in a clean and easy way.

### Dependencies in Python

The most important tool to be used when talking about Python's dependencies is `pip` - a thingie that installs everything. If you are used to Node JS dependency management, and even, to some extent, Java's, you might be surprised that all dependencies are installed in a common place. This might lead to come conflicts (eg. one library used in two projects, each requiring a different version) and deployment issues (forgetting to define a library as a dependency, because it has already been installed). There is a pretty cool solution for all this - **virtualenv**.

### Python 3 as python

In our little project we'd like to use Python 3 (`python3` on my Linux) instead of default Python  2.7 (`python`), and this also can be done with virtualenv. Let's start by checking what we already know - that it's not how we'd like it to be:

	$ python -V
	Python 2.7.6

### What does virtualenv do?

Creating a virtual environment will produce a directory in which a separate Python executable is installed. This not only allows us to use any Python version as a `python` command, but, and this is the most important thing, creates a separate place for all dependencies related to this Python. This way you can install all your dependencies here and they will not be shared between virtual environments of your system. This is particularily useful if you ever want to run your application on another machine and want to list all required libraries (and no more than that). You can easily erase the packages folder, install all from your list and check in the application could run.

### Creating virtualenv

First, you need to install virtualenv to your system. On my Linux Mint you should run:

	$ sudo apt-get install python-virtualenv

After successful installation, you may create your virtual environment. To do so, just pick a folder to store it (we'll call it _venv_), select your Python executable (`python3` in our case) and run:

	$ virtualenv -p python3 venv
	Running virtualenv with interpreter /usr/bin/python3
	Using base prefix '/usr'
	New python executable in venv/bin/python3
	Also creating executable in venv/bin/python
	Installing setuptools, pip, wheel...done.

Now to activate it:

	$ source venv/bin/activate
	(venv) $

### Using virtualenv

Note that after activtion you can see the virtual environment name before your command line prompt. Once you install your dependency, it's stored only within this directory. For example when we list the dependencies after intalling django, you can see:

	(venv) $ pip install django
	...

	(venv) $ pip freeze
	Django==1.8.5
	wheel==0.24.0


To check that the version now is as we expected to be:

	(venv) $ python -V
	Python 3.4.0

To deactivate and return to your system Python, simply type:

	(venv) deactivate
	
	$ python -V
	Python 2.7.6

	$ pip freeze
	BeautifulSoup==3.2.1
	Mako==0.9.1
	MarkupSafe==0.18
	...