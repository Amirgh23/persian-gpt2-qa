"""A small Persian question-answering demo powered by a pretrained GPT-2 model."""

from __future__ import annotations

import argparse
from dataclasses import dataclass


DEFAULT_MODEL = "HooshvareLab/gpt2-fa"


def build_prompt(question: str, context: str = "") -> str:
    """Convert a question (and optional reference text) to a causal-LM prompt."""
    question = question.strip()
    context = context.strip()
    if not question:
        raise ValueError("سؤال نمی‌تواند خالی باشد.")
    if context:
        return f"متن مرجع: {context}\nسؤال: {question}\nپاسخ کوتاه و دقیق:"
    return f"سؤال: {question}\nپاسخ کوتاه و دقیق:"


def clean_answer(text: str) -> str:
    """Stop the generated answer before a new prompt section starts."""
    answer = text.strip()
    for marker in ("\nسؤال:", "\nمتن مرجع:", "\nپاسخ:"):
        answer = answer.split(marker, 1)[0].strip()
    return answer or "مدل پاسخی تولید نکرد. لطفاً سؤال را دقیق‌تر مطرح کنید."


@dataclass
class GPT2Answerer:
    model_name: str = DEFAULT_MODEL

    def __post_init__(self) -> None:
        try:
            import torch
            from transformers import AutoModelForCausalLM, AutoTokenizer
        except ImportError as exc:
            raise RuntimeError(
                "وابستگی‌ها نصب نیستند. دستور pip install -r requirements.txt را اجرا کنید."
            ) from exc

        self._torch = torch
        self._tokenizer = AutoTokenizer.from_pretrained(self.model_name)
        self._model = AutoModelForCausalLM.from_pretrained(self.model_name)
        self._device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self._model.to(self._device).eval()

        if self._tokenizer.pad_token_id is None:
            self._tokenizer.pad_token = self._tokenizer.eos_token

    def answer(
        self,
        question: str,
        context: str = "",
        max_new_tokens: int = 80,
        temperature: float = 0.7,
    ) -> str:
        prompt = build_prompt(question, context)
        encoded = self._tokenizer(
            prompt,
            return_tensors="pt",
            truncation=True,
            max_length=900,
        ).to(self._device)

        with self._torch.inference_mode():
            output = self._model.generate(
                **encoded,
                max_new_tokens=max_new_tokens,
                do_sample=True,
                temperature=temperature,
                top_p=0.9,
                top_k=50,
                repetition_penalty=1.15,
                no_repeat_ngram_size=3,
                pad_token_id=self._tokenizer.pad_token_id,
                eos_token_id=self._tokenizer.eos_token_id,
            )

        generated_tokens = output[0, encoded["input_ids"].shape[1] :]
        generated = self._tokenizer.decode(generated_tokens, skip_special_tokens=True)
        return clean_answer(generated)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="پرسش‌وپاسخ فارسی با GPT-2")
    parser.add_argument("--model", default=DEFAULT_MODEL, help="نام مدل در Hugging Face")
    parser.add_argument("--question", help="سؤال؛ در صورت حذف، برنامه تعاملی اجرا می‌شود")
    parser.add_argument("--context", default="", help="متن مرجع اختیاری")
    parser.add_argument("--max-new-tokens", type=int, default=80)
    parser.add_argument("--temperature", type=float, default=0.7)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    print(f"در حال بارگذاری مدل {args.model} ...")
    answerer = GPT2Answerer(args.model)

    if args.question:
        print(answerer.answer(args.question, args.context, args.max_new_tokens, args.temperature))
        return

    print("پرسش‌وپاسخ آماده است. برای خروج «خروج» را وارد کنید.")
    while True:
        question = input("\nسؤال: ").strip()
        if question.lower() in {"خروج", "exit", "quit"}:
            break
        if not question:
            continue
        context = input("متن مرجع (اختیاری): ").strip()
        print("پاسخ:", answerer.answer(question, context, args.max_new_tokens, args.temperature))


if __name__ == "__main__":
    main()
