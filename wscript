#!/usr/bin/env python
# encoding: utf-8

VERSION='1.0'
APPNAME='googletest'

top = '.'
out = '.build'


import os, sys
import platform
from waflib import Configure
from waflib import Logs
from waflib import Utils
from waflib.Tools import waf_unit_test
from waflib.Build import BuildContext, CleanContext, InstallContext, UninstallContext
from wafcfg import common


''' Define Waf contexts for debug and release builds. '''
CONTEXTS = { BuildContext, CleanContext, InstallContext, UninstallContext }
for var in 'debug release'.split():
    for ctx in CONTEXTS:
        name = ctx.__name__.replace('Context', '').lower()

        class tmp(ctx):
            cmd = name + '_' + var
            variant = var


def options(opt):
    opt.load('compiler_cxx')


def configure(conf):
    conf.env.TARGET = platform.system().lower() + '_' + platform.machine().lower()
    conf.msg('Setting target to', conf.env.TARGET)
    conf.set_env()
    conf.load('compiler_cxx')
    env = conf.env.derive()
    conf.set_variant('release', env)
    conf.set_variant('debug', env)


def build(bld):
    if not bld.variant:
        bld.fatal('call "waf build_debug", "waf build_release"\nwaf --help')

    bld.recurse('googletest')
    bld.recurse('googlemock')
