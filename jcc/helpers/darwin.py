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

import sys, os

global JAVAHOME
JAVAHOME = None

if sys.platform == "darwin":

    # figure out where the JDK lives
    import platform, re
    _os_version = re.match("[0-9]+\.[0-9]+", platform.mac_ver()[0]).group(0)

    # this is where Apple says we should look for headers
    _path = "/System/Library/Frameworks/JavaVM.framework"
    if os.path.exists(os.path.join(_path, "Headers", "jni.h")):
        JAVAHOME = _path
    else:
        # but their updates don't always match their documentation, 
        # so look up the same path in the OS's /Developer tree
        _path = "/Developer/SDKs/MacOSX%s.sdk%s" %(_os_version, _path)
        if os.path.exists(os.path.join(_path, "Headers", "jni.h")):
            JAVAHOME = _path
