import unittest
from pathlib import Path
import tempfile
import shutil
import sys
from unittest.mock import patch, MagicMock

# Import the script functions
# We need to add the parent directory to the path to import extract_fiasse_sections
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))
import extract_fiasse_sections


class TestExtractFiasseSections(unittest.TestCase):
    def setUp(self):
        # Create a temporary directory for tests
        self.test_dir = Path(tempfile.mkdtemp())

    def tearDown(self):
        # Remove the temporary directory after tests
        shutil.rmtree(self.test_dir)

    def test_extract_section_id(self):
        self.assertEqual(extract_fiasse_sections.extract_section_id("## 1. Introduction"), "1")
        self.assertEqual(extract_fiasse_sections.extract_section_id("### 2.3. Principles"), "2.3")
        self.assertEqual(extract_fiasse_sections.extract_section_id("#### 6.4.1.2. Title"), "6.4.1.2")
        self.assertIsNone(extract_fiasse_sections.extract_section_id("## Abstract"))
        self.assertIsNone(extract_fiasse_sections.extract_section_id("### A.1. Maintainability"))

    def test_normalize_section_id(self):
        self.assertEqual(extract_fiasse_sections.normalize_section_id("1"), "1")
        self.assertEqual(extract_fiasse_sections.normalize_section_id("1.2"), "1.2")
        self.assertEqual(extract_fiasse_sections.normalize_section_id("1.2.3"), "1.2.3")
        self.assertEqual(extract_fiasse_sections.normalize_section_id("1.2.3.4"), "1.2.3")

    def test_format_section_id_for_filename(self):
        self.assertEqual(extract_fiasse_sections.format_section_id_for_filename("1"), "1.0.0")
        self.assertEqual(extract_fiasse_sections.format_section_id_for_filename("1.2"), "1.2.0")
        self.assertEqual(extract_fiasse_sections.format_section_id_for_filename("1.2.3"), "1.2.3")
        self.assertEqual(extract_fiasse_sections.format_section_id_for_filename("1.2.3.4"), "1.2.3")

    def test_parse_section_id_from_filename(self):
        self.assertEqual(extract_fiasse_sections.parse_section_id_from_filename("S1.0.0.md"), "1.0.0")
        self.assertEqual(extract_fiasse_sections.parse_section_id_from_filename("S1.2.0.md"), "1.2.0")
        self.assertEqual(extract_fiasse_sections.parse_section_id_from_filename("S10.2.3.md"), "10.2.3")
        self.assertIsNone(extract_fiasse_sections.parse_section_id_from_filename("code-index.md"))
        self.assertIsNone(extract_fiasse_sections.parse_section_id_from_filename("S1.0.0.0.md"))

    def test_section_sorting(self):
        filenames = ["S10.0.0.md", "S1.1.0.md", "S2.0.0.md", "S1.0.0.md"]
        sorted_filenames = sorted(filenames, key=extract_fiasse_sections.natural_sort_key)
        self.assertEqual(sorted_filenames, ["S1.0.0.md", "S1.1.0.md", "S2.0.0.md", "S10.0.0.md"])

    def test_split_into_sections(self):
        content = """# Title
## Abstract
This is abstract.

## 1. Section One
Content of section one.

### 1.1. Sub Section One
Content of sub section one.

#### 1.1.1. Deep Section
Content of deep section.

#### 1.1.1.1. Too Deep Section
Content of too deep section.

## 2. Section Two
Content of section two.
"""
        sections = extract_fiasse_sections.split_into_sections(content)
        self.assertIn("0.0.0", sections)
        self.assertIn("1", sections)
        self.assertIn("1.1", sections)
        self.assertIn("1.1.1", sections)
        self.assertIn("2", sections)

        self.assertTrue(sections["0.0.0"].startswith("# Title"))
        self.assertTrue(sections["1"].startswith("## 1. Section One"))
        self.assertTrue(sections["1.1"].startswith("### 1.1. Sub Section One"))
        
        # 1.1.1.1 should be grouped under 1.1.1 because depth limit is 3 parts
        self.assertIn("#### 1.1.1.1. Too Deep Section", sections["1.1.1"])

    def test_extract_sections_success(self):
        input_file = self.test_dir / "framework.md"
        output_dir = self.test_dir / "framework_extracted"
        
        input_file.write_text("""## 1. Intro
Intro text.
## 2. Setup
Setup text.
""", encoding="utf-8")
        
        success = extract_fiasse_sections.extract_sections(input_file, output_dir)
        self.assertTrue(success)
        self.assertTrue((output_dir / "S1.0.0.md").exists())
        self.assertTrue((output_dir / "S2.0.0.md").exists())
        self.assertEqual((output_dir / "S1.0.0.md").read_text(encoding="utf-8").strip(), "## 1. Intro\nIntro text.")

    def test_extract_sections_failure_non_existent(self):
        input_file = self.test_dir / "non_existent.md"
        output_dir = self.test_dir / "framework_extracted"
        
        success = extract_fiasse_sections.extract_sections(input_file, output_dir)
        self.assertFalse(success)

    def test_combine_sections_success(self):
        input_dir = self.test_dir / "framework_parts"
        output_file = self.test_dir / "framework_combined.md"
        
        input_dir.mkdir()
        (input_dir / "S1.0.0.md").write_text("## 1. Intro\nIntro text.", encoding="utf-8")
        (input_dir / "S2.0.0.md").write_text("## 2. Setup\nSetup text.", encoding="utf-8")
        (input_dir / "ignored.md").write_text("Ignored", encoding="utf-8")
        
        success = extract_fiasse_sections.combine_sections(input_dir, output_file)
        self.assertTrue(success)
        
        combined_content = output_file.read_text(encoding="utf-8")
        self.assertIn("## 1. Intro", combined_content)
        self.assertIn("## 2. Setup", combined_content)
        self.assertNotIn("Ignored", combined_content)
        # Verify order
        self.assertTrue(combined_content.index("## 1. Intro") < combined_content.index("## 2. Setup"))

    def test_combine_sections_failure_empty(self):
        input_dir = self.test_dir / "empty_dir"
        output_file = self.test_dir / "framework_combined.md"
        input_dir.mkdir()
        
        success = extract_fiasse_sections.combine_sections(input_dir, output_file)
        self.assertFalse(success)

    def test_update_llms_docs_success(self):
        sections_dir = self.test_dir / "sections"
        sections_dir.mkdir()
        (sections_dir / "S1.0.0.md").write_text("## 1. Intro\nContent", encoding="utf-8")
        
        llms_file = sections_dir / "llms.txt"
        llms_file.write_text("""# LLMS
## Docs
- [Old Intro](./S1.0.0.md): Old Description
- [Removed](./S3.0.0.md): Description
## Optional
Other content
""", encoding="utf-8")
        
        success = extract_fiasse_sections.update_llms_docs(llms_file, sections_dir)
        self.assertTrue(success)
        
        llms_content = llms_file.read_text(encoding="utf-8")
        self.assertIn("- [Old Intro](./S1.0.0.md): Old Description", llms_content)
        self.assertNotIn("Removed", llms_content)
        self.assertIn("## Optional", llms_content)

    def test_update_llms_docs_add_new_file(self):
        sections_dir = self.test_dir / "sections"
        sections_dir.mkdir()
        (sections_dir / "S1.0.0.md").write_text("## 1. Intro\nContent", encoding="utf-8")
        (sections_dir / "S2.0.0.md").write_text("## 2. Design\nContent", encoding="utf-8")
        
        llms_file = sections_dir / "llms.txt"
        llms_file.write_text("""# LLMS
## Docs
- [Old Intro](./S1.0.0.md): Old Description
## Optional
Other content
""", encoding="utf-8")
        
        success = extract_fiasse_sections.update_llms_docs(llms_file, sections_dir)
        self.assertTrue(success)
        
        llms_content = llms_file.read_text(encoding="utf-8")
        self.assertIn("- [Old Intro](./S1.0.0.md): Old Description", llms_content)
        self.assertIn("- [2. Design](./S2.0.0.md): TBD", llms_content)

    def test_update_llms_docs_no_llms_txt(self):
        sections_dir = self.test_dir / "sections"
        sections_dir.mkdir()
        llms_file = sections_dir / "llms.txt"
        # Should return True (noop success) when llms.txt doesn't exist
        success = extract_fiasse_sections.update_llms_docs(llms_file, sections_dir)
        self.assertTrue(success)

    def test_main_extract_success(self):
        input_file = self.test_dir / "framework.md"
        output_dir = self.test_dir / "framework_extracted"
        
        input_file.write_text("## 1. Intro\nIntro text.", encoding="utf-8")
        
        test_args = ["extract_fiasse_sections.py", str(input_file), str(output_dir)]
        with patch.object(sys, 'argv', test_args):
            exit_code = extract_fiasse_sections.main()
            self.assertEqual(exit_code, 0)
            self.assertTrue((output_dir / "S1.0.0.md").exists())

    def test_main_extract_failure(self):
        input_file = self.test_dir / "non_existent.md"
        output_dir = self.test_dir / "framework_extracted"
        
        test_args = ["extract_fiasse_sections.py", str(input_file), str(output_dir)]
        with patch.object(sys, 'argv', test_args):
            exit_code = extract_fiasse_sections.main()
            self.assertEqual(exit_code, 1)


if __name__ == "__main__":
    unittest.main()
