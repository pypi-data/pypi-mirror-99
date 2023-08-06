#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# imports.
import dev0s
dev0s.defaults.insert(dev0s.defaults.source_path(__file__, back=1))
from apps.packages.packages import inc_package_manager

# source path & version.
from dev0s.shortcuts import Version, Directory, Files, gfp
source = Directory(gfp.base(__file__))
base = Directory(source.fp.base())
version = Version(Files.load(source.join(".version")))