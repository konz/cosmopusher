from pybuilder.core import use_plugin, init

use_plugin("python.core")
use_plugin("python.unittest")
use_plugin("python.install_dependencies")
use_plugin("python.distutils")


name = "cosmopusher"
default_task = "publish"


@init
def set_properties(project):
    project.build_depends_on("pyhamcrest")
    project.depends_on("gevent")
    project.depends_on("pyserial")
    project.depends_on("docopt")
    project.depends_on("AWSIoTPythonSDK")

    project.set_property('distutils_console_scripts', ['cpusher=cosmopusher.cli:main'])
    project.set_property('distutils_classifiers', [
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python'
])
