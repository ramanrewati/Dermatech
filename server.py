from threading import Thread
import litserve as ls
import torch
from litserve.specs.openai import ChatCompletionRequest
from qwen_vl_utils import process_vision_info
from transformers import (
    AutoProcessor,
    Qwen2VLForConditionalGeneration,
    TextIteratorStreamer,
)
from src.config import MODEL

class Qwen2VLAPI(ls.LitAPI):
    def setup(self, device):
        self.model = Qwen2VLForConditionalGeneration.from_pretrained(
            MODEL,
            torch_dtype=torch.float16,
            device_map="auto",
        )
        self.processor = AutoProcessor.from_pretrained(MODEL)
        self.streamer = TextIteratorStreamer(
            self.processor.tokenizer,
            skip_prompt=True,
            skip_special_tokens=True,
        )
        self.device = device

    def decode_request(self, request: ChatCompletionRequest, context: dict):
        context["generation_args"] = {
            "max_new_tokens": request.max_tokens if request.max_tokens else 512,
        }
        messages = [
            message.model_dump(exclude_none=True) for message in request.messages
        ]
        
        # Process vision info
        image_inputs, video_inputs = process_vision_info(messages)
        
        # Apply chat template
        text = self.processor.tokenizer.apply_chat_template(
            messages,
            tokenize=False,
            add_generation_prompt=True,
        )
        
        # Process inputs
        inputs = self.processor(
            text=text,
            images=image_inputs,
            videos=video_inputs,
            return_tensors="pt",
        ).to(self.device)
        
        return inputs

    def predict(self, model_inputs, context: dict):
        generation_kwargs = dict(
            **model_inputs,
            streamer=self.streamer,
            **context["generation_args"],
        )
        thread = Thread(target=self.model.generate, kwargs=generation_kwargs)
        thread.start()
        
        for text in self.streamer:
            yield text

if __name__ == "__main__":
    api = Qwen2VLAPI()
    server = ls.LitServer(api, spec=ls.OpenAISpec())
    server.run(port=8000)