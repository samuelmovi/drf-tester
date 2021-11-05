from setuptools import setup, find_packages

setup(
    name='drf-tester',
    version='0.1.2',
    description='Testing Suite for DjangoRestFramework developers with deadlines.',
    url='http://github.com/samuelmovi/drf-tester/',
    author='Samuel Movi',
    author_email='samuel.software.developer@email.com',
    license='MIT',
    packages=find_packages(include=['drf_tester', 'drf_tester.*']),
    install_requires=["Django", "djangorestframework"],
    zip_safe=False,
    # include_package_data=True,
)

