from setuptools import setup, find_packages

VERSION = '0.0.1' 
DESCRIPTION = 'WebhooksaaS Python package'
LONG_DESCRIPTION = 'Python package to interact with the WebhooksaaS API.'

setup(
        name="webhooksaas", 
        version=VERSION,
        author="WebhooksaaS",
        author_email="usewebhooksaas@gmail.com",
        description=DESCRIPTION,
        long_description=LONG_DESCRIPTION,
        packages=find_packages(),
        install_requires=[],
        keywords=['python', 'webhooksaas', 'webhooks', 'api'],
        classifiers= [
            "Development Status :: 2 - Pre-Alpha",
            "Intended Audience :: Developers",
            "Programming Language :: Python :: 3",
            "Operating System :: MacOS :: MacOS X",
            "Operating System :: Microsoft :: Windows",
        ]
)
