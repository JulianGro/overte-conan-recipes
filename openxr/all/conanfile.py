import os
from conan import ConanFile
from conan.tools.files import get, collect_libs, replace_in_file, rmdir, copy
from conan.tools.cmake import CMakeToolchain, CMake, cmake_layout, CMakeDeps


class OpenxrConan(ConanFile):
    name = "openxr"
    description = "Generated headers and sources for OpenXR loader."
    url = "https://github.com/conan-io/conan-center-index"
    homepage = "https://github.com/KhronosGroup/OpenXR-SDK"
    license = "Apache License 2.0"
    settings = "os", "compiler", "build_type", "arch"
    implements = ["auto_shared_fpic"]
    options = {"shared": [True, False], "fPIC": [True, False]}
    default_options = {"shared": False, "fPIC": True}

    def layout(self):
        cmake_layout(self)

    def requirements(self):
        self.requires("jsoncpp/1.9.6")
        self.requires("vulkan-headers/1.4.313.0")  # Whatever version Overte's other dependencies use.
        self.requires("vulkan-loader/1.4.313.0")  # Whatever version Overte's other dependencies use.

    def source(self):
        get(self, **self.conan_data["sources"][self.version], strip_root=True)

    def generate(self):
        tc = CMakeToolchain(self)
        tc.variables["DYNAMIC_LOADER"] = self.options.shared
        tc.variables["BUILD_TESTS"] = False
        # Force using Conan jsoncpp, rather than autodetect.
        tc.variables["BUILD_WITH_SYSTEM_JSONCPP"] = True
        # Build all extensions, rather than autodetect.
        tc.variables["BUILD_ALL_EXTENSIONS"] = True
        # Hack to work around OpenXR-loader trying to load manifest files from its build directory,
        # which can result in "permission denied" errors on the target system.
        tc.variables["CMAKE_INSTALL_FULL_SYSCONFDIR"] = "/etc"
        tc.generate()
        deps = CMakeDeps(self)
        deps.generate()

    def build(self):
        cmake = CMake(self)
        cmake.configure()
        cmake.build()

    def package(self):
        copy(self, "LICENSE", src=self.source_folder, dst="licenses")
        cmake = CMake(self)
        cmake.install()

    def package_info(self):
        self.cpp_info.set_property("cmake_file_name", "OpenXR")
        self.cpp_info.set_property("cmake_target_name", "OpenXR::openxr_loader")
        self.cpp_info.libs = collect_libs(self)
        self.cpp_info.includedirs.append(os.path.join("include", "openxr"))
