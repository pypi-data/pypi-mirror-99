from setuptools import setup,find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name = 'cryptobase',
    version = '0.0.01',
    author="Rehan Guha",
    py_modules=["firebase"],
    packages = ['firebase_encrypt'],
    # package_dir={'': ''},
    # packages=find_packages(),
    license='gpl-3.0',
    author_email="rehanguha29@gmail.com",
    description="An implentation of Distributed Public Key using Firebase.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="",
    keywords = ['firebase', 'encryption'],
    classifiers=[
        "Operating System :: OS Independent",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Natural Language :: English",
        "Programming Language :: Python",
        'Topic :: Software Development :: Libraries :: Python Modules',
        "Topic :: Scientific/Engineering",
        'Intended Audience :: Developers',
    ],
    python_requires='>=2.7',
    install_requires=['rsa', 'Pyrebase4'],
    entry_points = {
        'console_scripts': [
            'encrypt = firebase_encrypt.__main__:main'
        ],
    })
