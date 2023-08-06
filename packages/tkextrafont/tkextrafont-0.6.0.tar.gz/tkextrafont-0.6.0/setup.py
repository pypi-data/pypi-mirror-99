"""
Author: RedFantom
License: GNU GPLv3
Copyright (c) 2021 RedFantom
"""
import sys


def read(file_name):
    with open(file_name) as fi:
        contents = fi.read()
    return contents


def printf(*args, **kwargs):
    kwargs.update({"flush": True})
    print(*args, **kwargs)


if "linux" in sys.platform:
    try:
        from skbuild import setup
        from skbuild.command.build import build
    except ImportError:
        printf("scikit-build is required to build this project")
        printf("install with `python -m pip install scikit-build`")
        raise


    class BuildCommand(build):
        """
        Intercept the build command to build the required modules in ./build

        extrafont depends on a library built from source. Building this library
        requires the following to be installed, Ubuntu package names:
        - fontconfig
        - libfontconfig1
        - libfontconfig1-dev
        - tcl-dev
        - tk-dev
        """

        def run(self):
            build.run(self)


    kwargs = {
        "install_requires": ["scikit-build"], "cmdClass": {"build": BuildCommand},
        "package_data": {"tkextrafont": ["extrafont.tcl", "fontnameinfo.tcl", "futmp.tcl", "pkgIndex.tcl"]}
    }

elif "win" in sys.platform:
    import os
    import shutil
    from setuptools import setup
    import subprocess as sp
    from typing import List, Optional

    dependencies = ["cmake", "tk", "toolchain", "fontconfig"]

    for dep in dependencies:
        printf("Installing dependency {}...".format(dep), end=" ")
        sp.call(["pacman", "--needed", "--noconfirm", "-S", "mingw-w64-x86_64-{}".format(dep)])  # , stdout=sp.PIPE)
        printf("Done.")
    sp.call(["cmake", ".", "-G", "MinGW Makefiles"])
    sp.call(["mingw32-make"])


    class DependencyWalker(object):
        """
        Walk the dependencies of a DLL file and find all DLL files

        DLL files are searched for in all the directories specified by
        - The PATH environment variable
        - The DLL_SEARCH_PATHS environment variable
        """

        def __init__(self, dll_file: str, dependencies_exe="deps\\dependencies.exe", specials=dict()):
            if not os.path.exists(dependencies_exe):
                printf("dependencies.exe is required to find all dependency DLLs")
                raise FileNotFoundError("Invalid path specified for dependencies.exe")
            self._exe = dependencies_exe
            if not os.path.exists(dll_file):
                raise FileNotFoundError("'{}' does not specify a valid path to first file".format(dll_file))
            self._dll_file = dll_file
            self._dll_cache = {}
            self._specials = specials
            self.walked = {}

        @property
        def dependency_dll_files(self) -> List[str]:
            """Return a list of abspaths to the dependency DLL files"""
            printf("Walking dependencies of {}".format(self._dll_file))
            dlls = [self._dll_file] + list(map(self._find_dll_abs_path, self._specials.keys()))
            done = []
            while set(dlls) != set(done):  # As long as not all dlls are done, keep searching
                for dll in set(dlls) - set(done):  # Go only over not-yet done DLLs
                    if dll is None:
                        done.append(None)
                        continue
                    printf("Looking for dependencies of {}".format(dll))
                    p = sp.Popen([self._exe, "-imports", dll], stdout=sp.PIPE)
                    stdout, stderr = p.communicate()
                    new_dlls = self._parse_dependencies_output(stdout)
                    for new_dll in new_dlls:
                        p = self._find_dll_abs_path(new_dll)
                        if p is None:
                            continue
                        elif "system32" in p:
                            continue
                        elif p not in dlls:
                            dlls.append(p)
                    done.append(dll)
            return list(set(dlls) - set((None,)))

        @staticmethod
        def _parse_dependencies_output(output: bytes) -> List[str]:
            """Parse the output of the dependencies.exe command"""
            dlls: List[str] = list()
            for line in map(str.strip, output.decode().split("\n")):
                if not line.startswith("Import from module"):
                    continue
                line = line[len("Import from module"):].strip(":").strip()
                dlls.append(line)
            return dlls

        def _find_dll_abs_path(self, dll_name: str) -> Optional[str]:
            """Find the absolute path of a specific DLL file specified"""
            if dll_name in self._dll_cache:
                return self._dll_cache[dll_name]
            printf("Looking for path of {}...".format(dll_name), end="")
            for var in ("PATH", "DLL_SEARCH_DIRECTORIES"):
                printf(".", end="")
                val = os.environ.get(var, "")
                for dir in val.split(";"):
                    if not os.path.exists(dir) and os.path.isdir(dir):
                        continue
                    if dir not in self.walked:
                        self.walked[dir] = list(os.walk(dir))
                    for dirpath, subdirs, files in self.walked[dir]:
                        if dll_name in files:
                            p = os.path.join(dirpath, dll_name)
                            printf(" Found: {}".format(p))
                            self._dll_cache[dll_name] = p
                            return p
            printf("Not found.")
            self._dll_cache[dll_name] = None
            return None

        def copy_to_target(self, target: str):
            for p in self.dependency_dll_files:
                if os.path.basename(p) in self._specials:
                    t = os.path.join(target, *self._specials[os.path.basename(p)].split("/"), os.path.basename(p))
                    d = os.path.dirname(t)
                    if not os.path.exists(d):
                        os.makedirs(d)
                    printf("Copying special {} -> {}".format(p, t))
                    shutil.copyfile(p, t)
                else:
                    printf("Copying {}".format(p))
                    target_file = os.path.join(target, os.path.basename(p))
                    try:
                        shutil.copyfile(p, target_file)
                    except shutil.SameFileError:
                        continue


    specials = {}
    DependencyWalker("libextrafont.dll", specials=specials).copy_to_target("tkextrafont")
    kwargs = {"package_data": {
        "extrafont": ["*.dll", "pkgIndex.tcl", "extrafont.tcl", "fontnameinfo.tcl", "futmp.tcl"] + [
            "{}/{}".format(dir.strip("/"), base) for base, dir in specials.items()]}}

else:
    printf("Only Linux and Windows are currently supported by the build system")
    printf("If you wish to help design a build method for your OS, please")
    printf("contact the project author.")
    raise RuntimeError("Unsupported platform")

setup(
    name="tkextrafont",
    version="v0.6.0",
    packages=["tkextrafont"],
    description="Fonts loader for Tkinter",
    author="The extrafont and tkextrafont authors",
    url="https://github.com/TkinterEP/tkextrafont",
    download_url="https://github.com/TkinterEP/tkextrafont/releases",
    license="GNU GPLv3",
    long_description=read("README.md"),
    long_description_content_type="text/markdown",
    zip_safe=False,
    **kwargs
)
