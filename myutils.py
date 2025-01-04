# utils.py
import json
import re
from typing import List, Dict, Tuple
from pathlib import Path

def load_valid_sections(filepath: str) -> Dict[str, str]:
    """
    Load and validate the titles.json file.
    """
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            titles_data = json.load(f)
            return titles_data
    except Exception as e:
        print(f"Error loading titles from {filepath}: {e}")
        return {}

def validate_section_number(section: str, valid_sections: Dict[str, str]) -> bool:
    """
    Validate section number format and existence.
    """
    if not re.match(r'^\d{3}\.\d{2}(\.\d)?$', section):
        return False
    return section in valid_sections

def chunk_text(text: str, chunk_size: int = 1000) -> List[str]:
    """
    Split text into chunks, preserving paragraph boundaries.
    """
    paragraphs = text.split('\n\n')
    chunks = []
    current_chunk = []
    current_length = 0

    for para in paragraphs:
        para_length = len(para)
        if current_length + para_length > chunk_size and current_chunk:
            chunks.append('\n\n'.join(current_chunk))
            current_chunk = [para]
            current_length = para_length
        else:
            current_chunk.append(para)
            current_length += para_length

    if current_chunk:
        chunks.append('\n\n'.join(current_chunk))

    return chunks

def clean_response_text(text: str) -> str:
    """Clean and normalize AI response text."""
    cleaned_text = text.strip()
    if cleaned_text.startswith('```json'):
        cleaned_text = cleaned_text[7:]
    if cleaned_text.endswith('```'):
        cleaned_text = cleaned_text[:-3]
    return cleaned_text

def parse_statements(text: str) -> List[str]:
    """Parse statements from cleaned response text."""
    try:
        parsed = json.loads(text)
        if isinstance(parsed, list):
            return [str(s) for s in parsed if s and len(str(s).split()) >= 3]
    except json.JSONDecodeError:
        matches = re.findall(r'"([^"]*)"', text)
        if matches:
            return [s for s in matches if s and len(s.split()) >= 3]
        try:
            fixed_text = text.replace('",\n  "', '", "')
            fixed_text = re.sub(r',\s*]', ']', fixed_text)
            parsed = json.loads(fixed_text)
            if isinstance(parsed, list):
                return [str(s) for s in parsed if s and len(str(s).split()) >= 3]
        except:
            pass
    return []

def deduplicate_statements(statements: List[str]) -> List[str]:
    """Remove duplicate statements while preserving order."""
    seen = set()
    deduped = []
    for stmt in statements:
        normalized = ' '.join(stmt.split())
        if normalized and normalized not in seen:
            seen.add(normalized)
            deduped.append(stmt)
    return deduped

def parse_section_numbers(text: str) -> List[str]:
    """Parse and validate section numbers from response text."""
    try:
        sections = json.loads(text)
        if isinstance(sections, list):
            return [str(s) for s in sections]
    except json.JSONDecodeError:
        matches = re.search(r'\[(.*?)\]', text)
        if matches:
            try:
                sections = json.loads(f"[{matches.group(1)}]")
                return [str(s) for s in sections]
            except:
                pass
    return []

def read_file_content(filepath: str) -> str:
    """Reads the content of a file with UTF-8 encoding."""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return f.read()
    except Exception as e:
        print(f"Error reading file {filepath}: {e}")
        return ""

def save_results(results: Dict[str, List[Tuple[str, str]]], output_path: str):
    """Saves the matching results to a text file."""
    with open(output_path, "w", encoding="utf-8") as f:
        for statement, matches in results.items():
            f.write("Statement:\n")
            f.write(statement + "\n\n")
            f.write("Relevant Sections:\n")
            for section, title in matches:
                f.write(f"- {section}: {title}\n")
            f.write("-" * 80 + "\n\n")
    print(f"\nResults saved to {output_path}")