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


import datetime


def get_timestamp():
    return datetime.datetime.strftime(
        datetime.datetime.now(), '%Y-%m-%d_%H-%M-%S')


def get_timestamp_precise():
    return datetime.datetime.strftime(
        datetime.datetime.now(), '%Y-%m-%d_%H-%M-%S.%f')


def get_timestamp_short():
    return datetime.datetime.strftime(
        datetime.datetime.now(), '%H-%M-%S')
