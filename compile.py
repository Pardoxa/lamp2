from distutils.core import setup
from distutils.extension import Extension
from Cython.Distutils import build_ext

ext_modules = [
    Extension("lightshow", ["lightshow.py"]),
    Extension("demo",["demo.py"]),
    Extension("ble2",["ble2.py"]),
    Extension("light_color",["light_color.py"]),
    Extension("icon_show",["icon_show.py"]),
    Extension("candle",["candle.py"]),
    Extension("stars",["stars.py"]),
    Extension("rainbow",["rainbow.py"]),
    Extension("game_of_life",["game_of_life.py"]),
    Extension("lightHandler",["lightHandler.py"])

]

setup(
    name = 'licht',
    cmdclass = {'build_ext': build_ext},
    ext_modules = ext_modules
)
