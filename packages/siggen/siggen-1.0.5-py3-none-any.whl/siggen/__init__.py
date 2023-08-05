# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from pkg_resources import parse_version


# yyyymmdd
__releasedate__ = "20210318"

# x.y.z or x.y.z.dev0 -- semver
__version__ = "1.0.5"
VERSION = parse_version(__version__)
