class JobControl:
    def __init__(self):
        self.jobs = {}
        
    def add_job(self, pid, command):
        """Add background job"""
        self.jobs[pid] = {'command': command, 'status': 'running'}
        
    def list_jobs(self):
        """List all background jobs"""
        return self.jobs