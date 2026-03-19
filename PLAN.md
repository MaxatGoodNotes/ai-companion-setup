# AI Companion — Development Plan

## Completed (Phase 1) — Model & Foundation

### witchZ3 Model Integration
- Extracted and configured witchZ3 Live2D model
- Added LipSync group (ParamMouthOpenY) for mouth sync with TTS
- Reordered expressions: face effects (F1-F11) and poses (N1-N10) at low indices, toggle expressions (E, Q, R, T, ET, W, Y) at high indices
- Created custom expressions: ET.exp3.json (combined clothes+underwear), F11.exp3.json (fixed to question mark), tongue.exp3.json

### Chat Command System
- `/help` — compact command listing
- 20+ transient expression commands (face effects F-series, poses N-series)
- Persistent toggle commands via frontend script injection (clothes, hair, body, head, cover)
- Silent WAV payload trick to carry expressions through the audio pipeline

### Persistent Toggle System (toggle-inject.js)
- WebSocket Proxy intercepts `toggle-parameter` and `play-reaction` messages from backend
- `requestAnimationFrame` loop writes parameter overrides every frame
- Supports persistent toggles and `/reset`
- Exposed `window._L2DM` in main bundle for model access

### Expression Mapping Audit
- Fixed F9/F10/F11 index swaps (angry, sweat, question were mismatched)
- Corrected N-series labels (N1=lipstick, N3=cat scratch, N4=whip, N6=cat paw)
- Removed phantom commands (kiss, bite, sugar) that mapped to wrong effects
- Added tongue (Param60 in mouth group — requires forced mouth open)

### Persona & LLM Expression Awareness
- Sharp, witty, brutally honest persona prompt with anti-leakage guardrails
- LLM expression prompt with categorized keywords (emotions, reactions, cat actions, actions)
- emotionMap in model_dict.json maps LLM output tags to expression indices

### Server Improvements
- No-cache headers for all JSON model files (prevents stale browser cache)

## Completed (Phase 2) — Memory & Affection

### Memory & Context Management
- **Context Manager** (`memory/context_manager.py`): Sliding window of recent messages (configurable, default 30). Overflow triggers LLM summarization of oldest messages into key facts. Hard-trim fallback for safety.
- **Long-Term Memory** (`memory/long_term_memory.py`): Persistent key-fact storage in `memory/{conf_uid}/memories.json`. Facts extracted on disconnect and injected into system prompt on connect. Deduplication, add, clear. Commands: `/memories`, `/forget`, `/summarize`.
- **Auto-Restore History**: On new connection, most recent chat history is automatically loaded so the AI remembers context across page refreshes.
- **Conversation Persistence**: Fixed frontend inadvertently creating new conversations on browser refresh by patching the main bundle.
- **Config**: `memory_config` section in `conf.yaml` and `CharacterConfig` model for tunable thresholds.

### Affection System
- **Affection** (`memory/affection.py`): Relationship score -100 to 100, starts at 0. Tiers: Hostile, Annoyed, Stranger, Acquaintance, Friend, Close, Intimate. Each tier injects a persona modifier into the system prompt. LLM evaluates session quality on disconnect to adjust score. Command: `/affection`.
- **Affection-Gated Toggles**: Close tier (75+) unlocks `[hideclothes]`, `[hidecover]`. Intimate tier (90+) unlocks `[hideunderwear]`, `[hidex]`. Tags parsed from LLM responses in `toggle_tag_parser.py`.
- **Prompt Integration**: `service_context.py` `construct_system_prompt()` injects affection tier modifier, unlocked toggle instructions, and long-term memory facts.

## Completed (Phase 3) — Animations & Reactions

### Keyframe Animation Engine
- **Interpolated animation system**: `requestAnimationFrame` tick loop with `easeInOut` cubic interpolation between keyframes. Replaced earlier `setTimeout`-based approach.
- **Multi-track reactions** (`REACTION_DEFS`): Each reaction defines multiple parameter tracks with independent keyframe timelines, all starting simultaneously.
- **Crash protection**: Tick loop wrapped in try/catch so errors are logged but never kill the animation system. Safe deletion pattern (collect finished anims, delete after iteration).
- **Proper cleanup**: Finished animations restore to their last keyframe value instead of blindly resetting to 0 (fixes params like `ParamEyeROpen` where 0 = eye closed).

### Head Animations
- `/yes` (nod): `ParamAngleY` bounce with gentle eye blink on the downward dip
- `/no` (shake): `ParamAngleX` side-to-side with firm blink at start, determined squint through the shake
- `/tilt` (curious): `ParamAngleZ` 25° tilt with eyeball drift toward tilt direction
- `/confused`: Opposite tilt with question mark (`Param75`) and confused squint
- LLM tags: `[nod]`, `[shake]`, `[tilt]`, `[confused]` — always allowed, not affection-gated

### Body Reactions
- `/dance`: Body sway (`ParamBodyAngleZ` ±22°) + head counter-sway + heart hands (`Param62`) + happy eye squint. ~5.8s duration.
- `/mic`: Microphone prop (`Param57`) + extended dance choreography (~7.6s) + happy squint.
- `/excited`: Quick body wiggle + waving hand (`Param54`) + star eyes (`Param9`) + happy squint. ~2.2s duration.

### Face Reactions
- `/wink`: Right eye close (`ParamEyeROpen`) + left eye smile + head tilt + heart (`Param10`)
- `/think`: Eyes drift up-right (`ParamEyeBallX/Y`) + question mark + head tilt + pondering half-squint
- `/tongue`: Tongue out (`Param60`) + mouth open + playful full squint. Converted from timed toggle to reaction.
- `/faceblack`: Black face (`Param70`) + eyes close completely during blackout. Converted from timed toggle to reaction.

### Affection-Triggered Reactions
- **shy-reject**: Plays when a sensitive toggle is used without sufficient affection. Surprised blink → cross arms (`Param61`) → confusion tilt → blush → anger (`Param76`) → auto re-clothe. Wide-open surprise then angry squint.
- **shy-accept**: Plays when a sensitive toggle is used with sufficient affection. Bashful look down-left (`ParamEyeBallX/Y`) → head tilt → blush + half-closed shy eyes.
- Test commands: `/shyaccept`, `/shyreject` for manual testing.

### Eyelid Enhancements (across all animations)
- `ParamEyeLOpen` / `ParamEyeROpen`: Used for blinks (nod, shake, shy-reject surprise) and closures (faceblack, wink)
- `ParamEyeLSmile` / `ParamEyeRSmile`: Used for happy squints (dance, mic, excited), determined squints (shake, confused), pondering squints (think), bashful squints (shy-accept), angry squints (shy-reject), playful squints (tongue)
- `ParamEyeBallX` / `ParamEyeBallY`: Used for gaze direction (think looks up-right, tilt drifts toward tilt, shy-accept looks down-left)

## Pending

### Future Ideas
- Voice cloning / custom TTS voice
- Multi-character support (switch models via command)
- Streaming response improvements
- Mobile-friendly UI adjustments
- Affection decay over time (if no sessions for N days)
- Memory importance scoring and pruning
