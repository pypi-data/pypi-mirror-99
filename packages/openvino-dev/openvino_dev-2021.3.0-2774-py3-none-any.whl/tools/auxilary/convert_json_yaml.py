#
# Copyright 2020-2021 Intel Corporation.
#
# This software and the related documents are Intel copyrighted materials,
# and your use of them is governed by the express license under which they
# were provided to you (End User License Agreement for the Intel(R) Software
# Development Products (Version October 2018)). Unless the License provides
# otherwise, you may not use, modify, copy, publish, distribute, disclose or
# transmit this software or the related documents without Intel's prior
# written permission.
#
# This software and the related documents are provided as is, with no
# express or implied warranties, other than those that are expressly
# stated in the License.

from pathlib import Path
import sys

sys.path.insert(0, Path(__file__).resolve().parent.parent.parent.as_posix()) # pylint: disable=C0413
from compression.utils.config_reader import read_config_from_file, write_config_to_file

src = Path(sys.argv[1])
dst = Path(sys.argv[2])

data = read_config_from_file(src)
write_config_to_file(data, dst)
