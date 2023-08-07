from base.job import InvalidJobTypeException

class BackgroundJobRunner:
    @staticmethod
    def run(jobs_map: dict, data: dict):
        """
        @:param data received after dump
        @:param jobs_map job instance mapping
        """
        job_type_name = data["job_type"]
        job = jobs_map.get(job_type_name, None)

        if not job:
            raise InvalidJobTypeException(f"Unable to find job '{job_type_name}' in the list of modules")


        return job().run(data["data"])

