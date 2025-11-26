#
#   Muna
#   Copyright © 2025 NatML Inc. All Rights Reserved.
#

# /// script
# requires-python = ">=3.11"
# dependencies = ["huggingface_hub", "muna", "onnxruntime", "sounddevice"]
# ///

from huggingface_hub import hf_hub_download
from json import loads as load_json
from muna import compile, Parameter, Sandbox
from muna.beta import OnnxRuntimeInferenceSessionMetadata
from numpy import (
    arange, array, asarray, expand_dims, float32, int32,
    int64, load as load_npz, max, ndarray, savez
)
from numpy.random import randn
from onnxruntime import InferenceSession
from pathlib import Path
from re import split
from torch import cat, from_numpy
from torch.nn.functional import pad
from typing import Annotated, Literal

from py.helper import UnicodeProcessor

GenerationVoice = Literal["M1", "M2", "F1", "F2"]

# Download models
HF_REPO_ID = "Supertone/supertonic"
duration_predictor_path = hf_hub_download(repo_id=HF_REPO_ID, filename="onnx/duration_predictor.onnx")
text_encoder_path = hf_hub_download(repo_id=HF_REPO_ID, filename="onnx/text_encoder.onnx")
vector_estimator_path = hf_hub_download(repo_id=HF_REPO_ID, filename="onnx/vector_estimator.onnx")
vocoder_path = hf_hub_download(repo_id=HF_REPO_ID, filename="onnx/vocoder.onnx")
config_path = hf_hub_download(repo_id=HF_REPO_ID, filename="onnx/tts.json")
unicode_indexer_path = hf_hub_download(repo_id=HF_REPO_ID, filename="onnx/unicode_indexer.json")

# Download voices
VOICE_STYLE_FILES: dict[GenerationVoice, str] = {
    "M1": "voice_styles/M1.json",
    "M2": "voice_styles/M2.json",
    "F1": "voice_styles/F1.json",
    "F2": "voice_styles/F2.json",
}
voices_path = Path("voices.npz")
if not voices_path.exists():
    voices = dict[str, ndarray]()
    for voice, remote_path in VOICE_STYLE_FILES.items():
        local_path = hf_hub_download(repo_id=HF_REPO_ID, filename=remote_path)
        voice_data = load_json(Path(local_path).read_text())
        voices[f"{voice}_style_ttl"] = asarray(voice_data["style_ttl"]["data"], dtype=float32)
        voices[f"{voice}_style_dp"] = asarray(voice_data["style_dp"]["data"], dtype=float32)
    savez(voices_path, **voices)

# Load models and voices
duration_predictor = InferenceSession(duration_predictor_path)
text_encoder = InferenceSession(text_encoder_path)
vector_estimator = InferenceSession(vector_estimator_path)
vocoder = InferenceSession(vocoder_path)
voices = load_npz(voices_path)
text_processor = UnicodeProcessor(unicode_indexer_path)

# Load configuration
config = load_json(Path(config_path).read_text())
sample_rate: int = config["ae"]["sample_rate"]
base_chunk_size = config["ae"]["base_chunk_size"]
chunk_compress_factor = config["ttl"]["chunk_compress_factor"]
latent_dim = config["ttl"]["latent_dim"]

@compile(
    tag="@supertone/supertonic",
    description="Perform text-to-speech with Supertonic.",
    sandbox=Sandbox()
        .pip_install("huggingface_hub", "onnxruntime")
        .run_commands("git clone https://github.com/supertone-inc/supertonic.git"),
    metadata=[
        OnnxRuntimeInferenceSessionMetadata(session=duration_predictor, model_path=duration_predictor_path),
        OnnxRuntimeInferenceSessionMetadata(session=text_encoder, model_path=text_encoder_path),
        OnnxRuntimeInferenceSessionMetadata(session=vector_estimator, model_path=vector_estimator_path),
        OnnxRuntimeInferenceSessionMetadata(session=vocoder, model_path=vocoder_path),
    ]
)
def generate_speech(
    text: Annotated[str, Parameter.Generic(description="Text to generate speech from.")],
    *,
    voice: Annotated[GenerationVoice, Parameter.AudioVoice(description="Generation voice.")],
    speed: Annotated[float, Parameter.AudioSpeed(
        description="Voice speed multiplier.",
        min=0.25,
        max=2.0,
    )]=1.0,
    silence_duration: Annotated[float, Parameter.Numeric(
        description="Silence duration between chunks, in seconds.",
        min=0.0,
        max=1.0
    )]=0.3,
    diffusion_steps: Annotated[int, Parameter.Numeric(
        description="Number of diffusion steps.",
        min=1,
        max=10
    )]=5,
) -> Annotated[ndarray, Parameter.Audio(
    description="Linear PCM audio samples with shape (F,) and sample rate 44.1KHz.",
    sample_rate=sample_rate,
)]:
    """
    Perform text-to-speech using the helper utilities.
    """    
    # Perform TTS
    text_chunks = _chunk_text(text)
    chunk_count = len(text_chunks)
    style_ttl = voices[f"{voice}_style_ttl"].repeat(chunk_count, axis=0)
    style_dp = voices[f"{voice}_style_dp"].repeat(chunk_count, axis=0)
    wav_chunks, durations = _infer( # (N,F), (N,)
        text_chunks,
        style_dp=style_dp,
        style_ttl=style_ttl,
        diffusion_steps=diffusion_steps,
        speed=speed
    )
    wav_chunks = from_numpy(wav_chunks)
    durations = from_numpy(durations)
    # Concatenate wav chunks with silence
    silence_samples = int(silence_duration * sample_rate)
    sample_counts = (durations * sample_rate).int()
    trimmed_chunks = [wav_chunk[:count.item()] for wav_chunk, count in zip(wav_chunks, sample_counts)]
    wav = cat([pad(wav_chunk, (0, silence_samples)) for wav_chunk in trimmed_chunks[:-1]] + [trimmed_chunks[-1]])
    # Trim audio to duration
    total_samples = sample_counts.sum().item() + silence_samples * (len(trimmed_chunks) - 1)
    wav = wav[:total_samples]
    # Return
    return wav.numpy()

def _infer( # CHECK
    text_list: list[str],
    *,
    style_dp: ndarray,
    style_ttl: ndarray,
    diffusion_steps: int=5,
    speed: float = 1.05
) -> tuple[ndarray, ndarray]:
    batch_size = len(text_list)
    text_ids, text_mask = text_processor(text_list)
    dur_onnx = duration_predictor.run(None, {
        "text_ids": text_ids,
        "style_dp": style_dp,
        "text_mask": text_mask
    })[0]
    dur_onnx = dur_onnx / speed
    text_emb_onnx = text_encoder.run(None, {
        "text_ids": text_ids,
        "style_ttl": style_ttl,
        "text_mask": text_mask
    })[0]  # dur_onnx: [batch_size]
    xt, latent_mask = _sample_noisy_latent(dur_onnx)
    total_step_np = array([diffusion_steps] * batch_size, dtype=float32)
    for step in range(diffusion_steps):
        current_step = array([step] * batch_size, dtype=float32)
        xt = vector_estimator.run(None, {
            "noisy_latent": xt,
            "text_emb": text_emb_onnx,
            "style_ttl": style_ttl,
            "text_mask": text_mask,
            "latent_mask": latent_mask,
            "current_step": current_step,
            "total_step": total_step_np,
        })[0]
    wav = vocoder.run(None, { "latent": xt })[0]
    return wav, dur_onnx

def _chunk_text( # CHECK # Make functional
    text: str,
    *,
    max_len: int=300
) -> list[str]:
    """
    Split text into chunks by paragraphs and sentences.
    """
    # Split by paragraph (two or more newlines)
    paragraphs = [p.strip() for p in split(r"\n\s*\n+", text.strip()) if p.strip()]
    chunks = []
    for paragraph in paragraphs:
        paragraph = paragraph.strip()
        if not paragraph:
            continue
        # Split by sentence boundaries (period, question mark, exclamation mark followed by space)
        # But exclude common abbreviations like Mr., Mrs., Dr., etc. and single capital letters like F.
        pattern = r"(?<!Mr\.)(?<!Mrs\.)(?<!Ms\.)(?<!Dr\.)(?<!Prof\.)(?<!Sr\.)(?<!Jr\.)(?<!Ph\.D\.)(?<!etc\.)(?<!e\.g\.)(?<!i\.e\.)(?<!vs\.)(?<!Inc\.)(?<!Ltd\.)(?<!Co\.)(?<!Corp\.)(?<!St\.)(?<!Ave\.)(?<!Blvd\.)(?<!\b[A-Z]\.)(?<=[.!?])\s+"
        sentences = split(pattern, paragraph)
        current_chunk = ""
        for sentence in sentences:
            if len(current_chunk) + len(sentence) + 1 <= max_len:
                current_chunk += (" " if current_chunk else "") + sentence
            else:
                if current_chunk:
                    chunks.append(current_chunk.strip())
                current_chunk = sentence
        if current_chunk:
            chunks.append(current_chunk.strip())
    return chunks

def _sample_noisy_latent(duration: ndarray) -> tuple[ndarray, ndarray]: # CHECK
    bsz = len(duration)
    wav_len_max = max(duration) * sample_rate
    wav_lengths = (duration * sample_rate).astype(int64)
    chunk_size = base_chunk_size * chunk_compress_factor
    latent_len = ((wav_len_max + chunk_size - 1) / chunk_size).astype(int32)
    noisy_latent = randn(bsz, latent_dim * chunk_compress_factor, latent_len).astype(float32)
    latent_mask = _get_latent_mask(
        wav_lengths,
        base_chunk_size,
        chunk_compress_factor
    )
    noisy_latent = noisy_latent * latent_mask
    return noisy_latent, latent_mask

def _get_latent_mask( # CHECK # Convert to PyTorch
    wav_lengths: ndarray,
    base_chunk_size: int,
    chunk_compress_factor: int
) -> ndarray:
    """
    Get latent mask from wav lengths.
    """
    latent_size = base_chunk_size * chunk_compress_factor
    latent_lengths = (wav_lengths + latent_size - 1) // latent_size
    latent_mask = _length_to_mask(latent_lengths)
    return latent_mask

def _length_to_mask( # CHECK # Convert to PyTorch
    lengths: ndarray,
    *,
    max_len: int | None=None
) -> ndarray:
    """
    Convert lengths to binary mask with shape (B, 1, max_len).
    """
    max_len = max_len or lengths.max()
    ids = arange(0, max_len)
    mask = (ids < expand_dims(lengths, axis=1)).astype(float32)
    return mask.reshape(-1, 1, max_len)

if __name__ == "__main__":
    import sounddevice as sd
    audio = generate_speech(
        text="Supertonic is such an odd model.",
        voice="F2"
    )
    sd.play(audio, samplerate=sample_rate)
    sd.wait()