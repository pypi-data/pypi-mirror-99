from abc import ABC, abstractmethod
from contextlib import closing, contextmanager
import glob
import os
from os.path import isdir
import re
import shutil
import socket
import subprocess  # nosec
import sys
from tarfile import TarFile
from typing import Any, Generator, Tuple, Type

import grpc
from logbook import FileHandler, Logger, NestedSetup, StreamHandler  # type: ignore

from hansken_extraction_plugin.runtime.extraction_plugin_server import serve

log = Logger(__name__)


class TestPluginRunner(ABC):
    """
    Abstract base class to encapsulate plugin runners. Subclasses serve a plugin on localhost.
    """
    DEFAULT_PORT = 8999

    @contextmanager
    @abstractmethod
    def serve_localhost(self, port: int = DEFAULT_PORT) -> Generator[Any, None, None]:
        """
        Serve a plugin on localhost.

        :param port: the port to listen on
        :return: a contextmanager which starts and stops the server
        """
        pass


class SimplePluginRunner(TestPluginRunner):
    """
    Runs a plugin on localhost using a grpc Server which runs in it's own thread.
    """
    def __init__(self, plugin_class: Type):
        self._plugin_class = plugin_class

    @contextmanager
    def serve_localhost(self, port: int = TestPluginRunner.DEFAULT_PORT) -> Generator[grpc.Server, None, None]:
        """
        Contextmanager to run (and stop) a plugin, listening on localhost

        :param port: port to listen on
        """
        with serve(self._plugin_class, f'[::]:{port}') as server:
            yield server


class DockerPluginRunner(TestPluginRunner):
    """
    TODO: HANSKEN-14216: This could be improved by using a docker api like https://docker-py.readthedocs.io/en/stable/
    """
    def __init__(self, docker_image: str):
        re_docker_image = re.compile('[a-z0-9]+(?:[._-]{1,2}[a-z0-9]+)*')
        if not re_docker_image.match(docker_image):
            raise ValueError(f'Invalid docker image name: {docker_image}')
        self._docker_image = docker_image

    @contextmanager
    def serve_localhost(self, port: int = TestPluginRunner.DEFAULT_PORT) -> Generator[str, None, None]:
        """Context manager for running a plugin in docker."""
        container_id = ''
        try:
            log.debug('Starting docker container in the background')
            container_id = self._run_docker(port)
            log.info(f'Started docker container {container_id} in the background')
            yield container_id
        finally:
            log.debug('Stopping docker container {}', container_id)
            self._stop_docker(container_id)

    def _run_docker(self, port) -> str:
        if os.path.exists('.cid'):
            log.error('.cid file found from previous run')
            os.remove('.cid')
        cmd = ['docker', 'run', '-d', '--rm',
               '--cidfile', '.cid',
               '-p', f'{str(port)}:8999',
               self._docker_image]

        subprocess.check_output(cmd, stderr=subprocess.STDOUT, shell=False)  # nosec
        return DockerPluginRunner._read_cid()

    @staticmethod
    def _read_cid() -> str:
        return open('.cid', 'r').readlines()[0].strip()

    @staticmethod
    def _stop_docker(container_id: str):
        try:
            cmd = ['docker', 'stop', '-f', '-t', '30', container_id]
            cid = str(subprocess.check_output(cmd, stderr=subprocess.STDOUT, shell=False))  # nosec
            log.info(f'Stopped container {cid}')
            os.remove('.cid')
        except subprocess.CalledProcessError as cpe:
            msg = f'Docker container {container_id} could not be stopped: {cpe}'
            log.error(msg)


class TestFramework(ABC):
    @abstractmethod
    def run(self, host: str, port: int) -> str:
        """
        Run the test framework for a plugin server.

        :param host: the host the plugin server is listening on
        :param port: the port the plugin server is listening on
        """
        pass


class _TestFrameworkWrapper:
    """
    Wrapper around the Extraction Plugins SDK test framework (a Java app).

    Note: check that python has sufficient permissions to execute bash and java.
    """
    TEST_RUNNER_DIR = '.runner'
    DEFAULT_HOST = 'localhost'
    DEFAULT_PORT = 8999

    def __init__(self):
        if not _TestFrameworkWrapper._test_framework_installed():
            version, _ = _TestFrameworkWrapper._test_framework_distinfo()
            log.info('Unpacking test framework version {}', version)
            _TestFrameworkWrapper._install_test_framework()

    @staticmethod
    def _test_framework_installed() -> bool:
        return os.path.exists(_TestFrameworkWrapper._test_framework_jar())

    @staticmethod
    def _clean_runner_dir() -> None:
        if os.path.exists(_TestFrameworkWrapper.TEST_RUNNER_DIR):
            log.debug('Cleaning test-runner directory: {}', _TestFrameworkWrapper.TEST_RUNNER_DIR)
            shutil.rmtree(_TestFrameworkWrapper.TEST_RUNNER_DIR)

    @staticmethod
    def _test_framework_distinfo() -> Tuple[str, str]:
        here = os.path.dirname(os.path.abspath(__file__))
        tgz_file = glob.glob(f'{here}/_resources/test-framework-*-bin.tar.gz', recursive=False)[0]
        version = tgz_file.split('test-framework-')[1].split('-bin')[0]
        return version, tgz_file

    @staticmethod
    def _install_test_framework() -> None:
        _, tgz_file = _TestFrameworkWrapper._test_framework_distinfo()
        log.debug('installing test-framework from: {}', tgz_file)
        downloaded_tgz_file = TarFile.open(tgz_file, 'r:gz')
        downloaded_tgz_file.extractall(_TestFrameworkWrapper.TEST_RUNNER_DIR)

    @staticmethod
    def _test_framework_dir() -> str:
        version, _ = _TestFrameworkWrapper._test_framework_distinfo()
        return f'{_TestFrameworkWrapper.TEST_RUNNER_DIR}/test-framework-{version}'

    @staticmethod
    def _test_framework_jar() -> str:
        version, _ = _TestFrameworkWrapper._test_framework_distinfo()
        return f'{_TestFrameworkWrapper._test_framework_dir()}/test-framework-{version}.jar'

    @staticmethod
    def run(input_dir: str, result_dir: str,
            host: str = DEFAULT_HOST, port: int = DEFAULT_PORT,
            regenerate: bool = False) -> str:
        """
        Run the Extraction Plugin SDK Flits Test Framework against a test plugin server.

        :param input_dir: path to directory with input test data
        :param result_dir: path to directory with result test data
        :param host: the host on which the plugin server is listening
        :param port: the port on which the plugin server is listening
        :param regenerate: do not validate, but *regenerate* (overwrite!) the test results from the input

        :return: the test output - will raise an exception if the plugin is not valid
        """
        # sanity check input and result directories
        if not (isdir(input_dir) and isdir(result_dir)):
            raise FileNotFoundError(f'Both {input_dir} and {result_dir} should be accessible directories.')

        # sanity check host name to protect against code injection through subprocess arguments
        re_hostname = re.compile('([a-zA-Z0-9\\-]*\\.)*[a-zA-Z0-9\\-]*')
        if not re_hostname.match(host):
            raise ValueError(f'Unacceptable host name: {host}')

        # build java command (should run with -Xmx350m)
        cmd = ['java', '-Xmx350m',
               '-jar', _TestFrameworkWrapper._test_framework_jar(),
               '--host', host, '-p', str(port), '-t', input_dir, '-r', result_dir,
               ]
        if regenerate:
            cmd += ['-g']
        try:
            log.debug('Running test-framework for plugin at {}:{}: {}', host, port, cmd)
            # run the integration test suite, exit code 1 indicates a test failure
            stdout = subprocess.check_output(cmd,
                                             shell=False,  # nosec
                                             stderr=subprocess.STDOUT)
            return str(stdout, 'utf-8')
        except subprocess.CalledProcessError as e:
            msg = str(e.output, 'utf-8')
            log.error(msg)
            raise AssertionError(f'Tests failed: {msg}')


class FlitsTestRunner(TestFramework):
    """
    Test Framework which uses the FlitsRunner as backend.
    """
    def __init__(self, input_dir: str, result_dir: str, regenerate: bool = False):
        """
        Specify a test run.

        :param input_dir: the input directory
        :param result_dir: the result directory to validate the plugin output
        :param regenerate: if the contents of the result dir should be re-generated, based on the input
                           Note: regenerating will overwrite result data!
        """
        self._input_dir = input_dir
        self._result_dir = result_dir
        self._regenerate = regenerate
        self._flits_runner = _TestFrameworkWrapper()

    def run(self, host: str = 'localhost', port: int = _TestFrameworkWrapper.DEFAULT_PORT) -> str:
        """
        Run the test framework for a plugin server.

        :param host: the host the plugin server is listening on
        :param port: the port the plugin server is listening on
        """
        return self._flits_runner.run(self._input_dir, self._result_dir, host, port, self._regenerate)


class PluginValidator:
    """
    Validates plugins using the Flits test-framework.
    """
    def __init__(self, test_framework: TestFramework, plugin_runner: TestPluginRunner):
        self._test_framework = test_framework
        self._plugin_runner = plugin_runner

    def validate_plugin(self):
        """
        Validate a single plugin by starting the plugin, running the test framework, and stopping the plugin.

        :return:
        """
        port = find_free_port()
        log.debug('Running plugin port {}', port)
        with self._plugin_runner.serve_localhost(port):
            output = self._test_framework.run('localhost', port)
            if output is not None:
                log.info('Test framework output:\n' + str(output))


def find_free_port() -> int:
    """Utility for finding a free tcp/udp port"""
    with closing(socket.socket(socket.AF_INET, socket.SOCK_STREAM)) as s:
        s.bind(('', 0))
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        return s.getsockname()[1]


@contextmanager
def log_context():
    """
    Contextmanager utility for test log configuration.

    This should be called once from the top level, since it removes the log file each time it is called.
    """
    # setup logging to stdout and .tox/tests.log
    log_file_name = 'tests.log'
    if os.path.exists(log_file_name):
        try:
            os.remove(log_file_name)  # clean log
        except PermissionError:
            log.warn('Could not delete ' + log_file_name)
    log_handler = NestedSetup([
        FileHandler(log_file_name, bubble=False, level='DEBUG', format_string=u'{record.message}'),
        StreamHandler(sys.stdout, bubble=True, level='DEBUG')])

    with log_handler.applicationbound() as context:
        yield context
