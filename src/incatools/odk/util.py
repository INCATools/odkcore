# odkcore - Ontology Development Kit Core
# Copyright © 2025 ODK Developers
#
# This file is part of the ODK Core project and distributed under the
# terms of a 3-clause BSD license. See the LICENSE file in that project
# for the detailed conditions.

import logging
import re
import subprocess
from pathlib import Path


def runcmd(cmd: str) -> None:
    """Runs a command in a new process.

    An exception will be thrown if the command fails for any reason.

    :param cmd: The command to run.
    """
    logging.info("RUNNING: {}".format(cmd))
    p = subprocess.Popen(
        [cmd],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        shell=True,
        universal_newlines=True,
    )
    (out, err) = p.communicate()
    logging.info("OUT: {}".format(out))
    if err:
        logging.error(err)
    if p.returncode != 0:
        raise Exception("Failed: {}".format(cmd))


def grep(file: Path, needle: str) -> bool:
    """Searches for a pattern anywhere in a file,

    :param file: The file to grep into.
    :param needle: The pattern to look for.
    :returns: True if the file contains the pattern.
    """
    pattern = re.compile(needle)
    with file.open("r") as fd:
        for line in fd:
            if pattern.search(line):
                return True
    return False
