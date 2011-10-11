
import sys

from jcc import cpp

if len(sys.argv) == 1 or '--help' in sys.argv:
    help = '''
  JCC - C++/Python Java Native Interface Code Generator

  Usage: python -m jcc.__main__ [options] [actions]

  Input options:
    --jar JARFILE           - make JCC wrap all public classes found in
                              JARFILE, add it to the module's CLASSPATH and
                              include it in the distribution 
    --include JARFILE       - include JARFILE in the distribution and add
                              it to the module's CLASSPATH
    --import MODULE         - link against the wrappers to classes shared
                              with MODULE instead of generating duplicate
                              and incompatible wrappers
    --exclude CLASS         - explicitly don't wrap CLASS
    --package PACKAGE       - add PACKAGE to the list of packages from
                              which dependencies are automatically wrapped
    --classpath [PATH|JAR]  - add [PATH|JAR] to CLASSPATH while generating
                              wrappers 
    --libpath [PATH]        - add [PATH] to java.library.path while generating
                              wrappers 
    --module MODULE         - include Python MODULE in the distribution
    --reserved SYMBOL       - mark SYMBOL as a reserved word that will be
                              mangled in the generated C++ code to avoid
                              clashes with C/C++ reserved words or header
                              file definitions
    --vmarg                 - add extra Java VM initialization parameter
    --resources             - include resource directory in distribution as
                              package data

  Python wrapper generation options:
    --python NAME           - generate wrappers for use from Python in a module
                              called NAME
    --version VERSION       - the generated module's version number
    --shared                - generate a module that links against a shared
                              library version of the JCC runtime so that
                              multiple JCC-wrapped modules can be used within
                              the same Python runtime
    --sequence CLASS METHODSIGNATURE
                            - generate a pythonic sequence protocol wrapper for
                              CLASS
    --mapping CLASS METHODSIGNATURE1 METHODSIGNATURE2
                            - generate a pythonic map protocol wrapper for CLASS
    --rename CLASS1=NAME1,CLASS2=NAME2,...
                            - rename one or more Python wrapper classes to
                              avoid name clashes due to the flattening of
                              the Java package namespaces as mapped into
                              Python
    --no-generics           - disable support for Java generics

    If you're planning to use pythonic wrappers you should read the relevant
    documentation first:
      http://lucene.apache.org/pylucene/jcc/documentation/readme.html#python

  Output options:
    --debug                 - generate a module using the C++ compiler's
                              debug options
    --output OUTPUTDIR      - the wrapper will be generated in OUTPUTDIR,
                              'build' by default
    --files N               - split the generated wrapper file into at least
                              N files to workaround C++ compiler file size
                              limitations 
    --arch                  - Mac OS X only: filter the -arch parameters
                              Python was configured with to build leaner
                              binaries, faster
    --find-jvm-dll          - Windows only: extract the directory containing
                              jvm.dll from the registry and append it to the
                              Path at runtime

  Actions:
    --build                 - generate the wrapper and compile it
    --compile               - recompile the (previously generated) module
    --install               - install the wrapper in the local site-packages

  Distribution actions:
    --use-distutils         - use distutils even when setuptools is available
    --bdist                 - generate a binary distutils-based distribution
                              or a setuptools-based .egg
    --wininst               - create an installer application for Microsoft
                              Windows

  Other distutils/setuptools options (there are passed right through):
    --compiler COMPILER     - use COMPILER instead of the platform default
    --root ROOTDIR
    --install-dir INSTALLDIR
    --prefix PREFIX
    --home HOMEDIR
'''
    print help
    sys.exit(0)
  
cpp.jcc(sys.argv)
