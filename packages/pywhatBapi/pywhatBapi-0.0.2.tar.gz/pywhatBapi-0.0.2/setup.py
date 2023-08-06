import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name='pywhatBapi',
    version="0.0.2",
    author='Sai Jeevan Puchakayala',
    author_email='saijeevan2002@gmail.com',
    description='PyWhatBapi is a Python library for Sending whatsapp messages to many unsaved mobile numbers, using a csv file as a Database. The mobile numbers and specific messages can stored in the csv file.',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/SaiJeevanPuchakayala',
    project_urls={
        "Bug Tracker": "https://github.com/SaiJeevanPuchakayala/pywhatBapi/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],

    install_requires=[
        'pyautogui',
        'time',
        'pandas',
        'webbrowser',
      ],

    python_requires=">=3.6",
)
