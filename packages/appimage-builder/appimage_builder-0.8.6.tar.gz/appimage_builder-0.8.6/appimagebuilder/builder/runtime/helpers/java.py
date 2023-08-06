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
from pathlib import Path

from appimagebuilder.common.finder import Finder
from .base_helper import BaseHelper
from ..environment import Environment


class Java(BaseHelper):
    def configure(self, env: Environment):
        java_path = self.finder.find_one("java", [Finder.is_file, Finder.is_executable])
        if java_path:
            java_home = Path(java_path).parent.parent
            env.set("JAVA_HOME", str(java_home))
