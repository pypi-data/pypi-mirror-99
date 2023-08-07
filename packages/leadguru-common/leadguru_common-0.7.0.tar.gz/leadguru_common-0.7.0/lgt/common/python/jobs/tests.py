import json
import unittest
from base import BaseBackgroundJob, BackgroundJobRunner
from jobs.simple_job import SimpleTestJob

class JobDataTest(unittest.TestCase):
    def test_can_run_simple_job(self):
        job_type = SimpleTestJob
        data = { "name": "Kiryl", "id": 123 }

        job = job_type()
        result = job.run(data)

        self.assertEqual(f"id=123;name=Kiryl", result)

    def test_can_run_serialized_job(self):
        job_type = SimpleTestJob
        data = {"name": "Kiryl", "id": 123}

        json_data = json.dumps(BaseBackgroundJob.dumps(job_type, data))

        result = BackgroundJobRunner.run({
            "SimpleTestJob": SimpleTestJob
        }, json.loads(json_data))

        self.assertEqual(f"id=123;name=Kiryl", result)






