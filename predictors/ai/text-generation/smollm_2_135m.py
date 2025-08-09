#
#   Muna
#   Copyright © 2025 NatML Inc. All Rights Reserved.
#

# /// script
# requires-python = ">=3.11"
# dependencies = [
#     "huggingface_hub",
#     "llama-cpp-python",
#     "muna"
# ]
# ///

from huggingface_hub import hf_hub_download
from llama_cpp import Llama
from muna import compile, Sandbox
from muna.beta import Message
from typing import Iterator

model_path = hf_hub_download(
    "unsloth/SmolLM2-135M-Instruct-GGUF",
    "SmolLM2-135M-Instruct-Q8_0.gguf"
)
model = Llama(model_path=model_path, verbose=False)

@compile(
    tag="@huggingface/smollm2-135m",
    description="Generate text with HuggingFace SmolLM2 135M.",
    sandbox=Sandbox()
        .apt_install("clang")
        .pip_install("huggingface_hub", "llama-cpp-python")
        .upload_file(model_path)
)
def predict(messages: list[Message]) -> Iterator[str]:
    for token in model.create_chat_completion(messages=messages, max_tokens=50_000, stream=True):
       yield token