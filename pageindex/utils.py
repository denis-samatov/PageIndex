from .core.llm import *
from .core.pdf import *
from .core.tree import *
from .core.logging import *
from .config import ConfigLoader, PageIndexConfig

# ---------------------------------------------------------------------------
# Backward-compatibility wrappers for legacy symbols that were previously
# defined in utils.py but are no longer present in the new core modules.
# These delegates allow existing code that imports from pageindex.utils to
# continue functioning without modification.
# ---------------------------------------------------------------------------
import asyncio as _asyncio
import functools as _functools
from typing import Any as _Any
from .core import llm as _core_llm


def llm_completion(*args: _Any, **kwargs: _Any) -> _Any:
    """Backward-compatible wrapper: delegates to ChatGPT_API in core.llm.
    
    If the caller passes return_finish_reason=True (legacy kwarg), we route
    to ChatGPT_API_with_finish_reason and return (response, finish_reason).
    """
    return_finish_reason = kwargs.pop("return_finish_reason", False)
    if hasattr(_core_llm, "llm_completion"):
        return _core_llm.llm_completion(*args, **kwargs)
    if return_finish_reason and hasattr(_core_llm, "ChatGPT_API_with_finish_reason"):
        return _core_llm.ChatGPT_API_with_finish_reason(*args, **kwargs)
    if hasattr(_core_llm, "ChatGPT_API"):
        return _core_llm.ChatGPT_API(*args, **kwargs)
    raise RuntimeError(
        "llm_completion is not available in pageindex.core.llm. "
        "Update your code to use ChatGPT_API directly."
    )


async def llm_acompletion(*args: _Any, **kwargs: _Any) -> _Any:
    """Backward-compatible async wrapper: delegates to ChatGPT_API_async in core.llm."""
    if hasattr(_core_llm, "llm_acompletion"):
        return await _core_llm.llm_acompletion(*args, **kwargs)
    if hasattr(_core_llm, "ChatGPT_API_async"):
        return await _core_llm.ChatGPT_API_async(*args, **kwargs)
    # Fallback: run sync completion in a thread executor using functools.partial
    # to safely pass keyword arguments (run_in_executor doesn't accept kwargs)
    loop = _asyncio.get_running_loop()
    return await loop.run_in_executor(
        None, _functools.partial(llm_completion, *args, **kwargs)
    )
