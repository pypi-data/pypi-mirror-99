
from .json_backend import JsonBackend
from .compress_json_backend import CompressJsonBackend

from .pickle_backend import PickleBackend
from .compress_pickle_backend import CompressPickleBackend

# Failable backends
from .pandas_csv_backend import PandasCsvBackend
from .numpy_backend import NumpyBackend
from .keras_model_backend import KerasModelBackend

from .exceptions import SerializationException, DeserializationException

class Backend:
    def __init__(self, load_kwargs, dump_kwargs):
        self.backends = [
            backend(load_kwargs, dump_kwargs)
            for backend in [
                JsonBackend,
                CompressJsonBackend,
                PickleBackend,
                CompressPickleBackend,
                NumpyBackend,
                PandasCsvBackend,
                KerasModelBackend
            ]
            if backend is not None
        ]


    def dump(self, obj_to_serialize: object, path:str) -> dict:
        """Serialize and save the object at the given path.
        If this backend needs extra informations to de-serialize data, it can 
        return them as a dictionary which will be serialized as a json."
        If the function returns None or does not return, an empty dictionary
        will be used as metadata."""     
        for backend in self.backends:
            if backend.can_serialize(obj_to_serialize, path):
                result = backend.dump(obj_to_serialize, path)
                if result is None:
                    result = {}
                return result
        raise SerializationException(
            "There is no backend to serialize the given object at the given path",
            path,
            obj_to_serialize
            )

    def load(self, metadata:dict, path:str) -> object:
        """Load the method at the given path. If the medod need extra
        informations it can """
        for backend in self.backends:
            if backend.can_deserialize(metadata, path):
                return backend.load(metadata, path)
        raise DeserializationException(
            "There is no backend to deserialize the given object at the given path",
            path
            )