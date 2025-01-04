import google.generativeai as genai
from google.generativeai import caching
from typing import List, Dict, Tuple, Optional

import myutils as utils
import prompts
import models

class EnhancedManualRegulationMatcher:
    def __init__(self, api_key: str, 
                 extraction_model: str = "gemini-1.5-flash-001",
                 matching_model: str = "gemini-1.5-flash-001", 
                 titles_filepath: str = "titles.json"):
        """
        Initialize the matcher with API credentials and load valid sections.

        Args:
            api_key (str): The Google AI API key
            extraction_model (str): Model to use for statement extraction. Defaults to "gemini-1.5-flash-001".
            matching_model (str): Model to use for regulation matching. Defaults to "gemini-1.5-flash-001".
            titles_filepath (str): Path to the titles JSON file
        """
        self.api_key = api_key
        self.extraction_model = extraction_model
        self.matching_model = matching_model
        self.valid_sections = utils.load_valid_sections(titles_filepath)
        genai.configure(api_key=api_key)

    def process_manual(self, manual_path: str, regs_path: str) -> Dict[str, List[Tuple[str, str]]]:
        """
        Process entire manual and match statements to regulations with titles.
        """
        regs_cache = None
        try:
            # Read manual
            manual_text = utils.read_file_content(manual_path)

            # Extract statements using the extraction model
            base_model = models.get_model(self.extraction_model)
            print(f"Extracting statements using {self.extraction_model}...")
            statements = self.extract_statements(manual_text, base_model)
            print(f"Extracted {len(statements)} statements")

            if not statements:
                print("No statements were extracted. Check the extraction process.")
                return {}

            # Set up model with regulations
            regs_document = genai.upload_file(path=regs_path)
            print("Uploaded regulations document")

            regs_cache = caching.CachedContent.create(
                model=self.matching_model,
                system_instruction=prompts.REGULATIONS_SYSTEM_INSTRUCTION,
                contents=[regs_document]
            )

            # Create the matching model using cached content
            matching_model = genai.GenerativeModel.from_cached_content(regs_cache)

            # Process statements
            results = {}
            for i, statement in enumerate(statements, 1):
                print(f"\nProcessing statement {i}/{len(statements)}")
                print(f"Statement: {statement[:200]}...")

                matches = self.match_statement_to_regs(statement, matching_model)
                if matches:
                    results[statement] = matches
                    print("Matched sections:")
                    for section, title in matches:
                        print(f"- {section}: {title}")

            return results

        except Exception as e:
            print(f"Error processing manual: {e}")
            return {}

        finally:
            if regs_cache:
                try:
                    regs_cache.delete()
                except Exception as e:
                    print(f"Error deleting cache: {e}")

    def extract_statements(self, text: str, model: genai.GenerativeModel) -> List[str]:
        """
        Extract meaningful statements using Gemini, processing in chunks if needed.

        Args:
            text (str): Text to process
            model: Gemini model instance

        Returns:
            List[str]: List of extracted statements
        """
        try:
            chunks = utils.chunk_text(text)
            all_statements = []

            print(f"Processing {len(chunks)} text chunks...")

            for i, chunk in enumerate(chunks, 1):
                print(f"Processing chunk {i}/{len(chunks)}...")
                prompt = prompts.create_statement_extraction_prompt(chunk)

                try:
                    response = model.generate_content(prompt)
                    if not response.text:
                        continue

                    cleaned_text = utils.clean_response_text(response.text)
                    chunk_statements = utils.parse_statements(cleaned_text)
                    all_statements.extend(chunk_statements)

                except Exception as e:
                    print(f"Error processing chunk {i}: {str(e)}")
                    continue

            return utils.deduplicate_statements(all_statements)

        except Exception as e:
            print(f"Error in extract_statements: {e}")
            return []

    def match_statement_to_regs(self, statement: str, model: genai.GenerativeModel, max_retries: int = 3) -> List[Tuple[str, str]]:
        """
        Match a single statement to relevant regulation sections with titles.

        Args:
            statement (str): Statement to match
            model: Gemini model instance
            max_retries (int): Number of retry attempts

        Returns:
            List[Tuple[str, str]]: List of tuples containing (section_number, title)
        """
        for attempt in range(max_retries):
            try:
                prompt = prompts.create_matching_prompt(statement)
                response = model.generate_content(prompt)
                
                if not response.text:
                    continue
                
                sections = utils.parse_section_numbers(response.text)
                if sections:
                    return [(section, self.valid_sections[section])
                            for section in sections
                            if utils.validate_section_number(section, self.valid_sections)]
                
            except Exception as e:
                print(f"Attempt {attempt + 1} failed: {str(e)}")
                if attempt == max_retries - 1:
                    print(f"Failed to process statement: {statement[:100]}...")
                    return []

        return []
