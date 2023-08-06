# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['htrace']

package_data = \
{'': ['*']}

install_requires = \
['click>=7.1.2,<8.0.0', 'dateparser>=1.0.0,<2.0.0', 'requests>=2.25.1,<3.0.0']

entry_points = \
{'console_scripts': ['htrace = htrace.__main__:main']}

setup_kwargs = {
    'name': 'htrace',
    'version': '0.2.0',
    'description': 'Tracing HTTP requests over redirects, link headers',
    'long_description': '# htrace\n\nSimple command line utility for tracing HTTP requests over redirects.\n\n```\nUsage: htrace [OPTIONS] URL\n\nOptions:\n  -T, --timeout INTEGER  Request timeout in seconds\n  -a, --accept TEXT      Accept header value\n  -j, --json             Report in JSON\n  -b, --body             Show response body\n  --help                 Show this message and exit.\n```\n\nExample:\n```\n% htrace "http://schema.org/"\n2021-03-19 08:18:09.371:> GET: http://schema.org/\n2021-03-19 08:18:09.371:> Accept: */*\n2021-03-19 08:18:09.371:< 301 http://schema.org/\n2021-03-19 08:18:09.371:< Content-Length: 0\n2021-03-19 08:18:09.371:< Content-Type: text/html\n2021-03-19 08:18:09.371:< Date: Fri, 19 Mar 2021 12:18:09 GMT\n2021-03-19 08:18:09.371:< Location: https://schema.org/\n2021-03-19 08:18:09.371:< Server: Google Frontend\n2021-03-19 08:18:09.371:< X-Cloud-Trace-Context: dc661d58e457af35212814c8e90163f8\n2021-03-19 08:18:09.371:< 0.0603 sec\n2021-03-19 08:18:09.426:> GET: https://schema.org/\n2021-03-19 08:18:09.426:> Accept: */*\n2021-03-19 08:18:09.426:< 200 https://schema.org/\n2021-03-19 08:18:09.426:< Access-Control-Allow-Credentials: true\n2021-03-19 08:18:09.426:< Access-Control-Allow-Headers: Accept\n2021-03-19 08:18:09.426:< Access-Control-Allow-Methods: GET\n2021-03-19 08:18:09.426:< Access-Control-Allow-Origin: *\n2021-03-19 08:18:09.426:< Access-Control-Expose-Headers: Link\n2021-03-19 08:18:09.426:< Age: 413\n2021-03-19 08:18:09.426:< Alt-Svc: h3-29=":443"; ma=2592000,h3-T051=":443"; ma=2592000,h3-Q050=":443"; ma=2592000,h3-Q046=":443"; ma=2592000,h3-Q043=":443"; ma=2592000,quic=":443"; ma=2592000; v="46,43"\n2021-03-19 08:18:09.426:< Cache-Control: public, max-age=600\n2021-03-19 08:18:09.426:< Content-Encoding: gzip\n2021-03-19 08:18:09.426:< Content-Length: 2206\n2021-03-19 08:18:09.426:< Content-Type: text/html\n2021-03-19 08:18:09.426:< Date: Fri, 19 Mar 2021 12:11:16 GMT\n2021-03-19 08:18:09.426:< ETag: "z2afww"\n2021-03-19 08:18:09.427:< Expires: Fri, 19 Mar 2021 12:21:16 GMT\n2021-03-19 08:18:09.427:< Link: </docs/jsonldcontext.jsonld>; rel="alternate"; type="application/ld+json"\n2021-03-19 08:18:09.427:< Server: Google Frontend\n2021-03-19 08:18:09.427:< X-Cloud-Trace-Context: 63d878a82afe363fca6c584963eb764b\n2021-03-19 08:18:09.427:< 0.0524 sec\n2021-03-19 08:18:09.457:SUMMARY: Start URL: http://schema.org/\n2021-03-19 08:18:09.457:SUMMARY: Final URL: https://schema.org/\n2021-03-19 08:18:09.457:SUMMARY: Start: 2021-03-19T12:18:09+0000\n2021-03-19 08:18:09.457:SUMMARY: Num requests: 2\n2021-03-19 08:18:09.457:SUMMARY: Elapsed: 0.113 seconds\n```\n',
    'author': 'datadavev',
    'author_email': '605409+datadavev@users.noreply.github.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/datadavev/htrace',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
