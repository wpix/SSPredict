from setuptools import setup

name1 = 'sspredict.plot = sspredict.plot_ss_ternary:main'
name2 = 'sspredict.predict = sspredict.predict_ss:main'
setup(
    name='SSPredict',
    version='0.1.0',
    url = 'https://github.com/DS-Wen/SSPredict',
    license ='MIT',
    author='Dongsheng Wen, Michael S. Titus',
    author_email='ds-wen@outlook.com, titus9@purdue.edu',
    description='Predict and plot the solid solution strengthening stress of CCAs in pseudo-ternary diagrams',
    packages = ['sspredict','sspredict/make_composition'],
    entry_points={
          'console_scripts': [name1,name2]
      },
    platforms='any',
    install_requires=[
    'numpy >= 1.13.3',
    'matplotlib >= 2.1.0',
    'pandas >= 0.23.4']


)
