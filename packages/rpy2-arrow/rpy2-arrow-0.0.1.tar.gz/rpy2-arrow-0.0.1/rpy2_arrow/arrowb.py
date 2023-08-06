from rpy2.robjects.packages import importr
from rpy2 import robjects
import rpy2_R6.r6b as r6b
import rpy2.rinterface_lib.callbacks

r_arrow = importr('arrow')
methods = importr('methods')


class CustomR6(r6b.R6):

    def __init__(self, obj):
        super().__init__(obj)
        self.ro = robjects.vectors.VectorOperationsDelegator(self)
        self.rx = robjects.vectors.ExtractDelegator(self)
        self.rx2 = robjects.vectors.DoubleExtractDelegator(self)

    def __str__(self):
        s = []
        with (rpy2.rinterface_lib
              .callbacks.obj_in_module(rpy2.rinterface_lib.callbacks,
                                       'consolewrite_print', s.append)):
            methods.show(self)
        s = str.join('', s)
        return s



class ArrowClassGenerator(r6b.R6DynamicClassGenerator):

    __DEFAULT_ATTRS__ = r6b.R6DynamicClassGenerator.__DEFAULT_ATTRS__.copy()
    __DEFAULT_ATTRS__.update({'new': r6b.r6_factorymethod,
                              'create': r6b.r6_factorymethod})
    __CLASSMAP__ = lambda x: r6b._dynamic_classmap(x, bases = (CustomR6, ))


ArrayGen = ArrowClassGenerator(r_arrow.Array)
TableGen = ArrowClassGenerator(r_arrow.Table)

