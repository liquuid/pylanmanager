#!/usr/bin/env python
# _*_ coding: UTF-8 _*_

import SimpleHTTPServer, pylanrc
import os

workdir = pylanrc.get_workdir()
os.chdir(workdir) 
SimpleHTTPServer.test()
