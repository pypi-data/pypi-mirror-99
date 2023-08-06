import re
import setuptools


CODE = "src/main"

with open(f'{CODE}/web_asset_vendor/__init__.py') as f:
    metadata = dict(re.findall(r'__(.*)__ = [\']([^\']*)[\']', f.read()))


setuptools.setup(
    name=metadata['title'],
    version=metadata['version'],
    author=metadata['author'],
    author_email=metadata['email'],
    maintainer=metadata['author'],
    maintainer_email=metadata['email'],
    license=metadata['license'],
    url='https://github.com/funkykay',
    description=u"Downloading assets from the web in a reproducible way",
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    install_requires=[
        'requests==2.25.1',
        'PyYAML==5.3.1'
    ],
    classifiers=[
        'Environment :: Web Environment',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7'
    ],
    package_dir={"": CODE},
    packages=setuptools.find_packages(where=CODE),
    python_requires=">=3.6",
)
