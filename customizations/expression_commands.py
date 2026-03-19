"""
Chat commands for triggering Live2D expressions and persistent toggles.

Commands are typed in the chat input with a `/` prefix (e.g. `/wave`, `/blush`).
They bypass the LLM and instantly trigger the corresponding action on the model.

Expression commands (face effects, poses) are transient — they play once via
the expression system. Toggle commands (body toggles) are persistent — they
directly set model parameters every frame via the injected frontend script.
The same toggle command typed again turns it off.

The command map below is built for the witchZ3 model.
"""

import io
import json
import base64
from loguru import logger


def _generate_silent_wav(duration_ms: int = 100, sample_rate: int = 24000) -> str:
    """Generate a short silent WAV and return it as a base64 string.

    The frontend only applies expressions when audio data is present,
    so we send a tiny inaudible clip to carry the expression payload.
    """
    import struct

    num_samples = int(sample_rate * duration_ms / 1000)
    bits_per_sample = 16
    num_channels = 1
    byte_rate = sample_rate * num_channels * bits_per_sample // 8
    block_align = num_channels * bits_per_sample // 8
    data_size = num_samples * block_align

    buf = io.BytesIO()
    buf.write(b"RIFF")
    buf.write(struct.pack("<I", 36 + data_size))
    buf.write(b"WAVE")
    buf.write(b"fmt ")
    buf.write(struct.pack("<IHHIIHH", 16, 1, num_channels, sample_rate, byte_rate, block_align, bits_per_sample))
    buf.write(b"data")
    buf.write(struct.pack("<I", data_size))
    buf.write(b"\x00" * data_size)

    return base64.b64encode(buf.getvalue()).decode("utf-8")


_SILENT_AUDIO = _generate_silent_wav()

# ── Transient expression commands (face effects & poses) ──
EXPRESSION_COMMANDS: dict[str, dict] = {
    # Face Effects (F-series, indices 0-10)
    "/star": {"index": 0, "label": "Star"},
    "/love": {"index": 1, "label": "Love"},
    "/flash": {"index": 2, "label": "Flash"},
    "/faceblack": {"index": 3, "label": "Face Black"},
    "/blush": {"index": 4, "label": "Blushing"},
    "/mask": {"index": 5, "label": "Mask"},
    "/tears": {"index": 6, "label": "Tears"},
    "/cry": {"index": 6, "label": "Tears"},
    "/exclaim": {"index": 7, "label": "!"},
    "/angry": {"index": 8, "label": "Angry"},
    "/sweat": {"index": 9, "label": "Sweat"},
    "/question": {"index": 10, "label": "?"},
    # Poses & Props (N-series, indices 11-21)
    "/lipstick": {"index": 11, "label": "Lipstick"},
    "/mic": {"index": 12, "label": "Microphone"},
    "/microphone": {"index": 12, "label": "Microphone"},
    "/scratch": {"index": 13, "label": "Cat Scratch"},
    "/whip": {"index": 14, "label": "Whip"},
    "/wave": {"index": 15, "label": "Waving"},
    "/cat": {"index": 16, "label": "Cat Paw"},
    "/hug": {"index": 17, "label": "Chest Hug"},
    "/hearts": {"index": 18, "label": "Heart Hands"},
    "/game": {"index": 19, "label": "Game"},
    "/write": {"index": 20, "label": "Writing"},
}

# ── Persistent toggle commands (body toggles via frontend injection) ──
TOGGLE_COMMANDS: dict[str, str] = {
    "/hideclothes": "Clothes",
    "/hideunderwear": "Clothes + Underwear",
    "/hidebody": "Body",
    "/hidehead": "Head",
    "/shorthair": "Short Hair",
    "/hidecover": "Covering",
    "/tongue": "Tongue Out",
    "/reset": "Reset All Toggles",
}

_ALL_COMMANDS = set(EXPRESSION_COMMANDS) | set(TOGGLE_COMMANDS) | {"/help"}


def is_expression_command(text: str) -> bool:
    """Return True if the text is a recognised /command."""
    token = text.strip().split()[0].lower() if text.strip() else ""
    return token in _ALL_COMMANDS


async def handle_expression_command(text: str, websocket_send) -> None:
    """Parse a /command and dispatch to expression or toggle handler."""
    token = text.strip().split()[0].lower()

    if token == "/help":
        await _send_help(websocket_send)
        return

    if token in TOGGLE_COMMANDS:
        await _handle_toggle(token, websocket_send)
        return

    cmd = EXPRESSION_COMMANDS.get(token)
    if not cmd:
        return

    logger.info(f"Expression command: {token} → index {cmd['index']} ({cmd['label']})")

    payload = {
        "type": "audio",
        "audio": _SILENT_AUDIO,
        "volumes": [0.0] * 5,
        "slice_length": 20,
        "display_text": {
            "text": f"✨ {cmd['label']}",
            "name": "Command",
            "avatar": None,
        },
        "actions": {"expressions": [cmd["index"]]},
        "forwarded": False,
    }
    await websocket_send(json.dumps(payload))


async def _handle_toggle(token: str, websocket_send) -> None:
    """Send a toggle-parameter message that the frontend script intercepts."""
    label = TOGGLE_COMMANDS[token]
    logger.info(f"Toggle command: {token} ({label})")

    await websocket_send(json.dumps({
        "type": "toggle-parameter",
        "command": token,
    }))

    await websocket_send(json.dumps({
        "type": "full-text",
        "text": f"🔀 Toggle: {label}",
    }))


async def _send_help(websocket_send) -> None:
    """Send a compact help listing of all available commands."""
    faces = "/star /love /flash /faceblack /blush /mask /tears /cry /exclaim /angry /sweat /question"
    poses = "/lipstick /mic /scratch /whip /wave /cat /hug /hearts /game /write"
    toggles = "/hideclothes /hideunderwear /hidebody /hidehead /shorthair /hidecover /tongue /reset"

    text = (
        f"Face: {faces}\n"
        f"Poses: {poses}\n"
        f"Toggle (persistent): {toggles}"
    )

    await websocket_send(
        json.dumps({"type": "full-text", "text": text})
    )
