# Persian GPT-2 Question Answering | پرسش‌وپاسخ فارسی با GPT‑2

[English](#english) | [فارسی](#فارسی)

## English

A compact command-line question-answering demo powered by a pretrained Persian GPT-2
model. It accepts a question and an optional reference passage, turns them into a structured
prompt, and generates a short answer with configurable decoding parameters.

### Features

- Interactive and single-question command-line modes
- Optional reference context for more relevant answers
- Persian GPT-2 model by default (`HooshvareLab/gpt2-fa`)
- Configurable model, output length, and temperature
- Unit tests for prompt construction and output cleanup

### Installation

Python 3.10 or newer is recommended.

```bash
python -m venv .venv
# Windows
.venv\Scripts\activate
python -m pip install -r requirements.txt
```

The model weights are downloaded from Hugging Face on the first run. An internet connection
and several gigabytes of free disk space may be required.

### Usage

Interactive mode:

```bash
python app.py
```

Ask one question with reference context:

```bash
python app.py --question "پایتخت ایران کجاست؟" --context "تهران پایتخت ایران است."
```

Use the original English GPT-2 model:

```bash
python app.py --model gpt2 --question "What is artificial intelligence?"
```

Run the tests:

```bash
python -m unittest -v
```

### How it works

1. `AutoTokenizer` and `AutoModelForCausalLM` load the pretrained model.
2. The question and optional context are formatted as a causal-language-model prompt.
3. The model generates up to 80 new tokens using Top-k and Top-p sampling.
4. The generated continuation is separated from the prompt and cleaned before display.

### Limitations

GPT-2 is a text-generation model rather than a specialized question-answering model. Its
answers can be incomplete or factually incorrect. Reference context generally improves
relevance but does not guarantee accuracy. A production system should use task-specific
fine-tuning, retrieval, and systematic evaluation.

The detailed Persian exercise report and test results are available in [REPORT.md](REPORT.md).

---

## فارسی

این پروژه یک سامانه ساده پرسش‌وپاسخ خط فرمان با مدل زبانی ازپیش‌آموزش‌دیده فارسی مبتنی
بر GPT‑2 است. برنامه سؤال و متن مرجع اختیاری را دریافت می‌کند، آن‌ها را به پرامپت ساختاریافته
تبدیل می‌کند و یک پاسخ کوتاه تولید می‌کند.

### امکانات

- حالت تعاملی و اجرای تک‌سؤال
- دریافت متن مرجع اختیاری برای پاسخ مرتبط‌تر
- استفاده پیش‌فرض از مدل فارسی `HooshvareLab/gpt2-fa`
- امکان تنظیم مدل، طول پاسخ و دما
- آزمون خودکار ساخت پرامپت و پاک‌سازی خروجی

### نصب

استفاده از Python 3.10 یا جدیدتر پیشنهاد می‌شود.

```bash
python -m venv .venv
# Windows
.venv\Scripts\activate
python -m pip install -r requirements.txt
```

در نخستین اجرا، وزن‌های مدل از Hugging Face دانلود می‌شوند؛ بنابراین اینترنت و چند
گیگابایت فضای آزاد ممکن است لازم باشد.

### اجرا

حالت تعاملی:

```bash
python app.py
```

اجرای یک سؤال همراه متن مرجع:

```bash
python app.py --question "پایتخت ایران کجاست؟" --context "تهران پایتخت ایران است."
```

استفاده از GPT‑2 اصلی برای پرسش انگلیسی:

```bash
python app.py --model gpt2 --question "What is artificial intelligence?"
```

اجرای آزمون‌ها:

```bash
python -m unittest -v
```

### روش کار

1. مدل و توکنایزر با `AutoTokenizer` و `AutoModelForCausalLM` بارگذاری می‌شوند.
2. سؤال و متن مرجع در قالب یک پرامپت مشخص قرار می‌گیرند.
3. مدل با نمونه‌گیری Top-k و Top-p حداکثر ۸۰ توکن جدید تولید می‌کند.
4. ادامه تولیدشده از پرامپت جدا و پیش از نمایش پاک‌سازی می‌شود.

### محدودیت

GPT‑2 مدل تولید متن است و مدل تخصصی پرسش‌وپاسخ محسوب نمی‌شود؛ بنابراین احتمال تولید پاسخ
ناقص یا نادرست وجود دارد. افزودن متن مرجع معمولاً ارتباط پاسخ را بهتر می‌کند، اما صحت آن را
تضمین نمی‌کند. برای استفاده واقعی، تنظیم دقیق، بازیابی اطلاعات و ارزیابی نظام‌مند لازم است.

گزارش کامل فارسی تمرین و نتایج آزمون‌ها در [REPORT.md](REPORT.md) قرار دارد.
