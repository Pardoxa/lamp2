from distutils.core import setup
from distutils.extension import Extension
from Cython.Distutils import build_ext

ext_modules = [
    Extension("demo",["demo.py"]),
    Extension("bluetooth_to_android",["bluetooth_to_android.py"]),
    Extension("light_functions",["light_functions.py"]),
    Extension("icon_show",["icon_show.py"]),
    Extension("candle",["candle.py"]),
    Extension("stars",["stars.py"]),
    Extension("rainbow",["rainbow.py"]),
    Extension("game_of_life",["game_of_life.py"]),
    Extension("drop",["drop.py"]),
    Extension("rainbow_dot",["rainbow_dot.py"]),
    Extension("cross",["cross.py"]),
    Extension("graphics",["graphics.py"]),
    Extension("unicorn_clock",["unicorn_clock.py"]),
    Extension("lightHandler",["lightHandler.py"])

]

setup(
    name = 'licht',
    cmdclass = {'build_ext': build_ext},
    ext_modules = ext_modules
)
