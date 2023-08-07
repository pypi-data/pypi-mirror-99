from base.job import (BaseBackgroundJobData, BaseBackgroundJob, InvalidJobTypeException)
from base.runner import (BackgroundJobRunner)
from simple_job import (SimpleTestJobData, SimpleTestJob)

#jobs
SimpleTestJob = SimpleTestJob

# module classes
SimpleTestJob = SimpleTestJob
BackgroundJobRunner = BackgroundJobRunner
BaseBackgroundJobData = BaseBackgroundJobData
BaseBackgroundJob = BaseBackgroundJob
InvalidJobTypeException = InvalidJobTypeException

jobs_map = {
    "SimpleTestJob": SimpleTestJob
}
