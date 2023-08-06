#!usr/bin/env python


from distutils.core import setup, Extension


privacy_module = Extension('_privacy_alg', sources=['privacy_wrap.cxx', 'privacy.cpp'], )


setup(
    name='privacy_alg',# module name
    version='1.0',
    author="wukai",
    author_email = "2365388286@qq.com",
    url = "http://wukai.name",
    description = """Some algorithms about privacy preserving""",
    ext_modules = [privacy_module],
    py_modules=['privacy_alg']# python file
)
