# AI Companion — Development Plan

## Completed

### witchZ3 Model Integration
- Extracted and configured witchZ3 Live2D model
- Added LipSync group (ParamMouthOpenY) for mouth sync with TTS
- Reordered expressions: face effects (F1-F11) and poses (N1-N10) at low indices, toggle expressions (E, Q, R, T, ET, W, Y) at high indices
- Created custom expressions: ET.exp3.json (combined clothes+underwear), F11.exp3.json (fixed to question mark), tongue.exp3.json

### Chat Command System
- `/help` — compact command listing
- 20+ transient expression commands (face effects F-series, poses N-series)
- Persistent toggle commands via frontend script injection (clothes, hair, body, head, cover)
- Timed toggle for `/tongue` (forces mouth open + tongue for 1.2s)
- Silent WAV payload trick to carry expressions through the audio pipeline

### Persistent Toggle System (toggle-inject.js)
- WebSocket Proxy intercepts `toggle-parameter` messages from backend
- `requestAnimationFrame` loop writes parameter overrides to both live values and saved parameters buffer every frame
- Supports three command types: persistent toggles, timed toggles, and `/reset`
- Exposed `window._L2DM` in main bundle for model access

### Expression Mapping Audit
- Fixed F9/F10/F11 index swaps (angry, sweat, question were mismatched)
- Corrected N-series labels (N1=lipstick, N3=cat scratch, N4=whip, N6=cat paw)
- Removed phantom commands (kiss, bite, sugar) that mapped to wrong effects
- Added tongue (Param60 in mouth group — requires forced mouth open)

### Persona & LLM Expression Awareness
- Sharp, witty, brutally honest persona prompt
- LLM expression prompt with categorized keywords (emotions, reactions, cat actions, actions)
- emotionMap in model_dict.json maps LLM output tags to expression indices

### Server Improvements
- No-cache headers for all JSON model files (prevents stale browser cache)

## Pending

### Session Memory (Auto-Restore)
- On new WebSocket connection, auto-load most recent chat history
- Restore conversation context so the AI remembers the current session
- Uses existing `chat_history_manager.py` file-based storage

### Long-Term Memory
- Create `long_term_memory.py` with load/save/merge functions
- On disconnect: use LLM to extract key facts from conversation
- Store facts in a JSON file per user
- On connect: inject known facts into system prompt
- Facts should be additive and deduplicated across sessions

### Future Ideas
- Voice cloning / custom TTS voice
- Multi-character support (switch models via command)
- Streaming response improvements
- Mobile-friendly UI adjustments
