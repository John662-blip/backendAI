from transformers import AutoTokenizer, AutoModelForCausalLM
import torch

class QwenManager16bit:
    def __init__(self, model_name="Qwen/Qwen3-4B-Instruct-2507"):
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        # load model với 16-bit
        self.model = AutoModelForCausalLM.from_pretrained(
            model_name,
            device_map="auto",           
            torch_dtype=torch.float16,   # sử dụng 16-bit
        )

    def generate_json(self, prompt, max_tokens=100):
        inputs = self.tokenizer(prompt, return_tensors="pt")
        outputs = self.model.generate(**inputs, max_new_tokens=max_tokens)
        return self.tokenizer.decode(outputs[0], skip_special_tokens=True)

    def summary_mail_100(self, contentMail, max_tokens=120):
        prompt = f"""
            Bạn là trợ lý AI chuyên tóm tắt email này tối đa 100 từ.
            Hãy tóm tắt email dưới đây một cách ngắn gọn, rõ ràng, tập trung vào nội dung chính

            #Mail : 
            {contentMail}

            ### Yêu cầu:
            - Tóm tắt dưới dạng đoạn văn ngắn.
            - Không lặp lại toàn bộ nội dung.
            - Giữ đúng ngữ cảnh, không bỏ sót thông tin quan trọng.

            ### Tóm tắt:
            """

        inputs = self.tokenizer(prompt, return_tensors="pt").to(self.model.device)
        outputs = self.model.generate(
            **inputs,
            max_new_tokens=max_tokens,
            temperature=0.5,
            top_p=0.9,
            repetition_penalty=1.1
        )

        return self.tokenizer.decode(outputs[0], skip_special_tokens=True)
