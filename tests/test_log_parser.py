import unittest

from tools.log_parser import parse_upload, summarize_events


class LogParserTests(unittest.TestCase):
    def test_csv_parsing(self):
        frame = parse_upload(b"time,event\n10:00,login\n", "events.csv")
        self.assertEqual(len(frame), 1)
        self.assertEqual(frame.iloc[0]["event"], "login")

    def test_json_events_list(self):
        frame = parse_upload(b'{"events":[{"type":"login"},{"type":"logout"}]}', "events.json")
        self.assertEqual(len(frame), 2)

    def test_text_parsing(self):
        frame = parse_upload(b"line one\n\nline two\n", "events.txt")
        self.assertEqual(len(frame), 2)

    def test_unsupported_extension(self):
        with self.assertRaises(ValueError):
            parse_upload(b"x", "events.exe")

    def test_summary_is_bounded(self):
        frame = parse_upload(b"event\na\nb\nc\n", "events.csv")
        summary = summarize_events(frame, max_rows=2)
        self.assertIn("Total rows in file: 3", summary)
        self.assertIn("up to 2 rows", summary)


if __name__ == "__main__":
    unittest.main()
