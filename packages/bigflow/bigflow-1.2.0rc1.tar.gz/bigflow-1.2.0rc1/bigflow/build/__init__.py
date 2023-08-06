from bigflow.commons import public

@public()
def setup(**kwargs):
    """Specify parameters of Bigflow project. Must me called from `setup.py`
    """
    # Laziliy import 'bigflow.dist' as it depends on 'setuptools'
    import bigflow.build.dist as d
    return d.setup(**kwargs)


# TODO: Remove functions in v2.0
import bigflow.build.dist as _dist
_reason = "Use `bigflow.build.setup` instead"
default_project_setup = public(deprecate_reason=_reason)(_dist.default_project_setup)
auto_configuration = public(deprecate_reason=_reason)(_dist.auto_configuration)
project_setup = public(deprecate_reason=_reason)(_dist.project_setup)
__all__ = [
    'default_project_setup',
    'auto_configuration',
    'project_setup',
]