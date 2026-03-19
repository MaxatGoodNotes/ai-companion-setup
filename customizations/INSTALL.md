# Installing Customizations

These files extend Open-LLM-VTuber with the witchZ3 model, chat commands, persistent toggles, and an LLM-aware expression system.

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

## Manual patches required

### websocket_handler.py

Add this import at the top of `src/open_llm_vtuber/websocket_handler.py`:

```python
from .expression_commands import is_expression_command, handle_expression_command
```

Then in `_handle_conversation_trigger`, add command interception before the normal conversation flow:

```python
async def _handle_conversation_trigger(self, websocket, client_uid, data):
    if data.get("type") == "text-input":
        text = data.get("text", "")
        if is_expression_command(text):
            await handle_expression_command(text, websocket.send_text)
            return
    # ... rest of method unchanged
```

### main bundle (frontend/assets/main-*.js)

Find the line containing `Live2DDebug` and inject `window._L2DM=LAppLive2DManager` to expose the Live2D manager globally. This is needed for toggle-inject.js to access the model.

### server.py

Add no-cache headers for model files in `CORSStaticFiles.get_response()`:

```python
if path.endswith((".model3.json", ".exp3.json", ".json")):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
```

## witchZ3 model

The witchZ3 Live2D model itself is not included (third-party asset). Place it at `live2d-models/witchZ3/witchZ3/` and copy the expression files from `customizations/witchZ3/` over the originals.
