import unittest
import aiohttp
import aiohttp.web
import configparser
import aiohttp_jinja2
import jinja2
import uvloop
import asyncio
from aiohttp import web
import logging
import traceback
import colorlog
import model, views
from middleware import setup_middlewares
import os
from pythonjsonlogger import jsonlogger
from utils import *

class MyTestCase(unittest.TestCase):
    def test_something(self):
        value=True
        self.assertEqual(filter_example(value), value)


if __name__ == '__main__':
    unittest.main()
