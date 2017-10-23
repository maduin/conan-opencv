from conans import ConanFile, CMake, RunEnvironment, tools
import os

class OpenCVTestConan(ConanFile):
    settings = "os", "compiler", "build_type", "arch"
    generators = "cmake"

    def build(self):
        cmake = CMake(self)
        cmake.configure(source_dir=self.conanfile_directory)
        cmake.build()

    def test(self):
        env = RunEnvironment(self)

        with tools.environment_append(env.vars):
            self.run("ctest -C {build_type}".format(build_type=self.settings.build_type))
