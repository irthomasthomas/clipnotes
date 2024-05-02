from setuptools import setup

setup(
    name='clipnotes',
    version='0.1.0',
    description='A tool to collect and process clipboard notes while reading papers or researching.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/irthomasthomas/clipnotes',
    author='Thomas Thomas',
    author_email='irthomasthomas@gmail.com',
    license='MIT',
    py_modules=['clipnotes'],
    entry_points={
        'console_scripts': [
            'clipnotes=clipnotes:main'
        ]
    }
)
