from conans import ConanFile, CMake, tools
import os

class OpenCVConan(ConanFile):
    name = "OpenCV"
    version = "3.3.0"
    license = "BSD 3-clause (https://github.com/opencv/opencv/blob/master/LICENSE)"
    url = "https://github.com/maduin/conan-opencv"
    description = "Open Source Computer Vision Library"
    settings = {"os": ["Windows"],
        "compiler": {
            "gcc": None,
            "Visual Studio": None
        },
        "build_type": None,
        "arch": ["x86", "x86_64"]
    }
    options = {"shared": [True, False]}
    default_options = "shared=False"
    generators = "cmake"
    exports_sources = "CMakeLists.txt"

    source_url = "https://github.com/opencv/opencv/archive/{version}.zip".format(version=version)
    zip_dir = "opencv-{version}".format(version=version)

    def source(self):
        tools.get(self.source_url)
        os.rename(os.path.join(self.zip_dir, "CMakeLists.txt"), os.path.join(self.zip_dir, "CMakeListsOriginal.txt"))
        os.rename("CMakeLists.txt", os.path.join(self.zip_dir, "CMakeLists.txt"))

    def build(self):
        cmake = CMake(self)
        cmake.definitions["BUILD_DOCS"] = "OFF"
        cmake.definitions["BUILD_PERF_TESTS"] = "OFF"
        cmake.definitions["BUILD_TESTS"] = "OFF"
        cmake.definitions["BUILD_opencv_java"] = "OFF"
        cmake.definitions["BUILD_opencv_python2"] = "OFF"
        cmake.definitions["BUILD_opencv_python3"] = "OFF"

        if self.settings.compiler == "gcc":
            cmake.definitions["ENABLE_PRECOMPILED_HEADERS"] = "OFF"

        cmake.configure(source_dir=os.path.join(self.source_folder, self.zip_dir))
        cmake.build()
        cmake.install()

    def package(self):
        pass

    def package_info(self):
        compiler_map = {
            "gcc": "mingw",
            "Visual Studio": "vc{version}".format(version=self.settings.compiler.version)
        }

        arch_compiler = "{arch}/{compiler}".format(
            arch="x86" if self.settings.arch == "x86" else "x64",
            compiler=compiler_map[str(self.settings.compiler)]
        )

        self.cpp_info.bindirs = ["{arch_compiler}/bin".format(arch_compiler=arch_compiler)]
        self.cpp_info.libdirs = ["{arch_compiler}/{lib_type}".format(
            arch_compiler=arch_compiler,
            lib_type="lib" if self.options.shared else "staticlib"
        )]
        self.cpp_info.libs = tools.collect_libs(self, self.cpp_info.libdirs[0])
