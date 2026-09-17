import platform

from conan import ConanFile
from conan.tools.files import download
import os
import shutil

# Note: Do NOT use conan create for this package!
# Export this package with:
# conan export . --user overte --channel aqt

class AqtConan(ConanFile):
    name = "qt"
    version = "6.11.2"
    author = "Julian Groß (julian.gro@overte.org) & Edgar (Edgar@AnotherFoxGuy.com)"
    settings = "os", "arch"
    options = {
        "modules": ["ANY"],
    }
    default_options = {
        "modules": "qtmultimedia qtpositioning qtwebchannel qtwebengine qtwebsockets qt5compat",
    }

    def source(self):
        if platform.system() == "Windows":
            download(self, "https://build-deps.overte.org/conan/aqt/aqt_x64_2026-09-17_076e165_patched.exe",
                     "aqt.exe")
        else:
            Exception("This Conan AQT package only supports Windows.")

    def package(self):
        glob_args = "-O {0} -m {1}".format(self.source_folder, self.options.modules)

        self.run("aqt install-qt windows desktop {0} win64_msvc2022_64 {1}".format(self.version, glob_args))
        src_dir = os.path.join(self.source_folder, self.version, "msvc2022_64")
        file_names = os.listdir(src_dir)
        for file_name in file_names:
            shutil.move(os.path.join(src_dir, file_name), self.package_folder)

    def package_info(self):
        self.buildenv_info.define_path("Qt6_ROOT", self.package_folder)
        self.runenv_info.define_path("Qt6_ROOT", self.package_folder)
