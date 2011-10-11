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


def patch_st_dir(patch_version, st_egg, jccdir):
    return '''

Shared mode is disabled, setuptools patch.43.%s must be applied to enable it
or the NO_SHARED environment variable must be set to turn off this error.

    sudo patch -d %s -Nup0 < %s/jcc/patches/patch.43.%s

See %s/INSTALL for more information about shared mode.
''' %(patch_version, st_egg, jccdir, patch_version, jccdir)


def patch_st_zip(patch_version, st_egg, jccdir):
    return '''

Shared mode is disabled, setuptools patch.43.%s must be applied to enable it
or the NO_SHARED environment variable must be set to turn off this error.

    mkdir tmp
    cd tmp
    unzip -q %s
    patch -Nup0 < %s/jcc/patches/patch.43.%s
    sudo zip %s -f
    cd ..
    rm -rf tmp

See %s/INSTALL for more information about shared mode.
''' %(patch_version, st_egg, jccdir, patch_version, st_egg, jccdir)


def patch_setuptools(with_setuptools):

    with_setuptools_c11 = ('00000000', '00000006', '*c', '00000011', '*final')

    try:
        from setuptools.command.build_ext import sh_link_shared_object
        enable_shared = True  # jcc/patches/patch.43 was applied
    except ImportError:
        import setuptools
        jccdir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        st_egg = os.path.dirname(setuptools.__path__[0])
        if with_setuptools < with_setuptools_c11:
            patch_version = '0.6c7'
        else:
            patch_version = '0.6c11'

        if os.path.isdir(st_egg):
            raise NotImplementedError, patch_st_dir(patch_version, st_egg,
                                                    jccdir)
        else:
            raise NotImplementedError, patch_st_zip(patch_version, st_egg,
                                                    jccdir)

    return enable_shared
