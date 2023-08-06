import os
import abc
import sys
from unittest import TestCase
import pyoccad

normal_imports = {'pyoccad.typing', 'pyoccad', 'pyoccad._version'}


class InitTest:
    name = ''
    classes_count = 0
    modules_count = 0

    @staticmethod
    @abc.abstractmethod
    def class_pattern_matcher(class_name, module_name):
        pass

    @staticmethod
    def flush_sys_module_cache():
        # flush the sys.modules cache
        modules_to_flush = [key for key in sys.modules if 'pyoccad' in key]
        for key in modules_to_flush:
            sys.modules.pop(key)

    @staticmethod
    def imported_modules(module):
        InitTest.flush_sys_module_cache()
        __import__('.'.join((pyoccad.__name__, module)))
        pyoccad_modules = [key for key in sys.modules if pyoccad.__name__ in key and key not in normal_imports]
        return {m for m in pyoccad_modules if module not in m}

    @staticmethod
    def flush_init(module):
        # flush the init file
        f = open(os.sep.join((os.path.dirname(pyoccad.__file__), module, '__init__.py')), "w")
        f.write("# Automatically generated imports running tests")
        f.close()

    @staticmethod
    def import_all_modules(top_module, class_pattern_matcher):
        """Dynamically imports all modules."""

        import inspect
        import os
        from importlib import reload
        from collections import OrderedDict

        imports = []
        globals_, locals_ = globals(), locals()

        # dynamically import all the package modules
        modules = dict()
        classes = OrderedDict()
        json_files = set()

        for root, _, files in os.walk(os.path.dirname(top_module.__file__)):
            relative_root = os.path.relpath(root, os.path.dirname(top_module.__file__))
            for filename in files:
                # process all python files in directory that don't start with underscore
                # (which also keeps this module from importing itself)
                modulename, ext = os.path.splitext(filename)
                if filename[0] != '_' and '_test' not in modulename:
                    if ext == '.py':
                        if relative_root == ".":
                            modules['.'.join([top_module.__name__, modulename])] = modulename
                        else:
                            modules['.'.join([top_module.__name__, relative_root, modulename])] = modulename

        saved_modules = modules.copy()
        old_length = len(modules) + 1
        while len(modules) and old_length > len(modules):
            old_length = len(modules)
            for package_module, modulename in modules.copy().items():
                try:
                    module = __import__(package_module, globals_, locals_, [modulename])

                    for obj_name in filter(lambda name: name[0] != '_', module.__dict__):
                        obj = module.__dict__[obj_name]
                        if inspect.isclass(obj):
                            if obj_name not in classes and class_pattern_matcher(obj_name, modulename):
                                globals_[obj_name] = obj
                                classes[obj_name] = package_module
                                imports.append("from {} import {}".format(package_module, obj_name))
                                # __import__(package_module, globals_, locals_, [obj_name])
                                f = open(top_module.__file__, "a")
                                f.write('\n' + imports[-1])
                                f.close()
                                reload(top_module)

                except ModuleNotFoundError as err:
                    raise err
                except ImportError as err:
                    continue

                modules.pop(package_module)  # Remove module from the available list

        if len(modules):
            raise ModuleNotFoundError('Failed to import from {} modules \n{}'.format(top_module.__name__,
                                                                                     '\n'.join(modules)))
        f = open(top_module.__file__, "a")
        f.write('\n')
        f.close()

        return imports, classes, saved_modules

    def test___init__(self):
        InitTest.flush_sys_module_cache()

        # flush init before importing!
        InitTest.flush_init(self.name)

        module = __import__('.'.join((pyoccad.__name__, self.name)), fromlist=(self.name))
        imports, classes, modules = InitTest.import_all_modules(module, self.class_pattern_matcher)

        self.assertEqual(self.classes_count, len(classes))
        self.assertEqual(self.modules_count, len(modules))

    def test_external_imports(self):
        self.assertEqual(set(), InitTest.imported_modules(self.name))


class InitCreateTest(InitTest, TestCase):

    name = 'create'
    classes_count = 43
    modules_count = 33

    @staticmethod
    def class_pattern_matcher(class_name, module_name):
        return 'Create' in class_name


class InitMeasureTest(InitTest, TestCase):

    name = 'measure'
    classes_count = 8
    modules_count = 10

    @staticmethod
    def class_pattern_matcher(class_name, module_name):
        return 'Measure' in class_name


class InitExploreTest(InitTest, TestCase):

    name = 'explore'
    classes_count = 1
    modules_count = 1

    @staticmethod
    def class_pattern_matcher(class_name, module_name):
        return 'Explore' in class_name


class InitHealTest(InitTest, TestCase):

    name = 'heal'
    classes_count = 0
    modules_count = 3

    @staticmethod
    def class_pattern_matcher(class_name, module_name):
        return class_name.lower() == module_name.replace('_', '').lower()


class InitTransformTest(InitTest, TestCase):

    name = 'transform'
    classes_count = 7
    modules_count = 9

    @staticmethod
    def class_pattern_matcher(class_name, module_name):
        return class_name.lower() == module_name.replace('_', '').lower()


# TODO: understand why doc import fails due to libGL missing
# class InitDocTest(InitTest, TestCase):
#
#     name = 'doc'
#     classes_count = 1
#     modules_count = 7
#
#     @staticmethod
#     def class_pattern_matcher(class_name, module_name):
#         return class_name.lower() == module_name.replace('_', '').lower()


class InitExchangeTest(InitTest, TestCase):

    name = 'exchange'
    classes_count = 0
    modules_count = 1

    @staticmethod
    def class_pattern_matcher(class_name, module_name):
        return class_name.lower() == module_name.replace('_', '').lower()
