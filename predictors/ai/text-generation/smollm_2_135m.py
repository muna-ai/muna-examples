#
#   Muna
#   Copyright © 2025 NatML Inc. All Rights Reserved.
#

from muna import compile, Sandbox
from muna.beta import Message
from llama_cpp import Llama
from pathlib import Path
from pydantic import BaseModel
from typing import Iterator, Literal

model_path = Path("test/models/smollm2_135m.gguf")
model = Llama(
    model_path=model_path.name if not model_path.exists() else str(model_path),
    verbose=False
)

@compile(
    tag="@yusuf/smollm2-135m",
    description="Generate text with HuggingFace SmolLM2 135M.",
    sandbox=Sandbox()
        .apt_install("clang")
        .pip_install("llama-cpp-python")
        .upload_file(model_path)
)
def predict(messages: list[Message]) -> Iterator[str]:
    for token in model.create_chat_completion(messages=messages, max_tokens=50_000, stream=True):
       yield token