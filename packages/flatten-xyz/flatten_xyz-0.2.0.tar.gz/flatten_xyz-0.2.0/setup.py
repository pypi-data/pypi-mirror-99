import setuptools

setuptools.setup(
    name='flatten_xyz',
    version='0.2.0',    
    description='A example for flatten arrays',
    url='https://github.com/adrian-zumbler/flatten_xyz',
    author='Adrian Meza',
    author_email='adrianm1@outlook.com',
    license='BSD 2-clause',
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.6",

    classifiers=[
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
)