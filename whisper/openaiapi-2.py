from typing import Annotated
from fastapi import FastAPI, Form, File

import torch
import intel_extension_for_pytorch as ipex
from transformers import AutoModelForSpeechSeq2Seq, AutoProcessor, pipeline


from faster_whisper import WhisperModel
import os
from io import BytesIO
import dotenv
import logging

LOGGER = logging.getLogger(__name__)
dotenv.load_dotenv()

DEFAULTS = {
    "MODEL_SIZE": "tiny",
    "DEVICE_TYPE": "cuda",
    "COMPUTE_TYPE": "float16",
    "BEAM_SIZE": 5,
    "VAD_FILTER": "true",
    "MIN_SILENCE_DURATION_MS": 50,
}


def get_env(key):
    return os.environ.get(key, DEFAULTS.get(key))


def get_int_env(key):
    return int(get_env(key))


def get_float_env(key):
    return float(get_env(key))


def get_bool_env(key):
    return get_env(key).lower() == 'true'


model_size = get_env("MODEL_SIZE")
device_type = get_env("DEVICE_TYPE")
compute_type = get_env("COMPUTE_TYPE")
beam_size = get_int_env("BEAM_SIZE")
vad_filter = get_bool_env("VAD_FILTER")
min_silence_duration_ms = get_int_env("MIN_SILENCE_DURATION_MS")
whisper_engine = WhisperModel(model_size, device=device_type, compute_type=compute_type)


#================================
device = "cuda:0" if torch.cuda.is_available() else "cpu"
torch_dtype = torch.bfloat16 

model_id = "openai/whisper-large-v3"

model = AutoModelForSpeechSeq2Seq.from_pretrained(
    model_id, torch_dtype=torch_dtype, low_cpu_mem_usage=True, use_safetensors=True
)
model.to(device)
model.eval()
model = ipex.optimize(model, dtype=torch_dtype)


processor = AutoProcessor.from_pretrained(model_id)

pipe = pipeline(
    "automatic-speech-recognition",
    model=model,
    tokenizer=processor.tokenizer,
    feature_extractor=processor.feature_extractor,
    max_new_tokens=128,
    chunk_length_s=30,
    batch_size=1,
    return_timestamps=True,
    torch_dtype=torch_dtype,
    device=device,
)
#================================


app = FastAPI()


@app.post("/v1/audio/transcriptions")
def create_transcription(file: Annotated[bytes, File()],
                         model: Annotated[str, Form()] = 'whipser-1',
                         language: Annotated[str | None, Form()] = None,
                         prompt: Annotated[str | None, Form()] = None):

    vad_parameters = dict(min_silence_duration_ms=min_silence_duration_ms)
#    segments, _ = whisper_engine.transcribe(BytesIO(file), beam_size=5,
#                                            language=language,
#                                            initial_prompt=prompt,
#                                            word_timestamps=False,
#                                            vad_filter=vad_filter,
#                                            vad_parameters=vad_parameters)
    
#    sentences = []
#    for segment in segments:
#        sentences.append(segment.text)
    with torch.no_grad(), torch.cpu.amp.autocast():
        sentences=pipe(file)
    print(sentences)
    sents=[]
    sents.append(sentences)

    return {
        "text": sentences
    }
