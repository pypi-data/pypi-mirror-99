from setuptools import setup

f=open('requirements.txt')
req = []
for line in f:
    req.append(line.strip())
f.close()

with open('../README.md') as f:
      long_description = f.read()

setup(name='textcl',
      packages=['textcl'],
      version='0.1.1',
      license='MIT',
      description='Package for text preprocessing to use in nlp tasks',
      author = 'Alina Petukhova',
      author_email = 'petukhova.alina@gmail.com',
      long_description = long_description,
      long_description_content_type='text/markdown',
      url = 'https://github.com/alinapetukhova/textcl',
      download_url = 'https://github.com/alinapetukhova/textcl/archive/refs/tags/v.0.1.1.tar.gz',
      keywords = ['NLP', 'Text preprocessing', 'Outlier detection'],
      install_requires=req,
      python_requires='>=3.6', 
      zip_safe=False,
      classifiers=[
            'Development Status :: 4 - Beta',
            'Intended Audience :: Developers',
            'Topic :: Scientific/Engineering :: Artificial Intelligence',
            'License :: OSI Approved :: MIT License',
            'Programming Language :: Python :: 3.6',
            'Programming Language :: Python :: 3.7',
            'Programming Language :: Python :: 3.8'
      ])
