import json
import subprocess

from exceptions import CommanderException


class Commander():
    _output = ''
    _error = ''
    _returncode = 0
    _logger = None

    def __init__(self, logger=None):
        self._set_logger(logger)

    """
    Run command with sub process
    """
    def run(self, cmd, supress_error=False):
        self._log_info('Start running command {} with supress error {}'.format(cmd, supress_error))

        try:
            result = subprocess.run(cmd.strip().split(' '), capture_output=True)
            self._output = result.stdout
            self._error = result.stderr

            if result.returncode != 0:
                raise CommanderException(result.stderr)

            return self
        except Exception as e:
            self._returncode = 1

            if supress_error:
                return self
            raise e

    """
    Get output message
    """
    def output(self):
        return self._output.decode("utf8").strip()

    """
    Get output message in JSON format
    """
    def json(self):
        try:
            return json.loads(self.output())
        except Exception as e:
            raise CommanderException('invalid JSON string "{}"'.format(self._output))

    """
    Get error message
    """
    def error(self):
        return self._error.decode("utf8").strip()

    """
    Return code is 0
    """
    def success(self):
        return self._returncode == 0

    """
    Return code is not 0
    """
    def fail(self):
        return self._returncode != 0

    """
    Print log info messages
    """
    def _log_info(self, message):
        if self._logger is not None:
            self._logger.info("COMMANDER: %s", message)

    """
    Print log error messages
    """
    def _log_error(self, message):
        if self._logger is not None:
            self._logger.error("COMMANDER: %s", message)

    """
    Print log warning messages
    """
    def _log_warning(self, message):
        if self._logger is not None:
            self._logger.warning("COMMANDER: %s", message)

    """
    Set the command logger
    """
    def _set_logger(self, logger):
        self._logger = logger
