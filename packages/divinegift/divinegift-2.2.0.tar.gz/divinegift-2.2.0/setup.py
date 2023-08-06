from setuptools import setup, find_packages

with open('README.md') as f:
    long_description = f.read()

from divinegift import version

setup(name='divinegift',
      version=version,
      description='Ver.2.1.3. Portioning function has been added.',
      long_description=long_description,
      long_description_content_type='text/markdown',  # This is important!
      classifiers=[
                   'Development Status :: 5 - Production/Stable',
                   #'Development Status :: 3 - Alpha',
                   'License :: OSI Approved :: MIT License',
                   'License :: OSI Approved :: Apache Software License',
                   'Programming Language :: Python :: 3',
                   "Operating System :: OS Independent",
                   ],
      keywords='s7_it',
      url='https://gitlab.com/gng-group/divinegift.git',
      author='Malanris',
      author_email='admin@malanris.ru',
      license='MIT',
      packages=find_packages(),
      install_requires=['requests', 'mailer', 'deprecation', 'cryptography', 'pyyaml>=5.1', 'python-dateutil'],
      include_package_data=True,
      zip_safe=False)
