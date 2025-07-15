import torch
from transformers import AutoTokenizer, AutoModelForCausalLM

# Set the device to CUDA if a GPU is available, otherwise use the CPU
DEVICE = "cuda" if torch.cuda.is_available() else "cpu"

# Use float16 for GPU for better performance, otherwise use float32 for CPU
DTYPE = torch.float16 if DEVICE == "cuda" else torch.float32

# The model identifier for the main Moondream 2 repository
MODEL_ID = "vikhyatk/moondream2"

# The specific revision that corresponds to the 0.5B parameter model
REVISION = "2024-08-26"

# Load the tokenizer for the specified model and revision
tokenizer = AutoTokenizer.from_pretrained(MODEL_ID, revision=REVISION)

# Load the 0.5B model from the pretrained repository
# trust_remote_code=True is required to execute model-specific code
# device_map automatically places the model on the available device (GPU or CPU)
moondream_0_5B = AutoModelForCausalLM.from_pretrained(
    MODEL_ID,
    revision=REVISION,
    trust_remote_code=True,
    torch_dtype=DTYPE,
    device_map={"": DEVICE}
)

# You can now use the 'moondream_0_5B' model for inference
