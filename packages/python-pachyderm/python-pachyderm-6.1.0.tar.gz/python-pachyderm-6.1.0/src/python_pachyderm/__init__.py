import string as _string
import importlib as _importlib
import enum as _enum
from google.protobuf.internal.enum_type_wrapper import EnumTypeWrapper as _EnumTypeWrapper

from .mixin.pfs import PFSFile, PutFileClient
from .client import Client, ConfigError, BadClusterDeploymentID
from .spout import SpoutManager, SpoutCommit
from .util import put_files, create_python_pipeline, parse_json_pipeline_spec, parse_dict_pipeline_spec
from grpc import RpcError


__all__ = [
    "Client",
    "RpcError",
    "SpoutManager",
    "SpoutCommit",
    "put_files",
    "create_python_pipeline",
    "PFSFile",
    "PutFileClient",
    "parse_json_pipeline_spec",
    "parse_dict_pipeline_spec",
    "ConfigError",
    "BadClusterDeploymentID",
]


try:
    from .version import __version__
    __version__ = __version__
except ModuleNotFoundError:
    # The version module is dynamically generated at install time, so if
    # referencing python-pachyderm without having installed it, the import
    # will fail -- so we just ignore import failures here.
    pass
else:
    __all__.append("__version__")


def _import_protos(path):
    """
    Imports items selectively from the auto-generated proto package.

    Importing is done dynamically so we can selectively blacklist items. We
    also dynamically define enums that build on top of the auto-generated
    protobuf enums, to create a more pythonic API.

    More broadly, the dark magic in here allows us to maintain parity with
    Pachyderm protobufs when they change, without having to maintain a manual
    mapping of protobuf to python_pachyderm values.
    """

    g = globals()
    module = _importlib.import_module(path)
    uppercase_letters = set(_string.ascii_uppercase)
    lowercase_letters = set(_string.ascii_lowercase)

    def import_item(g, module, key):
        value = getattr(module, key)

        if isinstance(value, _EnumTypeWrapper):
            # Dynamically define an enum class that is exported
            g[key] = _enum.Enum(key, {k: v for (k, v) in value.items()})
        else:
            # Export the value
            g[key] = value

        __all__.append(key)

    def should_import(key):
        return key[0] in uppercase_letters and any(c in lowercase_letters for c in key[1:])

    for key in dir(module):
        if should_import(key):
            import_item(g, module, key)
        elif key.startswith("google_dot_protobuf_dot_"):
            sub_module = getattr(module, key)
            for key in dir(sub_module):
                if should_import(key):
                    import_item(g, sub_module, key)


_import_protos("python_pachyderm.proto.pfs.pfs_pb2")
_import_protos("python_pachyderm.proto.pps.pps_pb2")
_import_protos("python_pachyderm.proto.version.versionpb.version_pb2")
_import_protos("python_pachyderm.proto.transaction.transaction_pb2")
_import_protos("python_pachyderm.proto.admin.admin_pb2")
_import_protos("python_pachyderm.proto.auth.auth_pb2")
_import_protos("python_pachyderm.proto.enterprise.enterprise_pb2")
