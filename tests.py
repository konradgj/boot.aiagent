import unittest
from functions.get_files_info import get_files_info


class FilesTest(unittest.TestCase):
    def test_dot(self):
        info = get_files_info("calculator", ".")
        print(info)
        self.assertEqual(
            info,
            """- main.py: file_size=576 bytes, is_dir=False
- tests.py: file_size=1343 bytes, is_dir=False
- pkg: file_size=66 bytes, is_dir=True""",
        )

    def test_dir(self):
        info = get_files_info("calculator", "pkg")
        print(info)
        self.assertEqual(
            info,
            """- calculator.py: file_size=1739 bytes, is_dir=False
- render.py: file_size=768 bytes, is_dir=False
- __pycache__: file_size=96 bytes, is_dir=True""",
        )

    def test_slash(self):
        info = get_files_info("calculator", "/bin")
        print(info)
        self.assertEqual(
            info,
            """Error: Cannot list '/bin' as it is outside the permitted working directory""",
        )

    def test_dotdot(self):
        info = get_files_info("calculator", "../")
        print(info)
        self.assertEqual(
            info,
            """Error: Cannot list '../' as it is outside the permitted working directory""",
        )

    def test_word(self):
        info = get_files_info("calculator", "main.py")
        self.assertEqual(
            info,
            """Error: 'main.py' is not a directory""",
        )


if __name__ == "__main__":
    unittest.main()
