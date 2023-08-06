"""cw-celerytask-helpers packaging information"""

modname = 'cw_celerytask_helpers'
distname = 'cw-celerytask-helpers'

numversion = (0, 8, 0)
version = '.'.join(str(num) for num in numversion)

license = 'LGPL'
author = 'LOGILAB S.A. (Paris, FRANCE)'
author_email = 'contact@logilab.fr'
description = 'Worker side helpers for cubicweb-celerytask'
web = 'http://www.cubicweb.org/project/%s' % distname

__depends__ = {
    'celery': '>=4,<5',
    'redis': None,
    'six': None,
}

classifiers = [
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
]
