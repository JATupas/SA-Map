import subprocess
from pathlib import Path

    
def run_oq_jobs(directory_path):
    directory = Path(directory_path)
    folders = [str(folder) for folder in directory.glob('*') if folder.is_dir()]

    for folder in folders:
        subprocess.run(
            ["oq", "engine", "--run", str(folder) + "/job.ini"],
            shell=True
        )
        print(folder)
    print("Done!")

# run_oq_jobs("C:/Users/shade/Downloads/SHADE App/demos - Copy/Openquake Calculator/OQ_TEST/")