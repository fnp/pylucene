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

import os, sys, platform, subprocess

jcc_ver = '2.11'
machine = platform.machine()

if machine.startswith("iPod") or machine.startswith("iPhone"):
    platform = 'ipod'
elif sys.platform == "win32" and "--compiler=mingw32" in sys.argv:
    platform = 'mingw32'
else:
    platform = sys.platform

# Add or edit the entry corresponding to your system in the JDK, INCLUDES,
# CFLAGS, DEBUG_CFLAGS, LFLAGS and JAVAC dictionaries below. 
# These entries are used to build JCC _and_ by JCC to drive compiling and
# linking via distutils or setuptools the extensions it generated code for.
#
# The key for your system is determined by the platform variable defined
# above.
#
# Instead of editing the entries below, you may also override these
# dictionaries with JCC_JDK, JCC_INCLUDES, JCC_CFLAGS, JCC_DEBUG_CFLAGS,
# JCC_LFLAGS and JCC_JAVAC environment variables using os.pathsep as value
# separator.

if platform in ("win32", "mingw32"):
    try:
        from helpers.windows import JAVAHOME
    except ImportError:
        JAVAHOME = None
elif platform in ("darwin",):
    try:
        from helpers.darwin import JAVAHOME
    except ImportError:
        JAVAHOME = None
else:
    JAVAHOME = None

JDK = {
    'darwin': JAVAHOME,
    'ipod': '/usr/include/gcc',
    'linux2': '/usr/lib/jvm/java-6-openjdk',
    'sunos5': '/usr/jdk/instances/jdk1.6.0',
    'win32': JAVAHOME,
    'mingw32': JAVAHOME,
    'freebsd7': '/usr/local/diablo-jdk1.6.0'
}
if 'JCC_JDK' in os.environ:
    JDK[platform] = os.environ['JCC_JDK']


if not JDK[platform]:
    raise RuntimeError('''
                       
Can't determine where the Java JDK has been installed on this machine.

Please set the environment variable JCC_JDK to that location before
running setup.py.
''')

elif not os.path.isdir(JDK[platform]):
    raise RuntimeError('''
                       
Java JDK directory '%s' does not exist.

Please set the environment variable JCC_JDK to the correct location before
running setup.py.
''' %(JDK[platform]))


INCLUDES = {
    'darwin': ['%(darwin)s/Headers' %(JDK)],
    'ipod': ['%(ipod)s/darwin/default' %(JDK)],
    'linux2': ['%(linux2)s/include' %(JDK),
               '%(linux2)s/include/linux' %(JDK)],
    'sunos5': ['%(sunos5)s/include' %(JDK),
               '%(sunos5)s/include/solaris' %(JDK)],
    'win32': ['%(win32)s/include' %(JDK),
              '%(win32)s/include/win32' %(JDK)],
    'mingw32': ['%(mingw32)s/include' %(JDK),
                '%(mingw32)s/include/win32' %(JDK)],
    'freebsd7': ['%(freebsd7)s/include' %(JDK),
                 '%(freebsd7)s/include/freebsd' %(JDK)],
}

CFLAGS = {
    'darwin': ['-fno-strict-aliasing', '-Wno-write-strings'],
    'ipod': ['-Wno-write-strings'],
    'linux2': ['-fno-strict-aliasing', '-Wno-write-strings'],
    'sunos5': ['-features=iddollar',
               '-erroff=badargtypel2w,wbadinitl,wvarhidemem'],
    'win32': ["/EHsc", "/D_CRT_SECURE_NO_WARNINGS"],  # MSVC 9 (2008)
    'mingw32': ['-fno-strict-aliasing', '-Wno-write-strings'],
    'freebsd7': ['-fno-strict-aliasing', '-Wno-write-strings'],
}

# added to CFLAGS when JCC is invoked with --debug
DEBUG_CFLAGS = {
    'darwin': ['-O0', '-g', '-DDEBUG'],
    'ipod': ['-O0', '-g', '-DDEBUG'],
    'linux2': ['-O0', '-g', '-DDEBUG'],
    'sunos5': ['-DDEBUG'],
    'win32': ['/Od', '/DDEBUG'],
    'mingw32': ['-O0', '-g', '-DDEBUG'],
    'freebsd7': ['-O0', '-g', '-DDEBUG'],
}

LFLAGS = {
    'darwin': ['-framework', 'JavaVM'],
    'ipod': ['-ljvm', '-lpython%s.%s' %(sys.version_info[0:2]),
             '-L/usr/lib/gcc/arm-apple-darwin9/4.0.1'],
    'linux2/i386': ['-L%(linux2)s/jre/lib/i386' %(JDK), '-ljava',
                    '-L%(linux2)s/jre/lib/i386/client' %(JDK), '-ljvm',
                    '-Wl,-rpath=%(linux2)s/jre/lib/i386:%(linux2)s/jre/lib/i386/client' %(JDK)],
    'linux2/i686': ['-L%(linux2)s/jre/lib/i386' %(JDK), '-ljava',
                    '-L%(linux2)s/jre/lib/i386/client' %(JDK), '-ljvm',
                    '-Wl,-rpath=%(linux2)s/jre/lib/i386:%(linux2)s/jre/lib/i386/client' %(JDK)],
    'linux2/x86_64': ['-L%(linux2)s/jre/lib/amd64' %(JDK), '-ljava',
                      '-L%(linux2)s/jre/lib/amd64/server' %(JDK), '-ljvm',
                      '-Wl,-rpath=%(linux2)s/jre/lib/amd64:%(linux2)s/jre/lib/amd64/server' %(JDK)],
    'sunos5': ['-L%(sunos5)s/jre/lib/i386' %(JDK), '-ljava',
               '-L%(sunos5)s/jre/lib/i386/client' %(JDK), '-ljvm',
               '-R%(sunos5)s/jre/lib/i386:%(sunos5)s/jre/lib/i386/client' %(JDK)],
    'win32': ['/LIBPATH:%(win32)s/lib' %(JDK), 'jvm.lib'],
    'mingw32': ['-L%(mingw32)s/lib' %(JDK), '-ljvm'],
    'freebsd7': ['-L%(freebsd7)s/jre/lib/i386' %(JDK), '-ljava', '-lverify',
                 '-L%(freebsd7)s/jre/lib/i386/client' %(JDK), '-ljvm',
                 '-Wl,-rpath=%(freebsd7)s/jre/lib/i386:%(freebsd7)s/jre/lib/i386/client' %(JDK)],
}

IMPLIB_LFLAGS = {
    'win32': ["/IMPLIB:%s"],
    'mingw32': ["-Wl,--out-implib,%s"]
}

if platform == 'linux2':
    LFLAGS['linux2'] = LFLAGS['linux2/%s' %(machine)]

JAVAC = {
    'darwin': ['javac', '-target', '1.5'],
    'ipod': ['jikes', '-cp', '/usr/share/classpath/glibj.zip'],
    'linux2': ['javac'],
    'sunos5': ['javac'],
    'win32': ['%(win32)s/bin/javac.exe' %(JDK)],
    'mingw32': ['%(mingw32)s/bin/javac.exe' %(JDK)],
    'freebsd7': ['javac'],
}

JAVADOC = {
    'darwin': ['javadoc'],
    'ipod': [],
    'linux2': ['javadoc'],
    'sunos5': ['javadoc'],
    'win32': ['%(win32)s/bin/javadoc.exe' %(JDK)],
    'mingw32': ['%(mingw32)s/bin/javadoc.exe' %(JDK)],
    'freebsd7': ['javadoc'],
}

try:
    if 'USE_DISTUTILS' in os.environ:
        raise ImportError
    from setuptools import setup, Extension
    from pkg_resources import require
    with_setuptools = require('setuptools')[0].parsed_version

    enable_shared = False
    with_setuptools_c7 = ('00000000', '00000006', '*c', '00000007', '*final')

    if with_setuptools >= with_setuptools_c7 and 'NO_SHARED' not in os.environ:
        if platform in ('darwin', 'ipod', 'win32'):
            enable_shared = True
        elif platform == 'linux2':
            from helpers.linux import patch_setuptools
            enable_shared = patch_setuptools(with_setuptools)
        elif platform == 'mingw32':
            enable_shared = True
            # need to monkeypatch the CygwinCCompiler class to generate
            # jcc.lib in the correct place
            from helpers.mingw32 import JCCMinGW32CCompiler
            import distutils.cygwinccompiler
            distutils.cygwinccompiler.Mingw32CCompiler = JCCMinGW32CCompiler

except ImportError:
    if sys.version_info < (2, 4):
        raise ImportError, 'setuptools is required when using Python 2.3'
    else:
        from distutils.core import setup, Extension
        with_setuptools = None
        enable_shared = False


def main(debug):

    _jcc_argsep = os.environ.get('JCC_ARGSEP', os.pathsep)

    if 'JCC_INCLUDES' in os.environ:
        _includes = os.environ['JCC_INCLUDES'].split(_jcc_argsep)
    else:
        _includes = INCLUDES[platform]

    if 'JCC_CFLAGS' in os.environ:
        _cflags = os.environ['JCC_CFLAGS'].split(_jcc_argsep)
    else:
        _cflags = CFLAGS[platform]

    if 'JCC_DEBUG_CFLAGS' in os.environ:
        _debug_cflags = os.environ['JCC_DEBUG_CFLAGS'].split(_jcc_argsep)
    else:
        _debug_cflags = DEBUG_CFLAGS[platform]

    if 'JCC_LFLAGS' in os.environ:
        _lflags = os.environ['JCC_LFLAGS'].split(_jcc_argsep)
    else:
        _lflags = LFLAGS[platform]

    if 'JCC_IMPLIB_LFLAGS' in os.environ:
        _implib_lflags = os.environ['JCC_IMPLIB_LFLAGS'].split(_jcc_argsep)
    else:
        _implib_lflags = IMPLIB_LFLAGS.get(platform, [])

    if 'JCC_JAVAC' in os.environ:
        _javac = os.environ['JCC_JAVAC'].split(_jcc_argsep)
    else:
        _javac = JAVAC[platform]

    if 'JCC_JAVADOC' in os.environ:
        _javadoc = os.environ['JCC_JAVADOC'].split(_jcc_argsep)
    else:
        _javadoc = JAVADOC[platform]

    from helpers.build import jcc_build_py

    jcc_build_py.config_file = \
        os.path.join(os.path.dirname(os.path.abspath(__file__)),
                     'jcc', 'config.py')
    jcc_build_py.config_text = \
        '\n'.join(['',
                   'INCLUDES=%s' %(_includes),
                   'CFLAGS=%s' %(_cflags),
                   'DEBUG_CFLAGS=%s' %(_debug_cflags),
                   'LFLAGS=%s' %(_lflags),
                   'IMPLIB_LFLAGS=%s' %(_implib_lflags),
                   'SHARED=%s' %(enable_shared),
                   'VERSION="%s"' %(jcc_ver),
                   ''])

    extensions = []

    boot = '_jcc'

    cflags = ['-DPYTHON'] + _cflags
    if debug:
        cflags += _debug_cflags
    includes = _includes + [boot, 'jcc/sources']
    lflags = _lflags
    if not debug:
        if platform == 'win32':
            pass
        elif platform == 'sunos5':
            lflags += ['-Wl,-s']
        else:
            lflags += ['-Wl,-S']

    sources = ['jcc/sources/jcc.cpp',
               'jcc/sources/JCCEnv.cpp',
               'jcc/sources/JObject.cpp',
               'jcc/sources/JArray.cpp',
               'jcc/sources/functions.cpp',
               'jcc/sources/types.cpp']
    for path, dirs, names in os.walk(boot):
        for name in names:
            if name.endswith('.cpp'):
                sources.append(os.path.join(path, name))
    package_data = ['sources/*.cpp', 'sources/*.h', 'patches/patch.*']

    if with_setuptools and enable_shared:
        from subprocess import Popen, PIPE
        from setuptools import Library

        kwds = { "extra_compile_args": cflags,
                 "include_dirs": includes,
                 "define_macros": [('_jcc_lib', None),
                                   ('JCC_VER', '"%s"' %(jcc_ver))],
                 "sources": sources[0:2] }

        if platform in ('darwin', 'ipod'):
            kwds["extra_link_args"] = \
                lflags + ['-install_name', '@rpath/libjcc.dylib',
                          '-current_version', jcc_ver,
                          '-compatibility_version', jcc_ver]
        elif platform == 'linux2':
            kwds["extra_link_args"] = \
                lflags + ['-lpython%s.%s' %(sys.version_info[0:2])]
            kwds["force_shared"] = True    # requires jcc/patches/patch.43
        elif platform in IMPLIB_LFLAGS:
            jcclib = 'jcc%s.lib' %(debug and '_d' or '')
            implib_flags = ' '.join(IMPLIB_LFLAGS[platform])
            kwds["extra_link_args"] = \
                lflags + [implib_flags %(os.path.join('jcc', jcclib))]
            package_data.append(jcclib)
        else:
            kwds["extra_link_args"] = lflags

        extensions.append(Library('jcc', **kwds))

        args = _javac[:]
        args.extend(('-d', 'jcc/classes'))
        args.append('java/org/apache/jcc/PythonVM.java')
        args.append('java/org/apache/jcc/PythonException.java')
        if not os.path.exists('jcc/classes'):
            os.makedirs('jcc/classes')
        try:
            process = Popen(args, stderr=PIPE)
        except Exception, e:
            raise type(e), "%s: %s" %(e, args)
        process.wait()
        if process.returncode != 0:
            raise OSError, process.stderr.read()
        package_data.append('classes/org/apache/jcc/PythonVM.class')
        package_data.append('classes/org/apache/jcc/PythonException.class')

        args = _javadoc[:]
        args.extend(('-d', 'javadoc', '-sourcepath', 'java', 'org.apache.jcc'))
        try:
            process = Popen(args, stderr=PIPE)
        except Exception, e:
            raise type(e), "%s: %s" %(e, args)
        process.wait()
        if process.returncode != 0:
            raise OSError, process.stderr.read()

    extensions.append(Extension('jcc._jcc',
                                extra_compile_args=cflags,
                                extra_link_args=lflags,
                                include_dirs=includes,
                                define_macros=[('_java_generics', None),
                                               ('JCC_VER', '"%s"' %(jcc_ver))],
                                sources=sources))

    args = {
        'name': 'JCC',
        'version': jcc_ver,
        'description': 'a C++ code generator for calling Java from C++/Python',
        'long_description': open('DESCRIPTION').read(),
        'author': 'Andi Vajda',
        'author_email': 'vajda@apache.org',
        'classifiers': ['Development Status :: 5 - Production/Stable',
                        'Environment :: Console',
                        'Intended Audience :: Developers',
                        'License :: OSI Approved :: Apache Software License',
                        'Operating System :: OS Independent',
                        'Programming Language :: C++',
                        'Programming Language :: Java',
                        'Programming Language :: Python',
                        'Topic :: Software Development :: Code Generators',
                        'Topic :: Software Development :: Libraries :: Java Libraries'],
        'packages': ['jcc'],
        'package_dir': {'jcc': 'jcc'},
        'package_data': {'jcc': package_data},
        'ext_modules': extensions,
        "cmdclass": {"build_py": jcc_build_py},
    }
    if with_setuptools:
        args['zip_safe'] = False
        
    setup(**args)


if __name__ == "__main__":
    main('--debug' in sys.argv)
