import os
import time
import string
import random

import pytest
import python_pachyderm

_test_pachyderm_version = None

def test_pachyderm_version():
    global _test_pachyderm_version

    if _test_pachyderm_version is None:
        value = os.environ.get("PACHYDERM_VERSION")

        if value is None:
            client = python_pachyderm.Client()
            value = client.get_remote_version()
            _test_pachyderm_version = (value.major, value.minor, value.micro)
        else:
            _test_pachyderm_version = tuple(int(i) for i in value.split("."))

    return _test_pachyderm_version

def skip_if_below_pachyderm_version(major, minor, revision):
    test = test_pachyderm_version() < (major, minor, revision)
    reason = "requires pachyderm {}.{}.{} or higher".format(major, minor, revision)
    return pytest.mark.skipif(test, reason=reason)

def skip_if_no_enterprise():
    test = os.environ.get("PACH_PYTHON_ENTERPRISE_CODE") == None
    return pytest.mark.skipif(test, reason="enterprise code not available")

def random_string(n):
    return "".join(random.choice(string.ascii_lowercase + string.digits) for _ in range(n))

def test_repo_name(test_name, prefix=None, suffix=None):
    prefix = "" if prefix is None else "{}-".format(prefix)
    suffix = suffix or random_string(6)
    return "{}{}-{}".format(prefix, test_name, suffix)

def create_test_repo(client, test_name, prefix=None, suffix=None):
    repo_name = test_repo_name(test_name, prefix=prefix, suffix=suffix)
    client.create_repo(repo_name, "python_pachyderm test repo for {}".format(test_name))
    return repo_name

def create_test_pipeline(client, test_name):
    repo_name_suffix = random_string(6)
    input_repo_name = create_test_repo(client, test_name, prefix="input", suffix=repo_name_suffix)
    pipeline_repo_name = test_repo_name(test_name, prefix="pipeline", suffix=repo_name_suffix)

    client.create_pipeline(
        pipeline_repo_name,
        transform=python_pachyderm.Transform(cmd=["sh"], image="alpine", stdin=["cp /pfs/{}/*.dat /pfs/out/".format(input_repo_name)]),
        input=python_pachyderm.Input(pfs=python_pachyderm.PFSInput(glob="/*", repo=input_repo_name)),
        enable_stats=True,
    )

    with client.commit(input_repo_name, 'master') as commit:
        client.put_file_bytes(commit, 'file.dat', b'DATA')

    return (commit, input_repo_name, pipeline_repo_name)

def wait_for_job(client, commit):
    # block until the commit is ready
    client.inspect_commit(commit, block_state=python_pachyderm.CommitState.READY.value)

    # while the commit is ready, the job might not be listed on the first
    # call, so repeatedly list jobs until it's available
    start_time = time.time()
    while True:
        for job in client.list_job():
            return job.job.id

        assert time.time() - start_time < 60.0, "timed out waiting for job"
        time.sleep(1)

def get_cluster_deployment_id():
    client = python_pachyderm.Client()
    cluster_info = client.inspect_cluster()
    return cluster_info.deployment_id
