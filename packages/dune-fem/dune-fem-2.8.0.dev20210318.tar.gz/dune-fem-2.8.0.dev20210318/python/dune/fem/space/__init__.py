import hashlib
import inspect
import sys
import os

import dune.common.module
from dune.common.utility import isString
from dune.generator.generator import SimpleGenerator
from dune.fem import function

from ._spaces import *

try:
    import ufl
    from dune.ufl import GridFunction, expression2GF
except:
    pass

def _uflToExpr(grid,order,f):
    if not ufl: return f
    if isinstance(f, list) or isinstance(f, tuple):
        if isinstance(f[0], ufl.core.expr.Expr):
            f = ufl.as_vector(f)
    if isinstance(f, GridFunction):
        return f
    if isinstance(f, ufl.core.expr.Expr):
        return expression2GF(grid,f,order).as_ufl()
    else:
        return f

def interpolate(space, expr, name=None, **kwargs):
    """interpolate a function into a discrete function space

    Args:
        space: discrete function space to interpolate into
        expr:  function to interpolate
        name:  name of the resulting discrete function

    Returns:
        DiscreteFunction: the constructed discrete function
    """
    expr = _uflToExpr(space.grid,space.order,expr)
    if name is None:
        try:
            name = expr.name
        except AttributeError:
            raise ValueError("interpolation requires a name for the resulting discrete function - either the expression needs a name attribute or 'name' needs to be provided as second argument.")
    # assert func.dimRange == space.dimRange, "range dimension mismatch"
    return function.discreteFunction(space, name=name, expr=expr, **kwargs)

def project(space, func, name=None, **kwargs):
    """project a (discrete) function into a discrete function space

    Args:
        space: discrete function space to project into
        func:  function to project
        name:  name of the resulting discrete function

    Returns:
        DiscreteFunction: the constructed discrete function
    """
    expr = _uflToExpr(space.grid,space.order,func)
    if name is None:
        name = func.name
    # assert func.dimRange == space.dimRange, "range dimension mismatch"
    df = function.discreteFunction(space, name=name, expr=None, **kwargs)
    df.project(func)
    return df

def dfInterpolate(self, f):
    if isinstance(f, list) or isinstance(f, tuple):
        if isinstance(f[0], ufl.core.expr.Expr):
            f = ufl.as_vector(f)
    dimExpr = 0
    if isinstance(f, GridFunction):
        func = f.gf
        dimExpr = func.dimRange
    elif isinstance(f, ufl.core.expr.Expr):
        func = expression2GF(self.space.grid,f,self.space.order).as_ufl()
        if func.ufl_shape == ():
            dimExpr = 1
        else:
            dimExpr = func.ufl_shape[0]
    else:
        try:
            gl = len(inspect.getargspec(f)[0])
            func = None
        except TypeError:
            func = f
            if isinstance(func,int) or isinstance(func,float):
                dimExpr = 1
            else:
                dimExpr = len(func)
        if func is None:
            if gl == 1:   # global function
                func = function.globalFunction(self.space.grid, "tmp", self.space.order, f).gf
            elif gl == 2: # local function
                func = function.localFunction(self.space.grid, "tmp", self.space.order, f).gf
            elif gl == 3: # local function with self argument (i.e. from @gridFunction)
                func = function.localFunction(self.space.grid, "tmp", self.space.order, lambda en,x: f(en,x)).gf
            dimExpr = func.dimRange

    if dimExpr == 0:
        raise AttributeError("can not determine if expression shape"\
                " fits the space's range dimension")
    elif dimExpr != self.space.dimRange:
        raise AttributeError("trying to interpolate an expression"\
            " of size "+str(dimExpr)+" into a space with range dimension = "\
            + str(self.space.dimRange))
    return self._interpolate(func)

def dfProject(self, f):
    if isinstance(f, list) or isinstance(f, tuple):
        if isinstance(f[0], ufl.core.expr.Expr):
            f = ufl.as_vector(f)
    dimExpr = 0
    if isinstance(f, GridFunction):
        func = f.gf
        dimExpr = func.dimRange
    elif isinstance(f, ufl.core.expr.Expr):
        func = expression2GF(self.space.grid,f,self.space.order).as_ufl()
        if func.ufl_shape == ():
            dimExpr = 1
        else:
            dimExpr = func.ufl_shape[0]
    else:
        try:
            gl = len(inspect.getargspec(f)[0])
            func = None
        except TypeError:
            func = f
            if isinstance(func,int) or isinstance(func,float):
                dimExpr = 1
            else:
                dimExpr = len(func)
        if func is None:
            if gl == 1:   # global function
                func = function.globalFunction(self.space.grid, "tmp", self.space.order, f).gf
            elif gl == 2: # local function
                func = function.localFunction(self.space.grid, "tmp", self.space.order, f).gf
            elif gl == 3: # local function with self argument (i.e. from @gridFunction)
                func = function.localFunction(self.space.grid, "tmp", self.space.order, lambda en,x: f(en,x)).gf
            dimExpr = func.dimRange

    if dimExpr == 0:
        raise AttributeError("can not determine if expression shape"\
                " fits the space's range dimension")
    elif dimExpr != self.space.dimRange:
        raise AttributeError("trying to interpolate an expression"\
            " of size "+str(dimExpr)+" into a space with range dimension = "\
            + str(self.space.dimRange))
    return self._project(func)

def localContribution(self, assembly):
    if assembly == "set":
        return self.setLocalContribution()
    elif assembly == "add":
        return self.addLocalContribution()
    else:
        raise ValueError("assembly can only be `set` or `add`")

def addDFAttr(module, cls, storage):
    setattr(cls, "_module", module)
    setattr(cls, "_storage", storage)
    setattr(cls, "interpolate", dfInterpolate )
    if hasattr(cls,"_project"):
        setattr(cls, "project", dfProject )
    setattr(cls, "localContribution", localContribution )
    try:
        from dune.fem.plotting import plotPointData
        setattr(cls, "plot", plotPointData)
    except ImportError:
        setattr(cls, "plot", lambda *args,**kwargs:
           print("problem importing plotting utility - possibly matplotlib is missing?"))

def addBackend(Df,backend):
    def backend_(self):
        try:
            return self._backend
        except:
            pass
        try:
            import numpy as np
            return np.array( self.dofVector, copy=False )
        except:
            pass
        return None
    setattr(Df,backend,property(backend_))

def storageToSolver(storage):
    if storage == "adaptive":
        return "fem"
    else:
        return str(storage)

generator = SimpleGenerator(["Space","DiscreteFunction"], "Dune::FemPy")

def addAttr(module, self, field, scalar, codegen):
    setattr(self, "_module", module)
    setattr(self, "field", field)
    setattr(self, "scalar", scalar)
    setattr(self, "codegenStorage", codegen)
    setattr(self, "interpolate",
            lambda *args,**kwargs: interpolate(self,*args,**kwargs))
    setattr(self, "codegen",
            lambda moduleName,interiorQuadratureOrders, skeletonQuadratureOrders:
                  _codegen(self,moduleName,interiorQuadratureOrders, skeletonQuadratureOrders)
           )
    DF = module.DiscreteFunction
    if hasattr(DF,"_project"):
        setattr(self, "project",
            lambda *args,**kwargs: project(self,*args,**kwargs))
    setattr(self, "function",
            lambda *args,**kwargs: function.discreteFunction(self,*args,**kwargs))
    DF.scalar = property(lambda self: self.space.scalar)

def addStorage(obj, storage):
    if not storage:
        storage = str("fem")
    if isString(storage):
        import dune.create as create
        assert storageToSolver(storage), "wrong storage (" + storage + ") passed to space"
        storage = create.discretefunction(storageToSolver(storage))(obj)
    else:
        storage = storage(obj)
    setattr(obj, "storage", storage)
    return storage

fileBase = "femspace"

def addDiscreteFunction(space, storage):
    from dune.generator import Constructor
    storage, dfIncludes, dfTypeName, _, _,backend = addStorage(space,storage)

    ctor = ()
    spaceType = space._typeName
    if storage == "petsc":
        try:
            import petsc4py
            dfIncludes += [os.path.dirname(petsc4py.__file__)+"/include/petsc4py/petsc4py.h"]
            ctor = [Constructor(['const std::string &name', 'const ' + spaceType + '&space', 'pybind11::handle dofVector'],
                    ['if (import_petsc4py() != 0) {',
                     '  throw std::runtime_error("Error during import of petsc4py");',
                     '}',
                     'Vec petscVec = PyPetscVec_Get(dofVector.ptr());',
                     'typename DuneType::DofVectorType *dofStorage = new typename DuneType::DofVectorType(space,petscVec);',
                     '// std::cout << "setup_petscStorage " << dofStorage << " " << petscVec << std::endl;',
                     'pybind11::cpp_function remove_petscStorage( [ dofStorage, dofVector, petscVec] ( pybind11::handle weakref ) {',
                     '  // std::cout << "remove_petscStorage " << vec.ref_count() << " " << dofStorage << " " << petscVec << std::endl;',
                     '  delete dofStorage;',
                     '  weakref.dec_ref();',
                     '} );',
                     'pybind11::weakref weakref( dofVector, remove_petscStorage );',
                     'weakref.release();',
                     'return new DuneType( name, space, *dofStorage );'],
                    ['"name"_a', '"space"_a', '"dofVector"_a', 'pybind11::keep_alive< 1, 3 >()', 'pybind11::keep_alive< 1, 4 >()'])
                ]
        except:
            ctor = [Constructor(['const std::string &name', 'const ' + spaceType + '&space', 'pybind11::handle dofVector'],
                    ['std::cerr <<"Can not use constructor with dof vector argument because `petsc4py` was not found!\\n";',
                     'throw std::runtime_error("Can not use constructor with dof vector argument because `petsc4py` was not found!");',
                     'return new DuneType(name,space);'],
                    ['"name"_a', '"space"_a', '"dofVector"_a', 'pybind11::keep_alive< 1, 3 >()', 'pybind11::keep_alive< 1, 4 >()'])
                   ]
    elif storage == "fem":
        ctor = [Constructor(['const std::string &name', 'const ' +
            spaceType + '&space', 'pybind11::array_t<double> dofVector'],
                ['double *dof = static_cast< double* >( dofVector.request(false).ptr );',
                 'return new DuneType(name,space,dof);'],
                ['"name"_a', '"space"_a', '"dofVector"_a', 'pybind11::keep_alive< 1, 3 >()', 'pybind11::keep_alive< 1, 4 >()'])
            ]
    elif storage == "istl":
        ctor = [Constructor(['const std::string &name', 'const ' +
            spaceType + '&space', 'typename DuneType::DofContainerType &dofVector'],
                ['return new DuneType(name,space,dofVector);'],
                ['"name"_a', '"space"_a', '"dofVector"_a', 'pybind11::keep_alive< 1, 3 >()', 'pybind11::keep_alive< 1, 4 >()'])
            ]
    else:
        ctor = [Constructor(['const std::string &name', 'const ' + spaceType + '&space', 'pybind11::handle vec'],
                ['std::cerr <<"Can not use constructor with dof vector argument for this type of discrete function storage!\\n";',
                 'throw std::runtime_error("Can not use constructor with dof vector argument for this type of discrete function storage!");',
                 'return new DuneType(name,space);'],
                ['"name"_a', '"space"_a', '"vec"_a', 'pybind11::keep_alive< 1, 3 >()', 'pybind11::keep_alive< 1, 4 >()'])
               ]
    dfIncludes += ["dune/fempy/py/discretefunction.hh"]
    return dfIncludes, dfTypeName, backend, ctor

def module(field, includes, typeName, *args,
           storage=None, scalar=False, codegen=False,
           ctorArgs):
    includes = includes + ["dune/fempy/py/space.hh"]
    defines = []

    class DummySpace:
        _typeName = typeName
        _includes = includes
    DummySpace.field     = field
    dfIncludes, dfTypeName,  backend, dfArgs = addDiscreteFunction(DummySpace, storage)

    moduleName = fileBase + "_" + hashlib.md5(typeName.encode('utf-8')).hexdigest() \
                          + "_" + hashlib.md5(dfTypeName.encode('utf-8')).hexdigest()

    module = generator.load(includes+dfIncludes, [typeName,dfTypeName], moduleName,
                            ((*args,), (*dfArgs,)),
                            dynamicAttr=[True,True],
                            bufferProtocol=[False,True],
                            options=[["std::shared_ptr<DuneType>"],[]],
                            defines=defines)

    spc = module.Space(*ctorArgs)
    addAttr(module, spc, field, scalar, codegen)
    setattr(spc,"DiscreteFunction",module.DiscreteFunction)
    addDFAttr(module, module.DiscreteFunction, addStorage(spc,storage))
    if not backend is None:
        addBackend(module.DiscreteFunction, backend)
    return spc

def _codegen(space,moduleName,interiorQuadratureOrders, skeletonQuadratureOrders):
    if interiorQuadratureOrders is None: interiorQuadratureOrders = []
    if skeletonQuadratureOrders is None: skeletonQuadratureOrders = []
    moduleNameExt = "i" + "".join(str(i) for i in interiorQuadratureOrders) + "_" +\
                    "s" + "".join(str(i) for i in skeletonQuadratureOrders)
    autogenFile = "autogeneratedcode_" + moduleName + "_" + moduleNameExt + ".hh"
    dune_py_dir   = dune.common.module.get_dune_py_dir()
    generated_dir = dune_py_dir # os.path.join(dune_py_dir, 'python', 'dune', 'generated')
    codegenPath = generated_dir
    space._generateQuadratureCode(interiorQuadratureOrders,skeletonQuadratureOrders,codegenPath,autogenFile)
    return [autogenFile], moduleNameExt
