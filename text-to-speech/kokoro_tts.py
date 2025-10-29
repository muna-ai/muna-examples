#
#   Muna
#   Copyright © 2025 NatML Inc. All Rights Reserved.
#

from huggingface_hub import hf_hub_download
from json import loads
from muna import compile, Parameter, Sandbox
from muna.beta import OnnxRuntimeInferenceSessionMetadata
from numpy import array, float32, fromfile, int64, load, ndarray, ones_like, savez
from onnxruntime import InferenceSession
from pathlib import Path
from typing import get_args, Annotated, Literal

# Language codes
GenerationLanguage = Literal[
    "en-US", "en-GB", "es-ES", "fr-FR", "hi-IN",
    "it-IT", "ja-JP", "pt-BR", "zh-CN"
]

# Generation voices
GenerationVoice = Literal[
    "af", "af_bella", "af_nicole", "af_sarah", "af_sky",
    "am_adam", "am_michael",
    "bf_emma", "bf_isabella",
    "bm_george", "bm_lewis"
]

# Download the Kokoro model
kokoro_model_path = hf_hub_download(
    repo_id="onnx-community/Kokoro-82M-ONNX",
    filename="onnx/model_fp16.onnx"
)

# Download the vocabulary
kokoro_tokenizer_path = hf_hub_download(
    repo_id="onnx-community/Kokoro-82M-ONNX",
    filename="tokenizer.json"
)
KOKORO_VOCAB = loads(Path(kokoro_tokenizer_path).read_text())["model"]["vocab"]

# Download ByT5-based grapheme to phoneme converter
byt5_model_path = hf_hub_download(
    repo_id="OpenVoiceOS/g2p-mbyt5-12l-ipa-childes-espeak-onnx",
    filename="fdemelo_g2p-mbyt5-12l-ipa-childes-espeak.onnx"
)

# Download and create an NPZ file of all Kokoro voices
def _load_kokoro_voice(voice_name: str) -> ndarray:
    voice_path = hf_hub_download(
        repo_id="onnx-community/Kokoro-82M-ONNX",
        filename=f"voices/{voice_name}.bin"
    )
    return fromfile(voice_path, dtype=float32).reshape(-1, 1, 256)

kokoro_voices_path = Path("kokoro_voices.npz")
if not kokoro_voices_path.exists():
    kokoro_voices = { voice_name: _load_kokoro_voice(voice_name) for voice_name in get_args(GenerationVoice) }
    savez(kokoro_voices_path, **kokoro_voices)

# Load all voices from the NPZ file
voices = load(kokoro_voices_path)

# Load model and converter
kokoro_model = InferenceSession(kokoro_model_path)
byt5_model = InferenceSession(byt5_model_path)

@compile(
    tag="@hexgrad/kokoro-tts",
    description="Perform text-to-speech with Kokoro TTS.",
    sandbox=Sandbox().pip_install("huggingface_hub", "numpy", "onnxruntime"),
    metadata=[
        OnnxRuntimeInferenceSessionMetadata(session=kokoro_model, model_path=kokoro_model_path),
        OnnxRuntimeInferenceSessionMetadata(session=byt5_model, model_path=byt5_model_path),
    ]
)
def generate_speech(
    text: Annotated[str, Parameter.Generic(description="Text to generate speech from")],
    *,
    voice: Annotated[GenerationVoice, Parameter.AudioVoice(description="Generation voice.")],
    language: Annotated[GenerationLanguage, Parameter.Generic(description="Generation language.")]="en-US",
    speed: Annotated[float, Parameter.AudioSpeed(
        description="Voice speed multiplier.",
        min=0.5,
        max=2.0
    )]=1.0
) -> Annotated[ndarray, Parameter.Audio(
    description="Linear PCM audio samples with shape (F,) and sample rate 24KHz.",
    sample_rate=24000
)]:
    """
    Perform text-to-speech with Kokoro TTS.
    """
    # Convert text to IPA
    ipa_text = _convert_to_ipa(text, language=language)
    # Convert IPA phonemes to token IDs using Kokoro vocabulary
    all_tokens = [KOKORO_VOCAB[item] for item in ipa_text if item in KOKORO_VOCAB]
    # Truncate to fit context length (512 total, leaving room for 2 padding tokens)
    tokens = all_tokens[:510]
    # Add the pad ids (0 at start and end)
    tokens_with_padding = [0] + tokens + [0]
    # Convert to input tensor
    padded_input_ids = array(tokens_with_padding, dtype=int64)[None]
    # Get voice style based on padded token length
    ref_s = voices[voice][len(tokens_with_padding)]
    # Specify speed
    speed_spec = array([speed], dtype=float32)
    # Run inference
    outputs = kokoro_model.run(None, {
        "input_ids": padded_input_ids,
        "style": ref_s,
        "speed": speed_spec
    })
    # Return the audio data
    return outputs[0].squeeze()

def _convert_to_ipa(
    text: str,
    *,
    language: GenerationLanguage
) -> str:
    """
    Convert a string to an IPA string with ByT5-G2P.
    """
    # Tokenize input (ByT5-G2P expects angle brackets around language code)
    prompt = f"<{language}>: {text}"
    num_special_tokens = 3
    input_ids = array([list(prompt.encode())]) + num_special_tokens
    attention_mask = ones_like(input_ids)
    # Generate autoregressively
    eos_token_id = 1
    max_length = 510
    decoder_input_ids = [0]
    for idx in range(max_length):
        logits = byt5_model.run(None, {
            "input_ids": input_ids,
            "attention_mask": attention_mask,
            "decoder_input_ids": array(decoder_input_ids)[None]
        })[0]
        last_token_logits = logits[:,-1,:]
        next_id = int(last_token_logits.argmax(-1).item())
        decoder_input_ids.append(next_id)
        if next_id == eos_token_id:
            break
    # Decode to IPA
    output_ids = [token_id - num_special_tokens for token_id in decoder_input_ids]
    phoneme_data = bytes([token_id for token_id in output_ids if 0 <= token_id < 256])
    phonemes = phoneme_data.decode()
    # Return
    return phonemes

if __name__ == "__main__":
    import sounddevice as sd
    # Generate audio
    audio = generate_speech(
        text="It was the best of times.",
        voice="bm_lewis",
        language="en-US",
        speed=1.0
    )
    print(audio.shape)
    # Playback
    sd.play(audio, samplerate=24_000)
    sd.wait()