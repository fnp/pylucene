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

import os, _winreg


class WindowsRegistry(object):

    def __init__(self):
        self.handle = _winreg.ConnectRegistry(None, _winreg.HKEY_LOCAL_MACHINE)

    def get(self, key, name):

        handle = None
        try:
            handle = _winreg.OpenKey(self.handle, key)
            return _winreg.QueryValueEx(handle, name)[0]
        finally:
            if handle is not None:
                handle.Close()

    def close(self):
        self.handle.Close()


def get_jvm_dll_directory(client_or_server="client"):

    jre_key = r"SOFTWARE\JavaSoft\Java Runtime Environment"
    jdk_key = r"SOFTWARE\JavaSoft\Java Development Kit"
    current_key = r"%s\%s"

    registry = None
    try:
        registry = WindowsRegistry()

        try: # try JRE
            version = registry.get(jre_key, "CurrentVersion")
            path = registry.get(current_key %(jre_key, version), "JavaHome")
            if not os.path.exists(path):
                path = None
        except:
            path = None

        if not path:
            try: # try JDK
                version = registry.get(jdk_key, "CurrentVersion")
                path = registry.get(current_key %(jdk_key, version), "JavaHome")
                if os.path.exists(path):
                    path = os.path.abspath(os.path.join(path, "jre"))
                else:
                    path = None
            except:
                path = None

    finally:
        if registry is not None:
            registry.close()

    if path:
        path = os.path.abspath(os.path.join(path, "bin", client_or_server))
        if os.path.exists(os.path.join(path, "jvm.dll")):
            return path

    return None


def add_jvm_dll_directory_to_path():

    path = os.environ['Path'].split(os.pathsep)
    dll_path = get_jvm_dll_directory()
    if dll_path is not None:
        path.append(dll_path)
        os.environ['Path'] = os.pathsep.join(path)
        return True

    raise ValueError, "jvm.dll could not be found"
