"""
Utility to persist arbitrary sklearn objects to HDF5
A hybrid method that combines json and HDF5 methods.

Author: Qiang Gu
Email: guqiang01@gmail.com
Date: 2020-2021

Classes:

    ModelToHDF5
    HDF5ToModel

"""
import h5py
import json
import numpy
import six
import sys
import types
import warnings
from keras.engine.network import Network
from keras.models import load_model
from ..utils import get_search_params


# reserved keys
_PY_VERSION = '-cpython-'
_NP_VERSION = '-numpy-'
_OBJ = '-object-'
_REDUCE = '-reduce-'
_GLOBAL = '-global-'
_FUNC = '--func-'
_ARGS = '-args-'
_STATE = '-state-'
_KEYS = '-keys-'
_MEMO = '-memo-'
_NP_NDARRAY = '-np_ndarray-'
_DTYPE = '-dtype-'
_VALUES = '-values-'
_NP_DATATYPE = '-np_datatype-'
_DATATYPE = '-datatype-'
_VALUE = '-value-'
_TUPLE = '-tuple-'
_SET = '-set-'
_BYTES = '-bytes-'
_PRIMITIVE = '-primitive-'
_NP_NDARRAY_O = '-np_ndarray_o_type-'
_WEIGHTS = '-model_weights-'
_CONFIG = '-model_config-'
_HYPERPARAMETER = '-model_hyperparameters-'
_KERAS_MODELS = '-keras_models-'
_KERAS_MODEL = '-keras_model-'

PY_VERSION = sys.version.split(' ')[0]


class HPicklerError(Exception):
    pass


class ModelToHDF5:
    """
    Follows python pickle.
    Save a scikit-learn/keras model to HDF5 file.
    """
    def __init__(self, verbose=0):
        self.memo = {}
        self.verbose = verbose

    def clear_memo(self):
        """Clears the `memo`
        """
        self.memo.clear()

    def memoize(self, obj):
        """
        Store an object id in the `memo`
        """
        assert id(obj) not in self.memo
        idx = len(self.memo)
        if self.verbose:
            print("Memoize: ", (idx, obj))
        self.memo[id(obj)] = idx, obj

    def dump(self, obj, file_path, mode='w',
             store_hyperparameter=True):
        """
        Main access of object save

        Parameters:
        obj : python object to save
        file_path : str or hdf5.File or hdf5.Group object
            Target file path in HDF5 format
        store_hyperparameter : bool.
            Whether to save model hyperparameter.
        """
        try:
            if isinstance(file_path, str):
                file = h5py.File(file_path, mode=mode)

            if not isinstance(file, h5py.Group):
                raise ValueError("The type of file_path, %s, is "
                                 "not supported. Supported types "
                                 "are file path (str), h5py.File "
                                 "and h5py.Group object!"
                                 % (str(file_path)))

            file.attrs[_PY_VERSION] = str(PY_VERSION).encode('utf8')

            np_module = sys.modules.get('numpy')
            if np_module:
                file.attrs[_NP_VERSION] = \
                    str(np_module.__version__).encode('utf8')

            self.weights = []
            self.keras_models = []

            config = {_OBJ: self.save(obj)}
            file[_CONFIG] = json.dumps(config).encode('utf8')

            if self.weights:
                weights_group = file.create_group(_WEIGHTS)
                for idx, arr in enumerate(self.weights):
                    weights_group[str(idx)] = arr

            if self.keras_models:
                k_models_group = file.create_group(_KERAS_MODELS)
                for idx, model in enumerate(self.keras_models):
                    idx_group = k_models_group.create_group(str(idx))
                    model.save(idx_group)

            if store_hyperparameter:
                h_params = get_search_params(obj)
                file[_HYPERPARAMETER] = json.dumps(h_params).encode('utf8')

        except:
            raise
        finally:
            file.close()

    def save(self, obj):

        # Check the `memo``
        x = self.memo.get(id(obj))
        if x:
            rval = {_MEMO: x[0]}
            return rval

        # Check type in `dispath` table
        t = type(obj)
        f = self.dispatch.get(t)
        if f:
            return f(self, obj)

        # Check for a class with a custom metaclass; treat as regular class
        try:
            issc = issubclass(t, type)
        except TypeError:
            issc = 0
        if issc:
            return self.save_global(obj)

        if isinstance(obj, Network):
            return self.save_keras_model(obj)

        return self.save_reduce(obj)

    def save_reduce(self, obj):
        """
        Decompose an object using pickle reduce
        """
        if self.verbose:
            print(obj)
        reduce = getattr(obj, "__reduce__", None)
        if reduce:
            rv = reduce()
        else:
            raise HPicklerError(
                "Can't reduce %r object: %r" % (type(obj).__name__, obj))
        assert (type(rv) is tuple),\
            "%s must return a tuple, but got %s" % (reduce, type(rv))

        lenth = len(rv)
        assert (lenth in [2, 3]),\
            ("Reduce tuple is expected to return 2- 3 elements, "
             "but got %d elements" % lenth)

        save = self.save

        rval = {}

        func = rv[0]
        assert callable(func), "func from reduce is not callable"
        rval[_FUNC] = save(func)

        args = rv[1]
        assert (type(args) is tuple)
        rval[_ARGS] = {_TUPLE: save(list(args))}

        if lenth == 3:
            state = rv[2]
            rval[_STATE] = save(state)

        self.memoize(obj)
        return {_REDUCE: rval}

    dispatch = {}

    def save_primitive(self, obj):
        return obj

    dispatch[type(None)] = save_primitive
    dispatch[bool] = save_primitive
    dispatch[int] = save_primitive
    dispatch[float] = save_primitive

    def save_string(self, obj):
        self.memoize(obj)
        return obj

    dispatch[str] = save_string

    def save_bytes(self, obj):
        self.memoize(obj)
        return {_BYTES: obj.decode('utf-8')}

    dispatch[bytes] = save_bytes

    """def save_unicode(self, obj):
        self.memoize(obj)
        return {_UNICODE: obj}

    if six.PY2:
        dispatch[unicode] = save_unicode"""
    # dispatch[bytearray] = save_primitive

    def save_list(self, obj):
        return [self.save(e) for e in obj]

    dispatch[list] = save_list

    def save_tuple(self, obj):
        aslist = self.save(list(obj))
        return {_TUPLE: aslist}

    dispatch[tuple] = save_tuple

    def save_set(self, obj):
        aslist = self.save(list(obj))
        return {_SET: aslist}

    dispatch[set] = save_set

    def save_dict(self, obj):
        if len(obj) == 0:
            return {}
        newdict = {}
        _keys = list(obj.keys())
        _keys.sort()
        newdict[_KEYS] = _keys
        for k in _keys:
            v = obj[k]
            """# for keras g model config. There might be a better way.
            if k == 'config' and isinstance(v, dict):
                newdict[k] = v
            else:"""
            newdict[k] = self.save(v)

        return newdict

    dispatch[dict] = save_dict

    def save_global(self, obj):
        name = getattr(obj, '__name__', None)
        if name is None:
            raise HPicklerError("Can't get global name for object %r"
                                % obj)
        module_name = getattr(obj, '__module__', None)
        if module_name is None:
            raise HPicklerError("Can't get global module name for "
                                "object %r" % obj)

        newdict = {_GLOBAL: [module_name, name]}
        self.memoize(obj)
        return newdict

    dispatch[types.FunctionType] = save_global
    dispatch[types.BuiltinFunctionType] = save_global

    def save_np_ndarray(self, obj):
        _dtype = obj.dtype
        if _dtype.descr == [('', '|O')]:
            newdict = {}
            newdict[_DTYPE] = self.save(obj.dtype)
            newdict[_VALUES] = self.save(obj.tolist())
            return {_NP_NDARRAY_O: newdict}
        else:
            new_dict = {_NP_NDARRAY: len(self.weights)}
            self.weights.append(obj)
            return new_dict

    dispatch[numpy.ndarray] = save_np_ndarray

    def save_np_datatype(self, obj):
        newdict = {}
        newdict[_DATATYPE] = self.save(type(obj))
        newdict[_VALUE] = self.save(obj.item())

        return {_NP_DATATYPE: newdict}

    dispatch[numpy.bool_] = save_np_datatype
    dispatch[numpy.int_] = save_np_datatype
    dispatch[numpy.intc] = save_np_datatype
    dispatch[numpy.intp] = save_np_datatype
    dispatch[numpy.int8] = save_np_datatype
    dispatch[numpy.int16] = save_np_datatype
    dispatch[numpy.int32] = save_np_datatype
    dispatch[numpy.int64] = save_np_datatype
    dispatch[numpy.uint8] = save_np_datatype
    dispatch[numpy.uint16] = save_np_datatype
    dispatch[numpy.uint32] = save_np_datatype
    dispatch[numpy.uint64] = save_np_datatype
    dispatch[numpy.float_] = save_np_datatype
    dispatch[numpy.float16] = save_np_datatype
    dispatch[numpy.float32] = save_np_datatype
    dispatch[numpy.float64] = save_np_datatype
    dispatch[numpy.complex_] = save_np_datatype
    dispatch[numpy.complex64] = save_np_datatype
    dispatch[numpy.complex128] = save_np_datatype

    def save_keras_model(self, obj):
        self.memoize(obj)
        new_dict = {_KERAS_MODEL: len(self.keras_models)}
        self.keras_models.append(obj)
        return new_dict


class HDF5ToModel:
    """
    Rebuild model from HDF5 generated by `ModelToHDF5.save`.
    """

    def __init__(self, verbose=0):
        # Store newly-built object
        self.memo = {}
        self.verbose = verbose

    def memoize(self, obj):
        lenth = len(self.memo)
        self.memo[lenth] = obj
        if self.verbose:
            print("Memoize: ", (lenth, obj))

    def load(self, file_path):
        try:
            if isinstance(file_path, str):
                data = h5py.File(file_path, 'r')
            if not isinstance(data, h5py.Group):
                raise ValueError("The type of %s is not supported! "
                                 "Supported types are file path (str), "
                                 "h5py.File and h5py.Group object!"
                                 % (str(file_path)))

            if data.attrs[_PY_VERSION].decode('utf8') != PY_VERSION:
                warnings.warn("Trying to load an object from python %s "
                              "when using python %s. This might lead to "
                              "breaking code or invalid results. Use at "
                              "your own risk."
                              % (data[_PY_VERSION].decode('utf8'),
                                 PY_VERSION.decode('utf8')))
            if _WEIGHTS in data:
                self.weights = data[_WEIGHTS]
            if _KERAS_MODELS in data:
                self.keras_models = data[_KERAS_MODELS]
            config = data[_CONFIG][()].decode('utf8')
            config = json.loads(config)
            model = self.load_all(config[_OBJ])
        except:
            raise
        finally:
            data.close()

        return model

    def load_all(self, data):
        """
        The main method to generate an object from python dict
        """
        t = type(data)
        if t is dict:
            if _MEMO in data:
                return self.memo[data[_MEMO]]
            if _BYTES in data:
                return self.load_bytes(data[_BYTES])
            if _REDUCE in data:
                return self.load_reduce(data[_REDUCE])
            if _GLOBAL in data:
                return self.load_global(data[_GLOBAL])
            if _TUPLE in data:
                return self.load_tuple(data[_TUPLE])
            if _SET in data:
                return self.load_set(data[_SET])
            if _NP_NDARRAY in data:
                return self.load_np_ndarray(data[_NP_NDARRAY])
            if _NP_NDARRAY_O in data:
                return self.load_np_ndarray_o_type(data[_NP_NDARRAY_O])
            if _NP_DATATYPE in data:
                return self.load_np_datatype(data[_NP_DATATYPE])
            if _KERAS_MODEL in data:
                return self.load_keras_model(data[_KERAS_MODEL])
            return self.load_dict(data)
        f = self.dispatch.get(t)
        if f:
            return f(self, data)

        raise HPicklerError("Unsupported data found: %s" % repr(data))

    dispatch = {}

    def load_primitive(self, data):
        return data

    dispatch[type(None)] = load_primitive
    dispatch[bool] = load_primitive
    dispatch[int] = load_primitive
    dispatch[float] = load_primitive

    def load_string(self, data):
        self.memoize(data)
        return data

    dispatch[str] = load_string

    """def load_unicode(self, data):
        obj = data[()].decode('utf8')
        self.memoize(obj)
        return obj

    dispatch[_UNICODE] = load_unicode"""

    def load_memo(self, data):
        return self.memo[data]

    def load_bytes(self, data):
        obj = data.encode('utf-8')
        self.memoize(obj)
        return obj

    def load_list(self, data):
        obj = [self.load_all(e) for e in data]
        return obj

    dispatch[list] = load_list

    def load_tuple(self, data):
        obj = self.load_all(data)
        return tuple(obj)

    def load_set(self, data):
        obj = self.load_all(data)
        return tuple(obj)

    def load_dict(self, data):
        newdict = {}
        _keys = data.pop(_KEYS, [])
        for k in _keys:
            v = data[str(k)]
            """if k == 'config' and isinstance(v, dict):
                newdict[k] = v
            else:"""
            newdict[k] = self.load_all(v)

        return newdict

    def find_class(self, module, name):
        if module == 'copy_reg' and not six.PY2:
            module = 'copyreg'
        elif module == '__builtin__' and not six.PY2:
            module = 'builtins'
        __import__(module, level=0)
        mod = sys.modules[module]
        return getattr(mod, name)

    def load_global(self, data):
        module = data[0]
        name = data[1]
        func = self.find_class(module, name)
        self.memoize(func)
        return func

    def load_reduce(self, data):
        """
        Build object
        """
        _func = data[_FUNC]
        func = self.load_all(_func)
        assert callable(func), "%r" % func

        _args = data[_ARGS]
        args = self.load_all(_args)

        try:
            obj = args[0].__new__(args[0], * args)
        except:
            obj = func(*args)

        _state = data.get(_STATE)
        if _state:
            state = self.load_all(_state)
            setstate = getattr(obj, "__setstate__", None)
            if setstate:
                setstate(state)
            else:
                assert (type(state) is dict)
                for k, v in state.items():
                    setattr(obj, k, v)

        if self.verbose:
            print(func)
        self.memoize(obj)
        return obj

    def load_np_ndarray_o_type(self, data):
        _dtype = self.load_all(data[_DTYPE])
        _values = self.load_all(data[_VALUES])
        obj = numpy.array(_values, dtype=_dtype)

        return obj

    def load_np_ndarray(self, data):
        obj = self.weights[str(data)][()]
        return obj

    def load_np_datatype(self, data):
        _datatype = self.load_all(data[_DATATYPE])
        _value = self.load_all(data[_VALUE])
        obj = _datatype(_value)

        return obj

    def load_keras_model(self, data):
        obj = load_model(self.keras_models[str(data)])
        self.memoize(obj)
        return obj


def dump_model_to_h5(obj, file_path, verbose=0,
                     store_hyperparameter=True):
    """
    Parameters
    ----------
    obj : python object
    file_path : str or hdf5.File or hdf5.Group object
    verbose : 0 or 1
    store_hyperparameter : bool
        whether to save model hyperparameters for tuning.
    """
    return ModelToHDF5(verbose=verbose).dump(
        obj, file_path, store_hyperparameter=store_hyperparameter)


def load_model_from_h5(file_path, verbose=0):
    """
    file_path : str or hdf5.File or hdf5.Group object
    verbose : 0 or 1
    """
    return HDF5ToModel(verbose=verbose).load(file_path)
