#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.

import os

from distutils.command.build_py import build_py
from distutils import log

class jcc_build_py(build_py):
    config_text = None
    config_file = None

    def run(self):
        self.write_jcc_config()
        return build_py.run(self)

    def write_jcc_config(self):
        # only write jcc's config.py file if it doesn't exist or a build 
        # command is given
        write = False
        if not os.path.isfile(self.config_file):
            write = True
        else:
            for command in self.distribution.commands:
                if command.startswith("build"):
                    write = True
                    break

        if write:
            log.info("writing %s" %(self.config_file))
            config = open(self.config_file, 'w')
            try:
                config.write(self.config_text)
            finally:
                config.close()
        else:
            log.info("not writing %s" %(self.config_file))
