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

import os, copy
from distutils.cygwinccompiler import Mingw32CCompiler

class JCCMinGW32CCompiler(Mingw32CCompiler):

    def link(self, target_desc, objects, output_filename, output_dir=None,
             libraries=None, library_dirs=None, runtime_library_dirs=None,
             export_symbols=None, debug=0, extra_preargs=None,
             extra_postargs=None, build_temp=None, target_lang=None): 
 
        # use separate copies, so we can modify the lists
        extra_preargs = copy.copy(extra_preargs or [])

        (dll_name, dll_extension) = os.path.splitext(output_filename)
        if dll_extension.lower() == ".dll":
            extra_preargs.extend(["-Wl,--out-implib,%s" %(os.path.join(os.path.dirname(dll_name), "jcc", "jcc.lib"))])

        Mingw32CCompiler.link(self, target_desc=target_desc,
                              objects=objects,
                              output_filename=output_filename, 
                              output_dir=output_dir, libraries=libraries,
                              library_dirs=library_dirs,
                              runtime_library_dirs=runtime_library_dirs,
                              export_symbols=export_symbols, debug=debug,
                              extra_preargs=extra_preargs,
                              extra_postargs=extra_postargs, 
                              build_temp=build_temp,
                              target_lang=target_lang)
