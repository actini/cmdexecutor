import sys

sys.path.append('./pyexecutor')

from pyexecutor import Commander
from pyexecutor import Executor

##################
# Executor tests #
##################
python = Executor('python')

# Output

result = python.run('-c print("executor")')

assert(result == 'executor')

# JSON output

result = python.run('-c print("{}")', json_output=True)

assert(result == dict())

###################
# Commander tests #
###################

commander = Commander()

# Output

result = commander.run(executor='echo', args='commander')

assert(result.ok() == True)
assert(result.fail() == False)
assert(result.error() == '')
assert(result.output() == 'commander')

# JSON output

result = commander.run(executor='echo', args='{}')

assert(result.json() == dict())

result = commander.run(executor='echo', args='[]')

assert(result.json() == list())

# Failure
result = commander.run(executor='somethingdonotexist', args='nothing', supress_error = True)

assert(result.fail() == True)
