import os
import subprocess

if 'custom' not in globals():
    from mage_ai.data_preparation.decorators import custom
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test

# Set the path to your local repository (inside the container)
# Assuming the repo is mounted at /home/src/ClimateResilienceDashboard inside the container
REPO_DIR = '/home/src/ClimateResilienceDashboard'

# Set the commit message
COMMIT_MSG = 'Automated commit: Updated LakeLevel.html'

@custom
def git_commit_and_push():
    try:
        # Navigate to the repository directory inside the container
        os.chdir(REPO_DIR)

        # Pull the latest changes from the remote (optional, useful if working in a shared repo)
        subprocess.check_call(['git', 'pull', 'origin', 'main'])

        # Stage all changes (including new HTML files, etc.)
        subprocess.check_call(['git', 'add', '.'])

        # Commit the changes with the provided commit message
        subprocess.check_call(['git', 'commit', '-m', COMMIT_MSG])

        # Push the changes to the remote repository
        subprocess.check_call(['git', 'push', 'origin', 'main'])

        print("Changes committed and pushed successfully!")
    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")
        raise

def git_pull():
    git_username = os.getenv('GIT_USERNAME')
    git_token = os.getenv('GIT_TOKEN')

    # Set the remote URL with username and token for HTTPS authentication
    remote_url = f'https://{git_username}:{git_token}@github.com/your_repo.git'

    try:
        subprocess.check_call(['git', 'pull', remote_url, 'main'])
    except subprocess.CalledProcessError as e:
        print(f"Error pulling from Git: {e}")
        raise

@test
def test_output(output, *args) -> None:
    """
    Template code for testing the output of the block.
    """
    assert output is not None, 'The output is undefined'
