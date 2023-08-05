from setuptools import setup

def read():
    return open("README.rst", "r").read()

setup(
    name='botd',
    version='30',
    url='https://github.com/bthate/botd',
    author='Bart Thate',
    author_email='bthate@dds.nl', 
    description="the bot daemon",
    long_description=read(),
    license='Public Domain',
    install_requires=["feedparser"],
    zip_safe=True,
    packages=["botd", "botl", "botl.cmd"],
    include_package_data=True,
    data_files=[('share/botd', ['botd.service']),
                 ('share/man/man8', ['man/botd.8.gz', 'man/botctl.8.gz'])],
    scripts=["bin/bot", "bin/botc", "bin/botctl", "bin/botd"],
    classifiers=['Development Status :: 3 - Alpha',
                 'License :: Public Domain',
                 'Operating System :: Unix',
                 'Programming Language :: Python',
                 'Topic :: Utilities'
                ]
)
