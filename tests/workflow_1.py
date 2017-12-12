import os
import sys
sys.path.insert(0, os.path.abspath('..'))

from westeros.keywords.workflows import Workflows


def main():
    wf = Workflows()
    wf.load_configurations("../etc/global.yaml",
                           "../etc/shared.yaml")
    wf.clean_environment()
    wf.backup_environment()

if __name__ == "__main__":
    main()
