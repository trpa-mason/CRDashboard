import subprocess

if 'custom' not in globals():
    from mage_ai.data_preparation.decorators import custom
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test


@custom
def git_pull():
    try:
        subprocess.check_call(['git', 'pull', 'origin', 'main'])
    except subprocess.CalledProcessError as e:
        print(f"Error pulling from Git: {e}")
        raise


@test
def test_output(output, *args) -> None:
    """
    Template code for testing the output of the block.
    """
    assert output is not None, 'The output is undefined'
