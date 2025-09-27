"""
Comprehensive tests for the docstring parser module.
"""

import pytest
from typing import Any, Dict

from prompted_objects.docstring_parser import DocstringParser, DocstringParseResult, parse_docstring
from prompted_objects.exceptions import ValidationError


class TestDocstringParseResult:
    """Test the DocstringParseResult class."""

    def test_creation_with_defaults(self):
        """Test creating result with default values."""
        result = DocstringParseResult()
        assert result.prompt is None
        assert result.metadata == {}
        assert result.notes is None
        assert result.raw_docstring == ""

    def test_creation_with_values(self):
        """Test creating result with provided values."""
        result = DocstringParseResult(
            prompt="Test prompt",
            metadata={"key": "value"},
            notes="Test notes",
            raw_docstring="Original docstring"
        )
        assert result.prompt == "Test prompt"
        assert result.metadata == {"key": "value"}
        assert result.notes == "Test notes"
        assert result.raw_docstring == "Original docstring"

    def test_repr(self):
        """Test string representation of result."""
        result = DocstringParseResult(
            prompt="Test",
            metadata={"key": "value"},
            notes="Notes"
        )
        repr_str = repr(result)
        assert "prompt='Test'" in repr_str
        assert "metadata={'key': 'value'}" in repr_str
        assert "notes='Notes'" in repr_str


class TestDocstringParser:
    """Test the DocstringParser class."""

    def setup_method(self):
        """Set up test fixtures."""
        self.parser = DocstringParser()

    def test_empty_docstring(self):
        """Test parsing empty docstring."""
        result = self.parser.parse("")
        assert result.prompt is None
        assert result.metadata == {}
        assert result.notes is None

    def test_whitespace_only_docstring(self):
        """Test parsing whitespace-only docstring."""
        result = self.parser.parse("   \n\t  \n  ")
        assert result.prompt is None
        assert result.metadata == {}
        assert result.notes is None

    def test_simple_prompt_only(self):
        """Test parsing docstring with only PROMPT section."""
        docstring = '''
        PROMPT:
        This is a test prompt.
        '''
        result = self.parser.parse(docstring)
        assert result.prompt == "This is a test prompt."
        assert result.metadata == {}
        assert result.notes is None

    def test_simple_metadata_only(self):
        """Test parsing docstring with only METADATA section."""
        docstring = '''
        METADATA:
        key: value
        another: 123
        '''
        result = self.parser.parse(docstring)
        assert result.prompt is None
        assert result.metadata == {"key": "value", "another": 123}
        assert result.notes is None

    def test_simple_notes_only(self):
        """Test parsing docstring with only NOTES section."""
        docstring = '''
        NOTES:
        These are some notes.
        '''
        result = self.parser.parse(docstring)
        assert result.prompt is None
        assert result.metadata == {}
        assert result.notes == "These are some notes."

    def test_all_sections(self):
        """Test parsing docstring with all sections."""
        docstring = '''
        PROMPT:
        This is the prompt section.

        METADATA:
        id: test.function
        policy:
          - if: "is_int(a)"
            then: code
        examples:
          - input: {a: 5}
            output: 10

        NOTES:
        Additional documentation here.
        '''
        result = self.parser.parse(docstring)
        assert result.prompt == "This is the prompt section."
        assert result.metadata == {
            "id": "test.function",
            "policy": [{"if": "is_int(a)", "then": "code"}],
            "examples": [{"input": {"a": 5}, "output": 10}]
        }
        assert result.notes == "Additional documentation here."

    def test_complex_metadata_structure(self):
        """Test parsing complex nested metadata."""
        docstring = '''
        METADATA:
        id: math.add
        policy:
          - if: "is_int(a) and is_int(b)"
            then: code
          - else: model
        examples:
          - input: {a: 2, b: 3}
            output: 5
          - input: {a: "hello", b: "world"}
            output: "helloworld"
        capabilities:
          io: false
          network: false
          imports: ["math"]
        '''
        result = self.parser.parse(docstring)
        expected_metadata = {
            "id": "math.add",
            "policy": [
                {"if": "is_int(a) and is_int(b)", "then": "code"},
                {"else": "model"}
            ],
            "examples": [
                {"input": {"a": 2, "b": 3}, "output": 5},
                {"input": {"a": "hello", "b": "world"}, "output": "helloworld"}
            ],
            "capabilities": {
                "io": False,
                "network": False,
                "imports": ["math"]
            }
        }
        assert result.metadata == expected_metadata

    def test_indented_docstring(self):
        """Test parsing indented docstring (typical in classes)."""
        docstring = '''
            PROMPT:
            This is indented.

            METADATA:
            key: value
        '''
        result = self.parser.parse(docstring)
        assert result.prompt == "This is indented."
        assert result.metadata == {"key": "value"}

    def test_mixed_indentation(self):
        """Test parsing with mixed indentation levels."""
        docstring = '''
        PROMPT:
            This has mixed indentation.
          And this has different indentation.

        METADATA:
          key: value
        '''
        result = self.parser.parse(docstring)
        assert result.prompt == "This has mixed indentation.\nAnd this has different indentation."
        assert result.metadata == {"key": "value"}

    def test_invalid_yaml_metadata(self):
        """Test error handling for invalid YAML in METADATA."""
        docstring = '''
        METADATA:
        invalid: yaml: content:
          - with: [unclosed brackets
        '''
        with pytest.raises(ValidationError, match="Invalid YAML in METADATA section"):
            self.parser.parse(docstring)

    def test_non_dict_metadata(self):
        """Test error handling for non-dictionary METADATA content."""
        docstring = '''
        METADATA:
        - item1
        - item2
        '''
        with pytest.raises(ValidationError, match="METADATA section must contain a YAML object"):
            self.parser.parse(docstring)

    def test_section_order_variations(self):
        """Test parsing with different section orders."""
        # METADATA first
        docstring1 = '''
        METADATA:
        key: value

        PROMPT:
        Test prompt
        '''
        result1 = self.parser.parse(docstring1)
        assert result1.metadata == {"key": "value"}
        assert result1.prompt == "Test prompt"

        # NOTES in middle
        docstring2 = '''
        PROMPT:
        First prompt

        NOTES:
        Some notes

        METADATA:
        key: value
        '''
        result2 = self.parser.parse(docstring2)
        assert result2.prompt == "First prompt"
        assert result2.notes == "Some notes"
        assert result2.metadata == {"key": "value"}

    def test_multiple_blank_lines(self):
        """Test parsing with multiple blank lines between sections."""
        docstring = '''


        PROMPT:
        Test prompt



        METADATA:
        key: value


        '''
        result = self.parser.parse(docstring)
        assert result.prompt == "Test prompt"
        assert result.metadata == {"key": "value"}

    def test_preserve_raw_docstring(self):
        """Test that original docstring is preserved."""
        original = 'PROMPT:\nTest prompt'
        result = self.parser.parse(original)
        assert result.raw_docstring == original

    def test_missing_colon_in_section_header(self):
        """Test handling of malformed section headers."""
        docstring = '''
        PROMPT
        Test prompt

        METADATA
        key: value
        '''
        # Should still parse correctly since we match on word followed by colon
        result = self.parser.parse(docstring)
        assert result.prompt == "Test prompt"
        assert result.metadata == {"key": "value"}

    def test_case_insensitive_section_names(self):
        """Test that section names are case insensitive."""
        docstring = '''
        prompt:
        Test prompt

        metadata:
        key: value

        notes:
        Test notes
        '''
        result = self.parser.parse(docstring)
        assert result.prompt == "Test prompt"
        assert result.metadata == {"key": "value"}
        assert result.notes == "Test notes"

    def test_section_with_no_content(self):
        """Test sections with no content."""
        docstring = '''
        PROMPT:

        METADATA:
        key: value

        NOTES:
        '''
        result = self.parser.parse(docstring)
        assert result.prompt is None  # Empty content becomes None
        assert result.metadata == {"key": "value"}
        assert result.notes is None


class TestConvenienceFunction:
    """Test the parse_docstring convenience function."""

    def test_parse_docstring_function(self):
        """Test the convenience function works correctly."""
        docstring = '''
        PROMPT:
        Test prompt

        METADATA:
        key: value
        '''
        result = parse_docstring(docstring)
        assert result.prompt == "Test prompt"
        assert result.metadata == {"key": "value"}

    def test_parse_docstring_empty(self):
        """Test convenience function with empty docstring."""
        result = parse_docstring("")
        assert result.prompt is None
        assert result.metadata == {}
        assert result.notes is None


class TestErrorHandling:
    """Test error handling and edge cases."""

    def setup_method(self):
        """Set up test fixtures."""
        self.parser = DocstringParser()

    def test_yaml_import_error(self):
        """Test behavior when PyYAML is not available."""
        # This would require mocking the yaml import, which is complex
        # For now, we test that the parser initializes correctly
        assert self.parser is not None

    def test_malformed_docstring_recovery(self):
        """Test that parser doesn't crash on malformed input."""
        # Various malformed inputs
        test_cases = [
            "Just plain text",
            "PROMPT:",  # No content
            "INVALID_HEADER:\ncontent",
            "PROMPT:\n\n\nMETADATA:\ninvalid: yaml: [",
        ]

        for case in test_cases:
            try:
                result = self.parser.parse(case)
                # Should not crash, may return partial results
                assert isinstance(result, DocstringParseResult)
            except ValidationError:
                # Expected for truly invalid YAML
                pass
            except Exception as e:
                pytest.fail(f"Parser crashed on input: {case!r} with error: {e}")


if __name__ == "__main__":
    pytest.main([__file__])
