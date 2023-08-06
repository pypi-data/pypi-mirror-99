import setuptools 

with open('README.md', 'r') as fh:
    long_description = fh.read()

setuptools.setup (
    name = 'pypassmanager',
    version = '1.0.1',
    description = 'Python Password Manager',
    long_description = long_description,
    long_description_content_type = 'text/markdown',
    author = 'Ajith S',
    author_email = 'ajiths1311@gmail.com',
    url = 'https://github.com/11ajith/pypassman',
    package_dir={'pypassmanager': 'src'},
    packages = ['pypassmanager'],
    install_requires=['bcrypt', 'pyperclip', 'cryptography'],  
    entry_points = {
        'console_scripts': ['pypassmanager = pypassmanager.password_manager:main'],
    },
    license = 'MIT',
    classifiers = [
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires = '>=3.6'
)
