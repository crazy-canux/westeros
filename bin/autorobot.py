#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
SUMMARY autorobot.py

Copyright (C) 2017 Canux CHENG.
All rights reserved.

LICENSE GNU General Public License v3.0.

:author: Canux CHENG canuxcheng@gmail.com
:version: V1.0.0
:since: 08 14 2017 15:58:22

DESCRIPTION:
"""
import argparse
import imp
import inspect
import os
import sys
from collections import OrderedDict
from distutils.util import strtobool
from functools import partial
from time import localtime, strftime

import robot
import yaml
from colorama import Fore, init as colorinit
from robot.parsing.model import TestData

_DEBUG_ = bool(sys.flags.debug) or (
    'pydevd.py' in str(inspect.stack()[-1])
)

ROBOT_HOME_DIR = os.path.expanduser('~/automation/robot')
ROBOT_CONF_DIR = os.path.join(ROBOT_HOME_DIR, 'etc')
ROBOT_SRC_DIR = os.path.join(ROBOT_HOME_DIR, 'robot')

if not os.path.exists(ROBOT_SRC_DIR):
    _, ROBOT_PKG_PATH, __ = imp.find_module('automation')

    ROBOT_CONF_DIR = os.path.join(ROBOT_PKG_PATH, 'workflow/etc')
    ROBOT_SRC_DIR = os.path.join(ROBOT_PKG_PATH, 'workflow/robot')

    if _DEBUG_ and not os.path.exists(ROBOT_CONF_DIR):
        ROBOT_CONF_DIR = os.path.realpath(
            os.path.join(ROBOT_PKG_PATH, '../etc')
        )

GLOBAL_SETTINGS_FILE = os.path.join(ROBOT_CONF_DIR, 'global.yaml')

class Color(object):
    colorinit()

    RED = partial(
        lambda info, color=Fore.RESET:
        color + str(info) + Fore.RESET,
        color=Fore.RED
    )

    BLUE = partial(
        lambda info, color=Fore.RESET:
        color + str(info) + Fore.RESET,
        color=Fore.BLUE
    )

    GREEN = partial(
        lambda info, color=Fore.RESET:
        color + str(info) + Fore.RESET,
        color=Fore.GREEN
    )

    YELLOW = partial(
        lambda info, color=Fore.RESET:
        color + str(info) + Fore.RESET,
        color=Fore.YELLOW
    )

    CYAN = partial(
        lambda info, color=Fore.RESET:
        color + str(info) + Fore.RESET,
        color=Fore.CYAN
    )

    MAGENTA = partial(
        lambda info, color=Fore.RESET:
        color + str(info) + Fore.RESET,
        color=Fore.MAGENTA
    )

    RESET = partial(
        lambda info, color=Fore.RESET:
        color + str(info) + Fore.RESET,
        color=Fore.RESET
    )


class Workflow(object):
    def __init__(self, name, doc, tags, robotsteps):
        self.name = name
        self.doc = doc
        self.tags = tags
        self.keywords = self.__parse_robot_steps(robotsteps)

    def __parse_robot_steps(self, robotsteps):
        keywords = []
        for s in robotsteps:
            if hasattr(s, 'name'):
                if s.args:
                    keywords.append(
                        '{step} {args}'.format(
                            step=s.name, args=str(','.join(s.args))
                        )
                    )
                else:
                    keywords.append('{step}'.format(step=s.name))
        return keywords


class AutoTest(object):
    def __init__(self, source=ROBOT_SRC_DIR):
        self.robot_sources = []
        self.test_suites = self.load_robot_source(source)

        self.__workflowdict = None

    def load_robot_source(self, source):
        if os.path.isfile(source):
            self.robot_sources.append(source)
        else:
            if os.path.isdir(source):
                for root, _, files in os.walk(source):
                    self.robot_sources += [
                        os.path.join(root, _file)
                        for _file in files
                        if _file.endswith('.robot') or
                           _file.endswith('.txt') or
                           _file.endswith('.html')
                    ]

        if self.robot_sources:
            return [
                TestData(source=source)
                for source in self.robot_sources
            ]
        else:
            raise ValueError('No workflow file was found')

    def __init_workflow_dict(self):
        _dict = OrderedDict()

        for suite in self.test_suites:
            for case in suite.testcase_table:
                _dict[case.name] = Workflow(
                    case.name,
                    case.doc.value,
                    case.tags,
                    case.steps
                )

        return _dict

    @property
    def workflowdict(self):
        if not self.__workflowdict:
            self.__workflowdict = self.__init_workflow_dict()
        return self.__workflowdict

    @property
    def workflowlist(self):
        return [str(k) for k in self.workflowdict.keys()]

    @workflowlist.setter
    def workflowlist(self, value):
        return self.workflowdict.keys().extend(value)

    def get_workflow_name(self, value=''):
        return self.workflowlist[int(value) - 1]

    def get_workflow_by_tags(self, tags):
        workflowlist = []
        for case_name in self.workflowlist:
            if set(
                    [tag.upper() for tag in tags]
            ) & set(
                [tag.upper()
                 for tag in self.workflowdict.get(
                    case_name
                ).tags]
            ):
                workflowlist.append(case_name)
        return workflowlist

    def get_workflow_by_name(self, names):
        workflowlist = []
        for name in names:
            for case_name in self.workflowlist:
                if name.split('*')[0] in case_name:
                    workflowlist.append(case_name)
        return workflowlist

    def remove_workflow_by_tags(self, wflist, tags):
        workflowlist = []
        for case_name in wflist:
            if not set(
                    [tag.upper() for tag in tags]
            ) & set(
                [tag.upper()
                 for tag in self.workflowdict.get(
                    case_name
                ).tags]
            ):
                workflowlist.append(case_name)
        return workflowlist


class ConfigYaml(object):
    def __init__(self, yamlpath=GLOBAL_SETTINGS_FILE):
        self.yamlpath = yamlpath
        self.data = self.load_config()

    def load_config(self):
        if not os.path.isfile(self.yamlpath):
            print Color.YELLOW(
                'Unable to identify global settings.\n'
                'Try to use default settings now...\n'
            )

            return self.__ordered_load(
                u"""
                key: value
                """,
                yaml.SafeLoader
            )

        with open(self.yamlpath, 'r') as f:
            return self.__ordered_load(f, yaml.SafeLoader)

    def save_config(self, savedata=None):
        try:
            with open(self.yamlpath, 'w') as f:
                self.__ordered_dump(
                    savedata or self.data,
                    f,
                    Dumper=yaml.SafeDumper
                )
        except IOError as ex:
            print Color.RED(ex.message)

    def __ordered_load(
            self, stream,
            Loader=yaml.Loader,
            object_pairs_hook=OrderedDict
    ):
        class OrderedLoader(Loader):
            pass

        def construct_mapping(loader, node):
            loader.flatten_mapping(node)
            return object_pairs_hook(loader.construct_pairs(node))

        OrderedLoader.add_constructor(
            yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG,
            construct_mapping)
        return yaml.load(stream, OrderedLoader)

    def __ordered_dump(
            self, data, stream=None,
            Dumper=yaml.Dumper, **kwds
    ):
        class OrderedDumper(Dumper):
            pass

        def _dict_representer(dumper, data):
            return dumper.represent_mapping(
                yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG,
                data.items())

        OrderedDumper.add_representer(
            OrderedDict, _dict_representer
        )

        return yaml.dump(
            data, stream, OrderedDumper, **kwds
        )

    def data_to_str(self, printdata=None, keylist=None):
        printdata = printdata or self.data
        retstr = ''
        for k, v in printdata.iteritems():
            if (not keylist) or (keylist and k in keylist):
                if isinstance(v, OrderedDict):
                    retstr += '%s :\n' % (k)
                    for kk, vv in v.iteritems():
                        retstr += '  %s : %s\n' % (kk, vv)
                else:
                    retstr += '%s : %s\n' % (k, v)

        return retstr


class Helper(object):
    @staticmethod
    def parse_input(inputval, inputtype):
        inputval = inputval.strip()
        if len(inputval) == 0:
            return False
        if inputtype == 'list':
            return [s.strip() for s in inputval.split(',')]
        else:
            return inputval

    @staticmethod
    def query_yes_no(question):
        print question + Color.RED(
            ' [yes(y)/no(n)]'
        ) + ' or ' + Color.RED('[true(t)/false(f)]\n')

        while True:
            try:
                return strtobool(raw_input().lower())
            except ValueError:
                print Color.RED(
                    'Please respond with yes(y)/no(n) '
                    'or true(t)/false(f)...\n'
                )

    @staticmethod
    def get_similiar_value(inputval, listval):
        from difflib import get_close_matches
        close_commands = get_close_matches(inputval, listval)
        if close_commands:
            return close_commands
        else:
            return False


class Output(object):
    def __init__(self, filepath):
        self.terminal = sys.stdout
        self.filepath = filepath
        self.__file = None

    def __enter__(self):
        self.__file = open(self.filepath, "w")
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.__file:
            self.__file.close()
            self.__file = None

    def close(self):
        self.__exit__(None, None, None)

    def write(self, message):
        if not self.__file:
            self.__enter__()
        self.__file.write(message)
        self.terminal.write(message)

    def flush(self):
        self.__file.flush()
        self.terminal.flush()


class ArgParse(object):
    def __init__(self):
        self._parserbase = argparse.ArgumentParser(add_help=False)
        self.parsecmd = argparse.ArgumentParser(
            prog='AutoCLI',
            description='%(prog)s, '
                        'Analytic Insights Module Automation',
            epilog="Automation End-to-End Verification",
            parents=[self._parserbase],
            add_help=False
        )
        self.autotest = AutoTest()
        self.config = ConfigYaml()
        self.args = None
        self.__init_arguments()

    def __init_arguments(self):
        self._group = self.parsecmd.add_argument_group(
            'General Options'
        )
        self._group.add_argument(
            '-v', '--version',
            action='version',
            version='%(prog)s 0.6.0'
        )
        self._group.add_argument(
            '-h', '--help',
            action='help',
            help='show {command} help'
        )

        self._subparsers = self.parsecmd.add_subparsers(
            title='Command Options', dest='cmdopt'
        )  # ,description='')

        self._parseworkflow = self._subparsers.add_parser(
            'workflow', help='List/Run Automation workflows'
        )
        self._parseworkflow.add_argument(
            '-l', '--list',
            action='store_const',
            const=self.autotest.workflowlist,
            help='List all workflow(s)'
        )
        self._parseworkflow.add_argument(
            '-a', '--all',
            action='store_const',
            const=self.autotest.workflowlist,
            help='Run all workflow(s)'
        )
        self._parseworkflow.add_argument(
            '-v', '--verbose',
            action='store_true',
            help='Generate test report with verbose messages/embedded screenshots',
        )
        self._parseworkflow.add_argument(
            '-s', '--show',
            nargs='+',
            # metavar='',
            # choices=self.choices,
            help='Show detail steps of specified workflow(s) with one-based indices.',
            dest='show'
        )
        self._parseworkflow.add_argument(
            '-r', '--run',
            nargs='+',
            # metavar='',
            # choices=self.choices,
            default=[],
            dest='run',
            help='Run specific workflow(s) with one-based indices.'
        )
        self._parseworkflow.add_argument(
            '-t', '--test',
            nargs='+',
            default=[],
            help='Run specific workflow(s) with partial name(s). '
                 'e.g.,: -t "[AutoWF-1]" "[AutoWF-2]"',
            dest='test'
        )
        self._parseworkflow.add_argument(
            '-i', '--include',
            nargs='+',
            default=[],
            help='Run workflow(s) with the specified tag(s). '
                 'e.g.,: -i "SETUP" "HADOOP"',
            dest='include'
        )
        self._parseworkflow.add_argument(
            '-e', '--exclude',
            nargs='+',
            default=[],
            help='Run workflow(s) without the specified tag(s), '
                 'workflow(s) with the tag(s) specified in "INCLUDE" are also excluded. '
                 'e.g.,: -e "TEARDOWN"',
            dest='exclude'
        )

        self._parseconfig = self._subparsers.add_parser(
            'config', help='View/Set configuration settings'
        )
        self._parseconfig.add_argument(
            '-l', '--list',
            action='store_const',
            const=self.config.data.keys(),
            help='List all configuration settings'
        )
        self._parseconfig.add_argument(
            '-a', '--all',
            action='store_const',
            const=self.config.data.keys(),
            help='Edit all configuration settings'
        )
        self._parseconfig.add_argument(
            '-s', '--show',
            nargs='+',
            metavar='',
            # choices=self.config.data.keys(),
            help='Show specific configuration settings.'
        )
        self._parseconfig.add_argument(
            '-e', '--edit',
            nargs='+',
            metavar='',
            # choices=self.config.data.keys(),
            help='Edit specific configuration settings.'
        )

    def validate_input_arguments(
            self, inputlist, verifylist,
            argument, isindex=False
    ):
        __choice_format = Color.YELLOW(
            '\nUnknown "{0}". Please select choices from:\n'
        )
        for inputval in inputlist:
            __choice_err = __choice_format.format(inputval)
            if inputval.isdigit() and isindex:
                if int(inputval) <= 0 or int(inputval) > len(verifylist):
                    choicestr = ''.join(
                        [
                            '{0:<3}-- {1}\n'.format(idx + 1, verify)
                            for idx, verify in enumerate(verifylist)
                        ]
                    )
                    raise argparse.ArgumentError(
                        argument, __choice_err + Color.GREEN(choicestr)
                    )
            else:
                if inputval not in verifylist:
                    guesslist = Helper.get_similiar_value(
                        inputval, verifylist
                    )
                    if guesslist:
                        choicestr = '\n'.join(
                            ['{0}'.format(guess) for guess in guesslist]
                        )
                        raise argparse.ArgumentError(
                            argument, __choice_err + Color.GREEN(choicestr)
                        )
                    else:
                        choicestr = '\n'.join(
                            ['{0}'.format(verify) for verify in verifylist]
                        )
                        raise argparse.ArgumentError(
                            argument, __choice_err + Color.GREEN(choicestr)
                        )

    def validate_input_tags(self, tags, argument, required=False):
        __choice_format = Color.YELLOW(
            '\nInvalid tag: "{0}". Please specify valid tags.\n'
        )
        for tag in tags:
            __choice_err = __choice_format.format(tag)
            for case_name in self.autotest.workflowlist:
                if tag.upper() in [
                    _tag.upper()
                    for _tag in self.autotest.workflowdict.get(
                        case_name
                    ).tags
                ]:
                    break
            else:
                if required:
                    raise argparse.ArgumentError(
                        argument, __choice_err
                    )

                print __choice_err

    def validate_input_test(self, test, argument):
        __choice_format = Color.YELLOW(
            '\nUnknown "{0}". '
            'Please select the right workflow name.\n'
        )
        for case in test:
            __choice_err = __choice_format.format(case)
            for case_name in self.autotest.workflowlist:
                if case.split('*')[0] in case_name:
                    break
            else:
                raise argparse.ArgumentError(
                    argument, __choice_err
                )

    def __robot_run(self, testcases):
        robothistory = os.path.expanduser(
            self.config.data.get(
                'history_dir',
                os.path.join(ROBOT_HOME_DIR, 'history')
            )
        )

        if not os.path.isdir(robothistory):
            os.makedirs(robothistory, 0755)

        timestamp = strftime('%Y%m%d-%H%M%S', localtime())
        robotout = os.path.join(robothistory, 'output%s' % timestamp)
        if not os.path.exists(robotout):
            os.mkdir(robotout)
        summarypath = os.path.join(robotout, 'summary%s.txt' % timestamp)
        print('Summary: %s' % os.path.abspath(summarypath))
        print('Dir:     %s' % os.path.abspath(robotout))

        with Output(summarypath) as output:
            _robot_options = {}

            if not self.args.verbose:
                # Sweep out WARN/INFO/DEBUG messages from log report
                # and move the debug information to debug.log file
                _robot_options.setdefault(
                    'loglevel', 'ERROR'
                )
                _robot_options.setdefault(
                    'debugfile', 'debug.log'
                )
            else:
                _robot_options.setdefault(
                    'loglevel', 'DEBUG:INFO'
                )

            robot.run(
                *self.autotest.robot_sources,
                outputdir=robotout,
                timestampoutputs=True,
                test=testcases,
                consolecolors='on',
                stdout=output,
                consolewidth=78,
                **_robot_options
            )

    def parse_args(self):
        if not sys.argv[1:]:
            self.parsecmd.print_help()
            exit(-1)

        (args_base, args_cmd) = self._parserbase.parse_known_args()
        if args_cmd:
            self.args = self.parsecmd.parse_args(
                args=args_cmd, namespace=args_base
            )

            if self.args.cmdopt == 'workflow':
                _arg_attrs = [
                    'list', 'show', 'all',
                    'run', 'test',
                    'include', 'exclude'
                ]

                for _attr_name in _arg_attrs:
                    if getattr(self.args, _attr_name):
                        _no_valid_arg = False
                        break
                else:
                    _no_valid_arg = True

                if _no_valid_arg:
                    self._parseworkflow.print_help()
                    exit(-1)
                try:
                    if self.args.show:
                        self.validate_input_arguments(
                            self.args.show, self.autotest.workflowlist,
                            self._parseworkflow._option_string_actions['--show'],
                            True
                        )
                    if self.args.run:
                        self.validate_input_arguments(
                            self.args.run, self.autotest.workflowlist,
                            self._parseworkflow._option_string_actions['--run'],
                            True
                        )
                    if self.args.test:
                        self.validate_input_test(
                            self.args.test,
                            self._parseworkflow._option_string_actions['--test']
                        )
                    if self.args.exclude:
                        self.validate_input_tags(
                            self.args.exclude,
                            self._parseworkflow._option_string_actions['--exclude']
                        )
                    if self.args.include:
                        self.validate_input_tags(
                            self.args.include,
                            self._parseworkflow._option_string_actions['--include'],
                            True
                        )

                    self.__parse_workflow()
                except argparse.ArgumentError:
                    err = sys.exc_info()[1]
                    self.parsecmd.error(str(err))

            if self.args.cmdopt == 'config':
                _arg_attrs = [
                    'list', 'show', 'all', 'edit'
                ]

                for _attr_name in _arg_attrs:
                    if getattr(self.args, _attr_name):
                        _no_valid_arg = False
                        break
                else:
                    _no_valid_arg = True

                if _no_valid_arg:
                    self._parseconfig.print_help()
                    exit(-1)
                try:
                    if self.args.show:
                        self.validate_input_arguments(
                            self.args.show, self.config.data.keys(),
                            self._parseconfig._option_string_actions['--show']
                        )
                    if self.args.edit:
                        self.validate_input_arguments(
                            self.args.edit, self.config.data.keys(),
                            self._parseconfig._option_string_actions['--edit']
                        )
                    self.__parse_config()
                except argparse.ArgumentError:
                    err = sys.exc_info()[1]
                    self.parsecmd.error(str(err))

    def __parse_workflow(self):
        if self.args.list:
            header = ['ID', 'TAGS', 'TITLE']
            formatter = ['{0:<5}', '{1:<30}', '{2}']
            partial_func = [Color.MAGENTA, Color.BLUE, Color.GREEN]

            format_wf = ''.join(formatter)
            print format_wf.format(*header)
            print format_wf.format(
                *(
                    '=' * len(col)
                    for col in header
                )
            )

            format_wf = ''
            for func, param in zip(partial_func, formatter):
                format_wf += func(param)

            print '\n'.join(
                format_wf.format(
                    index,
                    [str(tag) for tag in workflow.tags],
                    workflow.name
                ) for index, workflow in enumerate(
                    self.autotest.workflowdict.values(), 1
                )
            )

        if self.args.show:
            print('')
            for showflow in self.args.show:
                name = self.autotest.get_workflow_name(showflow)
                if name in self.autotest.workflowdict:
                    workflow = self.autotest.workflowdict[name]
                    from argparse import HelpFormatter, Action
                    h = HelpFormatter('')
                    h.start_section(Color.GREEN('%s' % workflow.name))
                    h.add_text(workflow.doc)
                    h.start_section('AUC Steps')
                    for k in workflow.keywords:
                        if k.startswith('Comment'):
                            comment = k[8:]
                            h.add_argument(
                                Action('', '', help=Color.BLUE(comment))
                            )
                        else:
                            h.add_argument(
                                Action('', '', help=Color.CYAN(k))
                            )

                    h.end_section()
                    h.end_section()
                    print(h.format_help())

        if self.args.include or \
                self.args.run or \
                self.args.test or \
                self.args.all or \
                self.args.exclude:
            r_list = [
                self.autotest.get_workflow_name(r)
                for r in self.args.run
            ]
            i_list = self.autotest.get_workflow_by_tags(
                self.args.include
            )
            t_list = self.autotest.get_workflow_by_name(
                self.args.test
            )
            testcases = r_list + i_list + t_list
            testcases = testcases if testcases else self.autotest.workflowlist

            testcases = self.autotest.remove_workflow_by_tags(
                testcases, self.args.exclude
            )

            _disabled_tag = 'DISABLED'
            if self.autotest.get_workflow_by_tags([_disabled_tag]):
                testcases = self.autotest.remove_workflow_by_tags(
                    testcases, [_disabled_tag]
                )

                print(
                    Color.BLUE(
                        '\nWorkflows with "{}" tag '
                        'are excluded by default\n'.format(
                            _disabled_tag
                        )
                    )
                )

            if testcases:
                self.__robot_run(testcases)
            else:
                print(
                    Color.RED(
                        "No workflow has been selected to run.\n"
                        "Please try to change the switch and "
                        "its relevant arguments."
                    )
                )

    def __parse_config(self):
        def set_config_by_input(keylist=None):
            defaultformat = '\nkey: ##{0}##. \nvalue: {1} type: {2}. \n'
            forformat = '\nkey: ##{0}## For **{3}**. \nvalue: {1} type: {2}.\n'
            listinfo = "Use ',' to split for list.\n"
            inputinfo = Color.YELLOW('Press <Enter> to keep default value\n{0}>')

            for k, v in self.config.data.iteritems():
                if (not keylist) or (
                            keylist and k in keylist
                ):
                    if isinstance(v, OrderedDict):
                        for kk, vv in v.iteritems():
                            typename = type(vv).__name__
                            prompt = forformat.format(
                                Color.CYAN(kk),
                                Color.GREEN(vv),
                                Color.MAGENTA(typename),
                                Color.CYAN(k)
                            )
                            prompt = prompt + listinfo \
                                if isinstance(vv, list) \
                                else prompt
                            prompt += inputinfo.format(Color.CYAN(kk))
                            inputval = Helper.parse_input(
                                raw_input(prompt), typename
                            )
                            if inputval:
                                self.config.data[k][kk] = inputval
                    else:
                        typename = type(v).__name__
                        prompt = defaultformat.format(
                            Color.CYAN(k), Color.GREEN(v), Color.MAGENTA(typename)
                        )
                        prompt = prompt + listinfo \
                            if isinstance(v, list) \
                            else prompt
                        prompt += inputinfo.format(Color.CYAN(k))
                        inputval = Helper.parse_input(
                            raw_input(prompt), typename
                        )
                        if inputval:
                            self.config.data[k] = inputval

            is_save = Helper.query_yes_no(
                'Do want to save the configuration?'
            )
            if is_save:
                self.config.save_config()
                print(
                    'Save the configuration into %s' % os.path.abspath(
                        self.config.yamlpath
                    )
                )
            else:
                self.config.load_config()

        inputkeys = self.args.show or self.args.list
        if inputkeys:
            print(
                self.config.data_to_str(keylist=inputkeys)
            )

        inputkeys = self.args.edit or self.args.all
        if inputkeys:
            set_config_by_input(inputkeys)


if __name__ == '__main__':
    ArgParse().parse_args()
