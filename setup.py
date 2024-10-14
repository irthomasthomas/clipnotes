from setuptools import setup, find_packages
    import os

    # Read the contents of README.md
    this_directory = os.path.abspath(os.path.dirname(__file__))
    with open(os.path.join(this_directory, 'README.md'), encoding='utf-8') as f:
        long_description = f.read()

    setup(
        name='clipnotes',
        version='0.1.0',
        description='A tool to collect and process clipboard notes while reading papers or researching.',
        long_description=long_description,
        long_description_content_type='text/markdown',
        url='https://github.com/irthomasthomas/clipnotes',
        author='Thomas Thomas',
        author_email='irthomasthomas@gmail.com',
        license='MIT',
        packages=find_packages(),
        install_requires=[
            'pyperclip',
        ],
        entry_points={
            'console_scripts': [
                'clipnotes=clipnotes.clipnotes:main'
            ]
        },
        classifiers=[
            'Development Status :: 3 - Alpha',
            'Intended Audience :: Developers',
            'License :: OSI Approved :: MIT License',
            'Programming Language :: Python :: 3',
            'Programming Language :: Python :: 3.6',
            'Programming Language :: Python :: 3.7',
            'Programming Language :: Python :: 3.8',
            'Programming Language :: Python :: 3.9',
        ],
        python_requires='>=3.6',
        project_urls={
            'Bug Reports': 'https://github.com/irthomasthomas/clipnotes/issues',
            'Source': 'https://github.com/irthomasthomas/clipnotes',
        },
    )