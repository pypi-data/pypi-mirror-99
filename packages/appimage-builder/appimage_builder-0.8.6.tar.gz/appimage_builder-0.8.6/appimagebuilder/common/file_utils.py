#  Copyright  2020 Alexis Lopez Zubieta
#
#  Permission is hereby granted, free of charge, to any person obtaining a
#  copy of this software and associated documentation files (the "Software"),
#  to deal in the Software without restriction, including without limitation the
#  rights to use, copy, modify, merge, publish, distribute, sublicense, and/or
#  sell copies of the Software, and to permit persons to whom the Software is
#  furnished to do so, subject to the following conditions:
#
#  The above copyright notice and this permission notice shall be included in
#  all copies or substantial portions of the Software.
import os
import stat


def set_permissions_rx_all(path):
    os.chmod(
        path,
        stat.S_IRUSR
        | stat.S_IRGRP
        | stat.S_IROTH
        | stat.S_IXUSR
        | stat.S_IXGRP
        | stat.S_IXOTH
        | stat.S_IWUSR,
    )
