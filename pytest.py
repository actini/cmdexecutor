import sys

sys.path.append('./pyexecutor')

from pyexecutor import Commander
from pyexecutor import Executor

##################
# Executor tests #
##################
echo = Executor('echo')

# Output

result = echo.run('executor')

assert(result == 'executor')

# JSON output

result = echo.run('{}', json_output=True)

assert(result == dict())

###################
# Commander tests #
###################

commander = Commander()

# Output

result = commander.run('echo commander')

assert(result.ok())
assert(result.has_error() == False)
assert(result.has_warning() == False)
assert(result.error() == None)
assert(result.warning() == None)
assert(result.output() == 'commander')

# JSON output

result = commander.run('echo {}')

assert(result.json() == dict())

# Warning

result = commander.run('echo warning 1>&2')

assert(result.has_warning())
assert(result.warning() == 'warning')

# Error

result = commander.run('echo error 1>&2')

assert(result.has_error())
assert(result.error() == 'error')
