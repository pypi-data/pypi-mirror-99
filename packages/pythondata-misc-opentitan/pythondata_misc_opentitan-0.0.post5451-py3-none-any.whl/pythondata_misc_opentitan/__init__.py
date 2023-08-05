import os.path
__dir__ = os.path.split(os.path.abspath(os.path.realpath(__file__)))[0]
data_location = os.path.join(__dir__, "resources")
src = "https://github.com/lowRISC/opentitan"

# Module version
version_str = "0.0.post5451"
version_tuple = (0, 0, 5451)
try:
    from packaging.version import Version as V
    pversion = V("0.0.post5451")
except ImportError:
    pass

# Data version info
data_version_str = "0.0.post5356"
data_version_tuple = (0, 0, 5356)
try:
    from packaging.version import Version as V
    pdata_version = V("0.0.post5356")
except ImportError:
    pass
data_git_hash = "76e35160386278edee3b4bcc5b5a20656a1f6722"
data_git_describe = "v0.0-5356-g76e351603"
data_git_msg = """\
commit 76e35160386278edee3b4bcc5b5a20656a1f6722
Author: Michael Munday <mike.munday@lowrisc.org>
Date:   Wed Jan 20 16:37:27 2021 +0000

    [sw] Add API for reading and writing Control and Status Registers
    
    Add a new API for reading and writing Control and Status Registers
    (CSRs). This new API allows CSR reads and writes to be mocked
    allowing code using CSRs to be more easily unit tested.
    
    This API and test code is based on a design by Miguel Young (@mcy).
    
    Signed-off-by: Michael Munday <mike.munday@lowrisc.org>

"""

# Tool version info
tool_version_str = "0.0.post95"
tool_version_tuple = (0, 0, 95)
try:
    from packaging.version import Version as V
    ptool_version = V("0.0.post95")
except ImportError:
    pass


def data_file(f):
    """Get absolute path for file inside pythondata_misc_opentitan."""
    fn = os.path.join(data_location, f)
    fn = os.path.abspath(fn)
    if not os.path.exists(fn):
        raise IOError("File {f} doesn't exist in pythondata_misc_opentitan".format(f))
    return fn
