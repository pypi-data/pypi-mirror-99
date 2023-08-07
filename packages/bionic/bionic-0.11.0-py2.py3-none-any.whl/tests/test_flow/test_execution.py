import pytest

import os


@pytest.mark.allows_parallel
def test_execution_mode(builder, parallel_execution_enabled):
    @builder
    def pid():
        return os.getpid()

    current_pid = os.getpid()
    returned_pid = builder.build().get("pid")

    if parallel_execution_enabled:
        current_pid != returned_pid
    else:
        current_pid == returned_pid
