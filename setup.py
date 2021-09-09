from setuptools import setup

setup(
    name='drf-tester',
    version='0.1.1',
    description='Testing Suite for DjangoRestFramework developers with deadlines.',
    url='http://github.com/samuelmovi/drf-tester/',
    author='Samuel Movi',
    author_email='samuel.software.developer@email.com',
    license='MIT',
    packages=['drf_tester',],
    install_requires=["Django", "djangorestframework"],
    zip_safe=False,
    include_package_data=True,
)

