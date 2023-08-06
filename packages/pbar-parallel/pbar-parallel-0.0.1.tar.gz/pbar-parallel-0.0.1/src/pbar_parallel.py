from typing import Union, Optional, Dict, Any

from attr import attrs, attrib
from joblib import Parallel, delayed

from _star_attr import star_attrs, star_attrib
from tqdm import tqdm
from tqdm.notebook import tqdm_notebook


def _default_bar_func_mapping():
    return {
        'tqdm': lambda args: lambda x: tqdm(x, **args),
        'tqdm_notebook': lambda args: lambda x: tqdm_notebook(x, **args),
        'False': lambda args: iter,
        'None': lambda args: iter,
    }


@attrs(auto_attribs=True, frozen=True, slots=True)
class _Executor:
    bar_key: str
    tqdm_kwargs: Dict[str, Any]
    _joblib_kwargs: Dict[str, Any]
    _bar_mapping: Dict = attrib(factory=_default_bar_func_mapping)

    def __call__(self, jobs):
        if str(self.bar_key) in self._bar_mapping.keys():
            bar_func = self._bar_mapping[str(self.bar_key)](self.tqdm_kwargs)
        else:
            raise ValueError(f"Illegal string key for bar_type: {self.bar_key}, use one of these instead:"
                             f"{list(self._bar_mapping.keys)})")
        return Parallel(**self._joblib_kwargs)(bar_func(jobs))


@star_attrs(auto_attribs=True, frozen=True, slots=True)
class PBarParallel:

    bar: Optional[Union[str, bool]] = "tqdm"
    joblib_kwargs: Dict[str, Any] = star_attrib(kw_only=True)

    def __call__(self, **tqdm_kwargs):
        return _Executor(bar_key=self.bar, tqdm_kwargs=tqdm_kwargs, joblib_kwargs=self.joblib_kwargs)
