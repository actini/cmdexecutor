import sys
import unittest
from unittest.mock import MagicMock
from unittest.mock import patch

sys.path.append('./pyexecutor')

from pyexecutor import Commander
from pyexecutor.exceptions import CommanderException

class TestCommander(unittest.TestCase):
    @patch('subprocess.run')
    @patch('subprocess.CompletedProcess')
    def test_success(self, mock_subprocess_completedprocess, mock_subprocess_run):
        mock_subprocess_completedprocess.stdout = b'{"test": true}'
        mock_subprocess_completedprocess.stderr = b''
        mock_subprocess_completedprocess.returncode = 0
        mock_subprocess_run.return_value = mock_subprocess_completedprocess

        commander = Commander()
        commander.run("python --version")

        mock_subprocess_run.assert_called_once()
        assert(commander.output() == '{"test": true}')
        assert(commander.json()['test'])
        assert(commander.error() == "")
        assert(commander.ok())
        assert(not commander.fail())

    @patch('subprocess.run')
    @patch('subprocess.CompletedProcess')
    def test_failure(self, mock_subprocess_completedprocess, mock_subprocess_run):
        mock_subprocess_completedprocess.stdout = b''
        mock_subprocess_completedprocess.stderr = b'error'
        mock_subprocess_completedprocess.returncode = 1
        mock_subprocess_run.return_value = mock_subprocess_completedprocess

        with self.assertRaises(CommanderException):
            commander = Commander()
            commander.run("python --version")

            mock_subprocess_run.assert_called_once()
            assert(commander.output() == '')
            assert(commander.json()['test'])
            assert(commander.error() == "error")
            assert(not commander.ok())
            assert(commander.fail())

if __name__ == '__main__':
    unittest.main()