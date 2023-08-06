# Copyright 2020, Aiven, https://aiven.io/
#
# This file is under the Apache License, Version 2.0.
# See the file `LICENSE` for details.

from aiven.client.argx import arg, CommandLineTool


class TestCLI(CommandLineTool):
    @arg()
    def xxx(self):
        """7"""

    @arg()
    def aaa(self):
        """1"""

    @arg()
    def ccc(self):
        """4"""


class SubCLI(CommandLineTool):
    @arg()
    def yyy(self):
        """8"""

    @arg()
    def bbb(self):
        """2"""

    @arg()
    def ddd(self):
        """5"""


class SubCLI2(CommandLineTool):
    @arg()
    def yyz(self):
        """9"""

    @arg()
    def bbc(self):
        """3"""

    @arg()
    def dde(self):
        """6"""


def test_extended_commands_remain_alphabetically_ordered():
    cli = TestCLI("testcli")
    cli.extend_commands(cli)  # Force the CLI to have its full arg set at execution

    sl2 = SubCLI2("subcli2")
    sl = SubCLI("subcli")

    cli.extend_commands(sl2)
    cli.extend_commands(sl)

    action_order = [item.dest for item in cli.subparsers._choices_actions]  # pylint: disable=protected-access
    assert action_order == ["aaa", "bbb", "bbc", "ccc", "ddd", "dde", "xxx", "yyy", "yyz"]
