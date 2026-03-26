from .core.llm import *
from .core.pdf import *
from .core.tree import *
from .core.logging import *

# ---------------------------------------------------------------------------
# Backward-compatibility wrappers for legacy symbols that were previously
# defined in utils.py but are no longer present in the new core modules.
# These delegates allow existing code that imports from pageindex.utils to
# continue functioning without modification.
# ---------------------------------------------------------------------------
import asyncio as _asyncio
from typing import Any as _Any
from . import core as _core_pkg
from .core import llm as _core_llm


def llm_completion(*args: _Any, **kwargs: _Any) -> _Any:
    """Backward-compatible wrapper: delegates to ChatGPT_API in core.llm."""
    if hasattr(_core_llm, "llm_completion"):
        return _core_llm.llm_completion(*args, **kwargs)
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
    # Fallback: run sync completion in a thread executor
    loop = _asyncio.get_running_loop()
    return await loop.run_in_executor(None, llm_completion, *args, **kwargs)
