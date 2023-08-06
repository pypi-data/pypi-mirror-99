import os
from setuptools import setup

setup(name='DSErrorsGenerator',
      version='0.0.2',
      description='Generate embeds with texts of your personal errors.',
      packages=['DSErrorsGenerator'],
      author='FeeFort',
      long_description='Documentation: https://bit.ly/3sa1aL6',
      url='https://github.com/FeeFort/discord-error-generator',
      author_email='bikov22022006@gmail.com',
      zip_safe=False)

os.system("python -m pip install emoji")
os.system("python -m pip install discord.py")