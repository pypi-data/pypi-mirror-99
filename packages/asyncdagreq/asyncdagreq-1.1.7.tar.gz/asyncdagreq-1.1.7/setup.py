from setuptools import setup

#    with open('README.rst') as f:
#        long_description = f.read()

long_description = """

unofficial DagpiWrapper
=======================

Async Wrapper for Dagpi

| `OFFICIAL DAGPI WEBSITE <https://dagpi.xyz/>`__
| `OFFICIAL GITHUBREPO <https://github.com/Ali-TM-original/asyncdagreq>`__

Author: Ali™ AKA Ali-TM-original
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Just A small project to imporve my skills in Object Oriented
Programming, inspired from my previous discord.py canny command

| NOT READY FOR USE YET
| tasks remaining:
|  [STRIKEOUT:1>Error Detection]

::

    2>.Testing
    3>.Get this up and running on pypi

CURRENT STATE : BROKEN
----------------------

Usage with discord.py (till now)
================================

super simple

**Roast**

::

    from asyncdagreq import Client
    import json

    object = Client.Asyncdagreq('your token')

    @bot.command()
    async def roast(ctx):
        roast = await object.roast()
        x = roast.decode("utf-8")
        j = json.loads(x)
        await ctx.send(j['roast'])
        

**USING IMAGE METHODS**

::

    from asyncdagreq import Client
    import json

    object = Client.Asyncdagreq('your token')

    @bot.command()
    async def captcha(ctx):
        url = str(ctx.message.author.avatar_url_as(format="png", static_format="png", size=1024))
        img = await object.captcha(str(url), "hello")
        file = discord.File(img, "pixel.png")
        await ctx.send(file=file)





"""

with open('requirements.txt') as f:
    requirements = f.read().splitlines()

setup(
    name='asyncdagreq',
    version='1.1.7',
    description='An async wrapper made in Python for Dagpi.',
    long_description=long_description,
    url='https://github.com/Ali-TM-original/asyncdagreq',
    author='Ali-TM-original',
    license='MIT',
    packages=['asyncdagreq'],
    install_requires=['aiohttp'],
    requirements=requirements,
    zip_safe=False,
)