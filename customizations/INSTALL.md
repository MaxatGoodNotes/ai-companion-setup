# Installing Customizations

These files extend Open-LLM-VTuber with the witchZ3 model, chat commands, persistent toggles, head animations, an LLM-aware expression system, memory management, and an affection system.

## Files and where they go

| Source (this repo) | Destination (Open-LLM-VTuber root) |
|---|---|
| `conf.yaml` | `conf.yaml` |
| `customizations/model_dict.json` | `model_dict.json` |
| `customizations/expression_commands.py` | `src/open_llm_vtuber/expression_commands.py` |
| `customizations/toggle-inject.js` | `frontend/toggle-inject.js` |
| `customizations/index.html` | `frontend/index.html` |
| `customizations/live2d_expression_prompt.txt` | `prompts/utils/live2d_expression_prompt.txt` |
| `customizations/witchZ3/*.exp3.json` | `live2d-models/witchZ3/witchZ3/` |
| `customizations/witchZ3/witchZ3.model3.json` | `live2d-models/witchZ3/witchZ3/witchZ3.model3.json` |

### Memory & Affection System (new directories)

| Source (this repo) | Destination (Open-LLM-VTuber root) |
|---|---|
| (generated) | `src/open_llm_vtuber/memory/__init__.py` |
| (generated) | `src/open_llm_vtuber/memory/context_manager.py` |
| (generated) | `src/open_llm_vtuber/memory/long_term_memory.py` |
| (generated) | `src/open_llm_vtuber/memory/affection.py` |
| (generated) | `src/open_llm_vtuber/conversations/toggle_tag_parser.py` |
| (generated) | `prompts/utils/memory_summary_prompt.txt` |
| (generated) | `prompts/utils/affection_eval_prompt.txt` |

## Manual patches required

### websocket_handler.py

Imports added at top:
```python
from .memory.context_manager import ContextManager
from .memory.long_term_memory import LongTermMemory
from .memory.affection import AffectionTracker
from .expression_commands import is_expression_command, handle_expression_command
from prompts import prompt_loader
```

Key changes:
- `_init_service_context`: initializes ContextManager, LongTermMemory, AffectionTracker; auto-restores history; reconstructs system prompt with memory/affection context
- `_handle_conversation_trigger`: passes service_context to `handle_expression_command` for memory commands
- `handle_disconnect`: runs `_run_disconnect_memory_tasks` (summarize + affection eval) before cleanup

### service_context.py

- Imports `LongTermMemory`, `AffectionTracker`, `ContextManager`
- Adds `long_term_memory`, `affection`, `context_manager` attributes
- `construct_system_prompt()` injects affection persona modifier, toggle unlock prompts, and long-term memory facts

### basic_memory_agent.py

- Imports `ContextManager`
- Adds `set_context_manager()`, `get_llm()`, `get_memory()`, `maybe_summarize()` methods
- `set_memory_from_history()` applies context window trim on load
- `_to_messages()` applies hard-trim before preparing messages

### config_manager/character.py

- Adds `memory_config: Optional[Dict]` field to `CharacterConfig`

### conversations/single_conversation.py

- Imports `toggle_tag_parser`
- After full response collected, calls `parse_and_send_toggle_tags()` to process affection-gated toggle tags

### main bundle (frontend/assets/main-*.js)

Find the line containing `Live2DDebug` and inject `window._L2DM=LAppLive2DManager` to expose the Live2D manager globally.

### server.py

Add no-cache headers for model files in `CORSStaticFiles.get_response()`:
```python
if path.endswith((".model3.json", ".exp3.json", ".json")):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
```

## witchZ3 model

The witchZ3 Live2D model itself is not included (third-party asset). Place it at `live2d-models/witchZ3/witchZ3/` and copy the expression files from `customizations/witchZ3/` over the originals.
