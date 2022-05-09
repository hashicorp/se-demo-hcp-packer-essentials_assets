import os, json, subprocess
from watchfiles import run_process, DefaultFilter, Change

TF_DIR = os.getenv('TF_DIR')
WATCHDOG_HOME = os.getenv('WATCHDOG_HOME')

def terraform_plan():

    changes = os.getenv('WATCHFILES_CHANGES')
    changes = json.loads(changes)

    if changes:
        # global WATCHDOG_HOME
        subprocess.run(["".join(WATCHDOG_HOME + '/tf-watchdog-automation.bash')])

    return

class TerraformFilter(DefaultFilter):
    allowed_extensions = '.tf'

    def __call__(self, change: Change, path: str) -> bool:
        return (
            super().__call__(change, path) and 
            path.endswith(self.allowed_extensions)
        )

def only_added(change: Change, path: str) -> bool:
    return change == Change.added

if __name__ == '__main__':
    
    run_process("".join(TF_DIR), target=terraform_plan, watch_filter=TerraformFilter())