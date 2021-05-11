import sys

sys.path.append('./pyexecutor')

from pyexecutor import Commander
from pyexecutor import Executor

##################
# Executor tests #
##################
python = Executor('python')

# Output

result = python.run(' -c print("executor")')

assert(result == 'executor')

# JSON output

result = python.run(' {}', json_output=True)

assert(result == dict())

###################
# Commander tests #
###################

commander = Commander()

# Output

result = commander.run('echo commander')

assert(result.success() == True)
assert(result.fail() == False)
assert(result.error() == '')
assert(result.output() == 'commander')

# JSON output

result = commander.run('echo {}')

assert(result.json() == dict())

# Failure
result = commander.run('somethingdonotexist nothing', supress_error = True)

assert(result.fail() == True)
