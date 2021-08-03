import sys
import unittest
from unittest.mock import MagicMock
from unittest.mock import patch

sys.path.append('./pyexecutor')

from pyexecutor import Executor, Commander, ExecutorException, CommanderException


class TestCommander(unittest.TestCase):
    @patch('subprocess.run')
    @patch('subprocess.CompletedProcess')
    def test_run_success(self, mock_subprocess_completedprocess, mock_subprocess_run):
        mock_subprocess_completedprocess.stdout = b'success'
        mock_subprocess_completedprocess.stderr = b''
        mock_subprocess_completedprocess.returncode = 0
        mock_subprocess_run.return_value = mock_subprocess_completedprocess

        commander = Commander()
        commander.run(executor='something')

        mock_subprocess_run.assert_called_once()
        assert(commander.output() == 'success')
        assert(commander.error() == '')
        assert(commander.ok())
        assert(not commander.fail())

    @patch('subprocess.run')
    @patch('subprocess.CompletedProcess')
    def test_run_failure(self, mock_subprocess_completedprocess, mock_subprocess_run):
        mock_subprocess_completedprocess.stdout = b''
        mock_subprocess_completedprocess.stderr = b'error'
        mock_subprocess_completedprocess.returncode = 1
        mock_subprocess_run.return_value = mock_subprocess_completedprocess

        with self.assertRaises(CommanderException):
            commander = Commander()
            commander.run(executor='something')

            mock_subprocess_run.assert_called_once()
            assert(commander.output() == '')
            assert(commander.error() == 'error')
            assert(not commander.ok())
            assert(commander.fail())

    @patch('subprocess.run')
    @patch('subprocess.CompletedProcess')
    def test_json_output(self, mock_subprocess_completedprocess, mock_subprocess_run):
        mock_subprocess_completedprocess.stdout = b'{"test": true}'
        mock_subprocess_completedprocess.stderr = b''
        mock_subprocess_completedprocess.returncode = 0
        mock_subprocess_run.return_value = mock_subprocess_completedprocess

        commander = Commander()
        commander.run(executor='something')

        assert(commander.json().get('test') is True)

class TestExecutor(unittest.TestCase):
    @patch('pyexecutor.Executor._set_executor')
    @patch('subprocess.run')
    @patch('subprocess.CompletedProcess')
    def test_init(self, mock_subprocess_completedprocess, mock_subprocess_run, mock_executor_setter):
        mock_subprocess_completedprocess.stdout = b'/usr/bin/python'
        mock_subprocess_completedprocess.stderr = b''
        mock_subprocess_completedprocess.returncode = 0
        mock_subprocess_run.return_value = mock_subprocess_completedprocess

        python = Executor('python')

        mock_executor_setter.assert_called_once()

    @patch('subprocess.run')
    @patch('subprocess.CompletedProcess')
    def test_run_success(self, mock_subprocess_completedprocess, mock_subprocess_run):
        mock_subprocess_completedprocess.stdout = b'/usr/bin/python'
        mock_subprocess_completedprocess.stderr = b''
        mock_subprocess_completedprocess.returncode = 0
        mock_subprocess_run.return_value = mock_subprocess_completedprocess

        python = Executor('python')

        mock_subprocess_completedprocess.stdout = b'3.6'
        mock_subprocess_completedprocess.stderr = b''
        mock_subprocess_completedprocess.returncode = 0
        mock_subprocess_run.return_value = mock_subprocess_completedprocess

        result = python.run('--version')

        assert(result == '3.6')

    @patch('subprocess.run')
    @patch('subprocess.CompletedProcess')
    def test_run_failure(self, mock_subprocess_completedprocess, mock_subprocess_run):
        mock_subprocess_completedprocess.stdout = b'/usr/bin/python'
        mock_subprocess_completedprocess.stderr = b''
        mock_subprocess_completedprocess.returncode = 0
        mock_subprocess_run.return_value = mock_subprocess_completedprocess

        python = Executor('python')

        with self.assertRaises(ExecutorException):
            mock_subprocess_completedprocess.stdout = b''
            mock_subprocess_completedprocess.stderr = b'error'
            mock_subprocess_completedprocess.returncode = 1
            mock_subprocess_run.return_value = mock_subprocess_completedprocess

            python.run("--version")

    @patch('subprocess.run')
    @patch('subprocess.CompletedProcess')
    def test_json_output(self, mock_subprocess_completedprocess, mock_subprocess_run):
        mock_subprocess_completedprocess.stdout = b'/usr/bin/python'
        mock_subprocess_completedprocess.stderr = b''
        mock_subprocess_completedprocess.returncode = 0
        mock_subprocess_run.return_value = mock_subprocess_completedprocess

        python = Executor('python')

        mock_subprocess_completedprocess.stdout = b'{"version": 3.6}'
        mock_subprocess_completedprocess.stderr = b''
        mock_subprocess_completedprocess.returncode = 0
        mock_subprocess_run.return_value = mock_subprocess_completedprocess

        result = python.run('--version', True)

        assert(result.get('version') == 3.6)

    @patch('subprocess.run')
    @patch('subprocess.CompletedProcess')
    def test_set_trailer(self, mock_subprocess_completedprocess, mock_subprocess_run):
        mock_subprocess_completedprocess.stdout = b'/usr/bin/python'
        mock_subprocess_completedprocess.stderr = b''
        mock_subprocess_completedprocess.returncode = 0
        mock_subprocess_run.return_value = mock_subprocess_completedprocess

        python = Executor('python')
        python.set_trailer('--debug')

        mock_subprocess_completedprocess.stdout = b'{"version": 3.6}'
        mock_subprocess_completedprocess.stderr = b''
        mock_subprocess_completedprocess.returncode = 0
        mock_subprocess_run.return_value = mock_subprocess_completedprocess

        result = python.run('--version')

        mock_subprocess_run.assert_called_with(['/usr/bin/python', '--version', '--debug'], capture_output=True)


if __name__ == '__main__':
    unittest.main()