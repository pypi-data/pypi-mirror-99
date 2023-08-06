from setuptools import setup, find_packages

with open('README.md') as readme_file:
    readme = readme_file.read()

with open('LICENSE') as license_file:
    license = license_file.read()

requirements = [
    # TODO: put package requirements here
]

test_requirements = [
    # TODO: put package test requirements here
]

setup(
    name='d8s',
    version='0.1.0',
    description="Future home of democritus project.",
    long_description=readme,
    author="Floyd Hightower",
    author_email='floyd.hightower27@gmail.com',
    project_urls={
        'Documentation': 'https://github.com/democritus-project/',
        'Say Thanks!': 'https://saythanks.io/to/floyd.hightower27%40gmail.com',
        'Source': 'https://github.com/democritus-project/',
        'Tracker': 'https://github.com/democritus-project/roadmap/issues',
        'Changelog': 'https://github.com/democritus-project/roadmap/',
    },
    packages=find_packages(exclude=('tests', 'docs')),
    include_package_data=True,
    install_requires=requirements,
    license=license,
    zip_safe=True,
    keywords='democritus,d8s,utility,utils',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
    test_suite='tests',
    tests_require=test_requirements
)
