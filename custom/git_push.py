import os
import subprocess
import pathlib

if 'custom' not in globals():
    from mage_ai.data_preparation.decorators import custom
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test

# Set the path to your local repository (inside the container)
REPO_DIR = '/home/src/ClimateResilienceDashboard'

# Set the path to the mounted html folder (inside the container)
html_path = pathlib.Path("/app/output")  # Path inside the container

# Set the commit message
COMMIT_MSG = 'Automated commit: Updated LakeLevel.html'

# Function to check for changes in the html folder
def check_for_changes():
    # Run `git status` to check for changes in the repo
    result = subprocess.run(['git', 'status', '--porcelain'], stdout=subprocess.PIPE)
    changes = result.stdout.decode().strip()

    # If there are changes (any output from `git status`)
    return bool(changes)

@custom
def git_commit_and_push():
    try:
        # Navigate to the repository directory inside the container
        os.chdir(REPO_DIR)

        # Pull the latest changes from the remote (optional, useful if working in a shared repo)
        subprocess.check_call(['git', 'pull', 'mage-repo', 'mb_edits'])

        # Check if there are changes in the html directory
        if check_for_changes():
            print("Changes detected, preparing to commit and push...")

            # Stage all changes (including new HTML files, etc.)
            subprocess.check_call(['git', 'add', '.'])

            # Commit the changes with the provided commit message
            subprocess.check_call(['git', 'commit', '-m', COMMIT_MSG])

            # Push the changes to the remote repository
            subprocess.check_call(['git', 'push', 'mage-repo', 'mb_edits'])

            print("Changes committed and pushed successfully!")
        else:
            print("No changes detected in the html folder. Exiting without commit.")
    
    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")
        raise

# @test
# def test_output(output, *args) -> None:
#     """
#     Template code for testing the output of the block.
#     """
#     assert output is not None, 'The output is undefined'
