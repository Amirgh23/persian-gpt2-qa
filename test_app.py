import unittest

from app import build_prompt, clean_answer


class PromptTests(unittest.TestCase):
    def test_prompt_with_context(self):
        prompt = build_prompt("پایتخت ایران کجاست؟", "تهران پایتخت ایران است.")
        self.assertIn("متن مرجع: تهران پایتخت ایران است.", prompt)
        self.assertTrue(prompt.endswith("پاسخ کوتاه و دقیق:"))

    def test_empty_question_is_rejected(self):
        with self.assertRaises(ValueError):
            build_prompt("   ")

    def test_clean_answer_stops_at_next_question(self):
        self.assertEqual(clean_answer("تهران است.\nسؤال: بعدی"), "تهران است.")


if __name__ == "__main__":
    unittest.main()
