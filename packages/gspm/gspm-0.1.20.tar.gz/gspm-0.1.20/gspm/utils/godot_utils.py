
import logging
import platform
import gspm.utils.path_utils as path_utils
import wget
import zipfile
import os
import gspm.utils.process_utils as process_utils
import subprocess

from packaging.version import Version
from gspm.utils.versions import *


host_url = "https://downloads.tuxfamily.org/godotengine/{0}/"


def edit_godot(project):

    cmd = _build_godot_cmd(project)
    cmd = "{0} -e".format(cmd)
    # cmd = "start dir"
    logging.debug("- running command {0}".format(cmd))
    process_utils.run_process(cmd, True)


def install_godot(project):

    logging.debug("[godot_utils] install_godot")

    if project.config.godot.local:
        pass
    else:
        # if Version('{0}'.format(project.config.godot.version)) < Version('2.1'):
        #     raise Exception("Version [{0}] Not Supported".format(project.config.godot.version))

        # if Version('{0}'.format(project.config.godot.version)) > Version('3.2.3'):
        #     raise Exception("Version [{0}] Not Supported".format(project.config.godot.version))

        logging.debug(
            "- checking for godot [{0}]".format(project.config.godot.version))

        dest_path = \
            "{0}/godot-{1}" \
            .format(project.repository_home, project.config.godot.version)

        dest_path = os.path.abspath(dest_path)

        if os.path.exists(dest_path):
            if not project.args.force:
                logging.info(
                    "- godot is already available at [{0}] - skipping"
                    .format(dest_path))
                return
            else:
                path_utils.clean_path(dest_path)

        path_utils.create_path(dest_path)

        uri = _build_godot_uri(project)

        _mono = ''
        if (project.config.godot.mono):
            _mono = ' for mono'

        _version = "Version [{0}-{1}-{2}]{3} on [{4}]".format(project.config.godot.version, project.config.godot.release, project.config.godot.arch, _mono, _get_platform())

        if (uri == '*none'):
            raise Exception("Version {0} Not Supported.".format(_version))

        project.config.uri = uri

        logging.log(99,
            "getting godot {0}".format(_version))

        logging.debug(
            "- downloading [{0}] to [{1}]".format(uri, dest_path))

        file = wget.download(uri, dest_path)

        logging.log(99, "\r")
        
        logging.info("\r- dowload complete")
        zipf = zipfile.ZipFile(file)
        zipf.extractall(dest_path)
        zipf.close()

        if _get_platform() == "darwin":
            subprocess.call(['chmod', '-R', '+x', dest_path])
            
        if _get_platform() == "linux":
            subprocess.call(['chmod', '-R', '+x', dest_path])

        os.remove(file)


def run_godot(project):
    cmd = _build_godot_cmd(project)
    cmd = "{0} -r".format(cmd)
    # cmd = "start dir"
    logging.debug("- running command {0}".format(cmd))
    return process_utils.run_process(cmd, True)


def run_godot_script(project, script):
    cmd = _build_godot_cmd(project)
    cmd = "{0} {1}".format(cmd, script)
    # cmd = "start dir"
    logging.debug("- running command {0}".format(cmd))
    return process_utils.run_process(cmd, True)


def export_godot(project, name, path):
    cmd = _build_godot_cmd(project)
    cmd = "{0} --no-window --export {1} {2}".format(cmd, name, os.path.abspath(path))
    # cmd = "start dir"
    logging.debug("- running command {0}".format(cmd))
    return process_utils.run_process(cmd, True)


def _build_godot_uri(project):
    logging.debug("[godot_utils] _build_godot_uri")
    _uri = "*none"
    _mono = ''
    _system = _get_platform()

    if (project.config.godot.mono == True):
        _mono = 'mono'

    _version = ':{0}:{1}:{2}:{3}:{4}'.format(project.config.godot.version, project.config.godot.release, _system, project.config.godot.arch, _mono )

    if (_version in godot_versions):
        _uri = godot_versions[_version]

    return _uri


def _build_godot_uriX(project):
    logging.debug("[godot_utils] _build_godot_uri")

    system = _get_platform()
    uri = ""

    if project.args.headless:
        uri = _build_linux_uri(project)

    if system == "windows":
        uri = _build_windows_uri(project)

    if system == "darwin":
        uri = _build_darwin_uri(project)

    if system == "linux":
        uri = _build_linux_uri(project)

    if not uri:
        raise Exception("Platform [{0}] Not Supported".format(system))

    return uri


def _build_godot_cmd(project):
    logging.debug("[godot_utils] _build_godot_cmd")
    system = _get_platform()
    cmd = ""

    if system == "windows":
        cmd = _build_windows_cmd(project)

    if system == "darwin":
        cmd = _build_darwin_cmd(project)

    if system == "linux":
        cmd = _build_linux_cmd(project)

    if not cmd:
        raise Exception("Platform [{0}] Not Supported".format(system))

    return cmd


def _build_windows_uri(project):

    logging.debug("[godot_utils] _build_windows_uri")

    stable = 'stable'

    if Version('{0}'.format(project.config.godot.version)) < Version('3.3'):
        host = host_url.format(project.config.godot.version)
    else:
        host = host_url.format("{0}".format(project.config.godot.version) + "/alpha3")
        stable = 'alpha3'

    if Version('{0}'.format(project.config.godot.version)) < Version("2.1"):
        template = "{2}Godot_v{0}_{3}_win{1}.exe.zip"
    else:
        template = "{2}Godot_v{0}-{3}_win{1}.exe.zip"

    uri = template.format(project.config.godot.version, project.config.godot.arch, host, stable)
    return uri


def _build_darwin_uri(project):

    logging.debug("[godot_utils] _build_darwin_uri")

    stable = 'stable'
    host = host_url.format(project.config.godot.version)

    if Version('{0}'.format(project.config.godot.version)) > Version('3.3'):
        host = host_url.format("{0}".format(project.config.godot.version) + "/alpha3")
        stable = 'alpha3'

    template = "{2}Godot_v{0}-{3}_osx.{1}.zip"

    if Version('{0}'.format(project.config.godot.version)) < Version("3.1"):
        template = "{2}Godot_v{0}-{3}_osx.fat.zip"
    
    if Version('{0}'.format(project.config.godot.version)) < Version("2.1"):
        template = "{2}Godot_v{0}_{3}_osx32.zip"
    
    uri = template.format(project.config.godot.version, project.config.godot.arch, host, stable)
    return uri


def _build_linux_uri(project):

    logging.debug("[godot_utils] _build_linux_uri")

    stable = 'stable'

    if Version('{0}'.format(project.config.godot.version)) < Version('3.3'):
        host = host_url.format(project.config.godot.version)
    else:
        host = host_url.format("{0}".format(project.config.godot.version) + "/alpha3")
        stable = 'alpha3'

    if Version('{0}'.format(project.config.godot.version)) < Version("2.1"):
        template = "{2}Godot_v{0}_{3}_x11.{1}.zip"
    else:
        template = "{2}Godot_v{0}-{3}_x11.{1}.zip"
        #template = "{2}Godot_v{0}-{3}_linux_headless.{1}.zip"

    uri = template.format(project.config.godot.version, project.config.godot.arch, host, stable)
    return uri


def _build_windows_cmd(project):
    
    logging.debug("[godot_utils] _build_windows_cmd")
    cmd = ""
    proj_path = os.path.abspath(project.project_path)

    if project.config.godot.local:
        cmd = "start {0} --path {1}".format(os.path.abspath(project.config.godot.local), proj_path)
    else:
        godot_path = os.path.abspath("{0}/godot-{1}".format(project.repository_home, project.config.godot.version))
        cmd = "start {0}\{1} --path {2}".format(godot_path, _get_godot_runtime(project), proj_path)

    return cmd


def _build_linux_cmd(project):

    cmd = ""
    proj_path = os.path.abspath(project.project_path)

    if project.config.godot.local:
        cmd = "{0} --path {1}".format(os.path.abspath(project.config.godot.local), proj_path)
    else:
        godot_path = os.path.abspath("{0}/godot-{1}".format(project.repository_home, project.config.godot.version))
        proj_path = os.path.abspath(project.project_path)
        cmd = "{0}/{1} --path {2}".format(godot_path, _get_godot_runtime(project), proj_path, project.config.godot.arch)

    return cmd


def _build_darwin_cmd(project):

    cmd = ""
    proj_path = os.path.abspath(project.project_path)

    if project.config.godot.location:
        cmd = "{0} --path {1}".format(os.path.abspath(project.config.godot.location), proj_path)
    else:
        godot_path = os.path.abspath("{0}/godot-{1}".format(project.repository_home, project.config.godot.version))
        cmd = "arch -{3} {0}/{1} --path {2}".format(godot_path, _get_godot_runtime(project), proj_path, project.config.godot.arch)
        logging.debug(cmd)

    return cmd


#   return the platform we are running on
def _get_platform():
    logging.debug('[godot_utils] _get_platform')
    return platform.system().lower()


def _get_godot_runtime(project):
    logging.debug('[godot_utils] _get_godot_runtime')
    plat = _get_platform()
    runtime = ""

    if plat == "windows":
        runtime = _get_windows_runtime(project)

    if plat == "darwin":
        runtime = _get_darwin_runtime(project)

    if plat == "linux":
        runtime = _get_linux_runtime(project)

    if not runtime:
        raise Exception("Platform [{0}] Not Supported".format(plat))

    return runtime


def _get_windows_runtime(project):
    logging.debug('[godot_utils] _get_windows_runtime')
    _uri = _build_godot_uri(project)
    _runtime = _uri[_uri.rfind("/")+1:]
    _runtime = _runtime.replace('.zip', '')

    if (project.config.godot.mono):
        _runtime = '{0}\{0}'.format(_runtime)
        
    return _runtime


def _get_linux_runtime(project):
    logging.debug('[godot_utils] _get_linux_runtime')
    _uri = _build_godot_uri(project)
    _runtime = _uri[_uri.rfind("/")+1:]
    _runtime = _runtime.replace('.zip', '')

    if (project.config.godot.mono):
        _runtime = '{0}/{0}'.format(_runtime)
        _s = list(_runtime)
        _s[_runtime.rfind("_")] = '.'
        _runtime = "".join(_s)

    return _runtime


def _get_darwin_runtime(project):
    logging.debug('[godot_utils] _get_darwin_runtime')
    runtime = "Godot.app/Contents/MacOS/Godot"
    if (project.config.godot.mono):
            runtime = "Godot_mono.app/Contents/MacOS/Godot"

    return runtime

