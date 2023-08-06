#!/usr/bin/env python
#   -*- coding: utf-8 -*-

from setuptools import setup
from setuptools.command.install import install as _install

class install(_install):
    def pre_install_script(self):
        pass

    def post_install_script(self):
        pass

    def run(self):
        self.pre_install_script()

        _install.run(self)

        self.post_install_script()

if __name__ == '__main__':
    setup(
        name = 'github3api',
        version = '0.0.8',
        description = 'An advanced REST client for the GitHub API',
        long_description = "[![GitHub Workflow Status](https://github.com/soda480/github3api/workflows/build/badge.svg)](https://github.com/soda480/github3api/actions)\n[![Code Coverage](https://codecov.io/gh/soda480/github3api/branch/master/graph/badge.svg)](https://codecov.io/gh/soda480/github3api)\n[![Code Grade](https://www.code-inspector.com/project/13337/status/svg)](https://frontend.code-inspector.com/project/13337/dashboard)\n[![PyPI version](https://badge.fury.io/py/github3api.svg)](https://badge.fury.io/py/github3api)\n\n# github3api #\nAn advanced REST client for the GitHub API. It is a subclass of [rest3client](https://pypi.org/project/rest3client/) tailored for the GitHub API with special optional directives for GET requests that can return all pages from an endpoint or return a generator that can be iterated over. By default all requests will be retried if ratelimit request limit is reached.\n\n\n### Installation ###\n```bash\npip install github3api\n```\n\n### Example Usage ###\n\n```python\n>>> from github3api import GitHubAPI\n```\n\n`GitHubAPI` instantiation\n```python\n# instantiate using no-auth\n>>> client = GitHubAPI()\n\n# instantiate using a token\n>>> client = GitHubAPI(bearer_token='****************')\n```\n\n`GET` request\n```python\n# GET request - return JSON response\n>>> client.get('/rate_limit')['resources']['core']\n{'limit': 60, 'remaining': 37, 'reset': 1588898701}\n\n# GET request - return raw resonse\n>>> client.get('/rate_limit', raw_response=True)\n<Response [200]>\n```\n\n`POST` request\n```python\n>>> client.post('/user/repos', json={'name': 'test-repo1'})['full_name']\n'soda480/test-repo1'\n\n>>> client.post('/repos/soda480/test-repo1/labels', json={'name': 'label1', 'color': '#006b75'})['url']\n'https://api.github.com/repos/soda480/test-repo1/labels/label1'\n```\n\n`PATCH` request\n```python\n>>> client.patch('/repos/soda480/test-repo1/labels/label1', json={'description': 'my label'})['url']\n'https://api.github.com/repos/soda480/test-repo1/labels/label1'\n```\n\n`DELETE` request\n```python \n>>> client.delete('/repos/soda480/test-repo1')\n```\n\n`GET all` directive - Get all pages from an endpoint and return list containing only matching attributes\n```python\nfor repo in client.get('/user/repos', _get='all', _attributes=['full_name']):\n    print(repo['full_name'])\n```\n\n`GET page` directive - Yield a page from endpoint\n```python\nfor repo in client.get('/user/repos', _get='page'):\n    print(repo['full_name'])\n```\n\n### Projects using `github3api` ###\n\n* [edgexfoundry/sync-github-labels](https://github.com/edgexfoundry/cd-management/tree/git-label-sync) A script that synchronizes GitHub labels and milestones\n\n* [edgexfoundry/prune-github-tags](https://github.com/edgexfoundry/cd-management/tree/prune-github-tags) A script that prunes GitHub pre-release tags\n\n* [edgexfoundry/create-github-release](https://github.com/edgexfoundry/cd-management/tree/create-github-release) A script to facilitate creation of GitHub releases\n\n\n### Development ###\n\nEnsure the latest version of Docker is installed on your development server. Fork and clone the repository.\n\nBuild the Docker image:\n```sh\ndocker image build \\\n--target build-image \\\n--build-arg http_proxy \\\n--build-arg https_proxy \\\n-t \\\ngithub3api:latest .\n```\n\nRun the Docker container:\n```sh\ndocker container run \\\n--rm \\\n-it \\\n-e http_proxy \\\n-e https_proxy \\\n-v $PWD:/github3api \\\ngithub3api:latest \\\n/bin/sh\n```\n\nExecute the build:\n```sh\npyb -X\n```\n\nNOTE: commands above assume working behind a proxy, if not then the proxy arguments to both the docker build and run commands can be removed.\n",
        long_description_content_type = 'text/markdown',
        classifiers = [
            'Development Status :: 4 - Beta',
            'Environment :: Console',
            'Environment :: Other Environment',
            'Intended Audience :: Developers',
            'Intended Audience :: System Administrators',
            'License :: OSI Approved :: Apache Software License',
            'Operating System :: POSIX :: Linux',
            'Programming Language :: Python',
            'Programming Language :: Python :: 3.6',
            'Topic :: Software Development :: Libraries',
            'Topic :: Software Development :: Libraries :: Python Modules',
            'Topic :: System :: Networking',
            'Topic :: System :: Systems Administration'
        ],
        keywords = '',

        author = 'Emilio Reyes',
        author_email = 'emilio.reyes@intel.com',
        maintainer = '',
        maintainer_email = '',

        license = 'Apache License, Version 2.0',

        url = 'https://github.com/soda480/github3api',
        project_urls = {},

        scripts = [],
        packages = ['github3api'],
        namespace_packages = [],
        py_modules = [],
        entry_points = {},
        data_files = [],
        package_data = {},
        install_requires = ['rest3client'],
        dependency_links = [],
        zip_safe = True,
        cmdclass = {'install': install},
        python_requires = '',
        obsoletes = [],
    )
