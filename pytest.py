import sys

sys.path.append('./pyexecutor')

from pyexecutor import Commander
from pyexecutor import Executor

##################
# Executor tests #
##################
python = Executor('python3')

# Output

result = python.run(' -c print("executor")')

assert(result == 'executor')

# JSON output

result = python.run(' -c print("{}")', json_output=True)

assert(result == dict())

###################
# Commander tests #
###################

commander = Commander()

# Output

result = commander.run('python3 -c print("commander")')

assert(result.success() == True)
assert(result.fail() == False)
assert(result.error() == '')
assert(result.output() == 'commander')

# JSON output

result = commander.run('python3 -c print("{}")')

assert(result.json() == dict())

# Error

result = commander.run('python3 -c print("failure!", file=sys.stderr); exit 1;', supress_error = True)

assert(result.fail() == True)
assert(result.error() == 'failure!')
