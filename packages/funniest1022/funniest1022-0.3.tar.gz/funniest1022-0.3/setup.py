from setuptools import setup

setup(name='funniest1022',
      version='0.3',
      description='The funniest joke in the world',
      url='http://github.com/storborg/funniest1022',
      author='Flying Circus',
      author_email='flyingcircus@example.com',
      license='MIT',
      packages=['funniest1022'],
      install_requires=[
          'pandas',
      ],
      zip_safe=False)