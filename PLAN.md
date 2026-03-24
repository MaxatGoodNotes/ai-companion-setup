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

## Phase 4 — Smart LLM Router (Next)

### Problem
Dolphin 8B (local, uncensored) handles conversation and NSFW freely but lacks reasoning depth. Gemini Flash (cloud, $0.10/1M tokens) is much smarter but censors NSFW content. Manual `/escalate` creates friction — the user must decide when local isn't good enough.

### Solution: Sentence Embedding Classifier
A 22MB pre-trained sentence transformer (`all-MiniLM-L6-v2`) classifies each user message in ~5ms and routes it to the right backend. No training required — uses cosine similarity against curated example clusters.

### Architecture

```
User message
    |
    v
[NSFW keyword check] ---> NSFW? ---> Dolphin (local)
    |
    v (SFW)
[Sentence embedding]
    |
    v
[Cosine similarity vs local/cloud centroids]
    |
    +-- closer to "local" cluster ---> Dolphin (local)
    +-- closer to "cloud" cluster ---> Gemini Flash (cloud)
```

### Routing Categories

**Always local (Dolphin 8B):**
- NSFW / sexual / dark humor / edgy content
- Emotional support, venting, personal topics
- Roleplay, character interactions, casual banter
- Opinion-seeking ("what do you think about...")
- Short casual messages

**Cloud-eligible (Gemini Flash):**
- Factual questions ("what is...", "how does...")
- Technical help (code, math, debugging)
- Analysis, comparison, summarization
- Web search queries
- Long-form reasoning tasks

### Implementation Plan

1. **`llm_router.py`** — new module in `src/open_llm_vtuber/`
   - `LLMRouter` class: loads `all-MiniLM-L6-v2` at startup
   - `router_examples.json`: curated examples (~50 per category) for centroid computation
   - `route(message) -> "local" | "cloud"`: NSFW keyword check first, then embedding similarity
   - Configurable bias toward local (threshold offset) to preserve immersion as default
   - Logging: every routing decision logged with confidence score for tuning

2. **`conf.yaml` changes**
   - Add `gemini_llm` config under `llm_config` with API key (via env var)
   - Add `router_config` section: `enabled: true`, `cloud_provider: gemini_llm`, `local_bias: 0.05`

3. **Agent integration**
   - Modify `basic_memory_agent` to accept a router instance
   - Before calling LLM, run `router.route(message)` to pick provider
   - If cloud is selected, swap the LLM client for that call only
   - If cloud fails (rate limit, network), fall back to local silently

4. **Manual override commands**
   - `/local` — force next response from Dolphin regardless of routing
   - `/cloud` — force next response from Gemini regardless of routing
   - `/router` — show last 5 routing decisions with confidence scores

5. **Dependencies**
   - `sentence-transformers` (~1MB, torch already installed)
   - `google-generativeai` or use existing `openai_compatible_llm` with Gemini's OpenAI-compatible endpoint
   - `all-MiniLM-L6-v2` model weights (~22MB, downloaded once to `models/`)

6. **Tuning workflow**
   - Run for a week with logging enabled
   - Review misrouted messages in logs
   - Add misrouted examples to `router_examples.json` and recompute centroids
   - Adjust `local_bias` threshold if too many/few messages go to cloud

### Design Decisions
- **Default is always local** — cloud is opt-in by the classifier, not opt-out. If the classifier is uncertain, it stays on Dolphin. Immersion > intelligence.
- **No LLM-based routing** — the local 8B model can't reliably judge its own competence. A separate tiny classifier avoids this trap.
- **NSFW check is keyword-based, not ML** — keywords are deterministic and reliable for this; false negatives here would break immersion via Gemini refusal.
- **Stateless per-message routing** — each message routed independently. No conversation-level state (if a technical conversation drifts to banter, the next message correctly routes back to local).

## Pending — Future Ideas
- Voice cloning / custom TTS voice
- Multi-character support (switch models via command)
- Streaming response improvements
- Mobile-friendly UI adjustments
- Affection decay over time (if no sessions for N days)
- Memory importance scoring and pruning
