from setuptools import setup

setup(
    name='CryptoMax',
    version='1.0.0',    
    description='A Python package for implementing cryptography algorithms',
    url='https://github.com/shuds13/pyexample',
    author='Paul Hudson',
    author_email='ehdtvyt@gmail.com',
    license='BSD 2-clause',
    py_modules=["CryptoMax"],
    package_dir={'':'src'},
    install_requires=['numpy', 'sympy', 'pycryptodome'],

    classifiers=[
        'Development Status :: 1 - Planning',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: BSD License',       
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
)