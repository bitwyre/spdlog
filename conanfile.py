from conans import ConanFile, CMake, tools


class SpdlogConan(ConanFile):
    name = "spdlog"
    version = "1.6.0rc"
    license = "<Put the package license here>"
    author = "<Put your name here> <And your email here>"
    url = "<Package recipe repository url here, for issues about the package>"
    description = "<Description of spdlog here>"
    topics = ("<Put some tag here>", "<here>", "<and here>")
    settings = "os", "compiler", "build_type", "arch"
    options = {
        "shared": [True, False],
        "use_pic": [True, False]
    }
    default_options = {"shared": False, "use_pic": False}
    requires = [
        "fmt/6.2.0@bitwyre/stable"
    ]
    generators = "cmake"
    exports_sources = "*"
    no_copy_source = True

    def _configure_cmake(self):
        cmake = CMake(self)
        cmake.definitions['BUILD_SHARED_LIBS'] = self.options.shared
        cmake.definitions['BUILD_TESTING'] = False
        cmake.definitions['CMAKE_POSITION_INDEPENDENT_CODE'] = self.options.use_pic
        cmake.definitions['CMAKE_PREFIX_PATH'] = self.deps_cpp_info["fmt"].rootpath
        cmake.definitions["SPDLOG_BUILD_BENCH"] = False
        cmake.definitions["SPDLOG_BUILD_EXAMPLE"] = False
        cmake.definitions["SPDLOG_BUILD_SHARED"] = self.options.shared
        cmake.definitions["SPDLOG_BUILD_TESTS"] = False
        cmake.definitions["SPDLOG_FMT_EXTERNAL"] = True
        cmake.definitions["SPDLOG_INSTALL"] = True
        cmake.configure()
        return cmake

    def build(self):
        cmake = self._configure_cmake()
        cmake.build()

    def package(self):
        cmake = self._configure_cmake()
        cmake.install()

    def package_info(self):
        self.cpp_info.libs = tools.collect_libs(self)
        self.cpp_info.defines = ["SPDLOG_COMPILED_LIB", "SPDLOG_FMT_EXTERNAL"]
        if self.settings.os == "Linux":
            self.cpp_info.system_libs = ["pthread"]
