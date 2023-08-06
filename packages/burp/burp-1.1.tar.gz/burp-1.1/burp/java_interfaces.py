from types import ModuleType
import sys

def install_java_interfaces():
    module = ModuleType("java")
    sys.modules["java"] = module

    module = ModuleType("java.net")
    sys.modules["java.net"] = module
