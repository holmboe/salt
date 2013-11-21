# -*- coding: utf-8 -*-

# Get instant unit test feedback during development. Inspired by Gary
# Bernhardt's talk about "Fast Test, Slow Test".

# Pre-requisites:
#
#    pip install sniffer
#
# If you use Linux, you'll need to install pyinotify
# If you use Windows, you'll need to install pywin32
# If you use Mac OS X 10.5+ (Leopard), you'll need to install MacFSEvents
#
# For notification system (libnotify, etc) support, see
# https://github.com/jeffh/sniffer/

# Usage:
#
#    cd tests; \ # one of the below
#    sniffer
#    sniffer -xunit.modules.virt_test
#    sniffer -xunit.modules.virt_test -xunit.modules.file_test

from sniffer.api import *
from subprocess import call
import os, termstyle

# Customize the pass/fail colors
pass_fg_color = termstyle.green
pass_bg_color = termstyle.bg_default
fail_fg_color = termstyle.red
fail_bg_color = termstyle.bg_default

# Watch these directories for changes.
watch_paths = (
    os.path.join('..', 'salt'),
    'unit',
)

# The file_validator gets invoked on every file that gets changed in
# the watched paths. Return True to invoke any runnable functions,
# False otherwise.
@file_validator
def py_files(filename):
    return all([
        filename.endswith('.py'),
        not os.path.basename(filename).startswith('.'),
    ])

# A runnable gets invoked for verification. This is ideal for running
# tests of some sort. For anything you want to get constantly
# reloaded, do an import in the function.
#
# sys.argv[0] and any arguments passed via -x prefix will be sent to
# this function as it's arguments. The function should return
# logically True if the validation passed and logicially False if it
# fails.
@runnable
def execute_salt_unit_tests(*args):
    if len(args) > 1:
        names = [' --name {0}'.format(m) for m in args[1:]]
        return call(
            'python runtests.py {0}'.format(''.join(names)),
            shell=True
        ) == 0
    else:
        return call(
            'python runtests.py --unit-tests',
            shell=True
        ) == 0
