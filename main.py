import os
from pathlib import Path
import argparse
from typing import Optional

from matcher import EnhancedManualRegulationMatcher
from myutils import save_results

def get_api_key() -> Optional[str]:
    """Get API key from environment variable."""
    api_key = os.getenv('GOOGLE_API_KEY')
    if not api_key:
        print("Error: GOOGLE_API_KEY environment variable not set")
        print("Please set your Google API key with:")
        print("export GOOGLE_API_KEY='your-api-key-here'")
        return None
    return api_key

def validate_files(paths: list[str]) -> bool:
    """Validate that all required files exist."""
    missing_files = []
    for path in paths:
        if not Path(path).exists():
            missing_files.append(path)
    
    if missing_files:
        print("Error: The following required files are missing:")
        for file in missing_files:
            print(f"- {file}")
        return False
    return True

def parse_arguments():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description='Process aviation manual against regulations.')
    parser.add_argument('--manual', default='manual.txt',
                      help='Path to the manual file (default: manual.txt)')
    parser.add_argument('--regs', default='parts47.txt',
                      help='Path to the regulations file (default: parts47.txt)')
    parser.add_argument('--titles', default='titles.json',
                      help='Path to the titles JSON file (default: titles.json)')
    parser.add_argument('--output', default='matching_results.txt',
                      help='Path for output file (default: matching_results.txt)')
    parser.add_argument('--extraction-model', default='gemini-1.5-flash',
                      help='Model for statement extraction (default: gemini-1.5-flash)')
    parser.add_argument('--matching-model', default='gemini-1.5-flash',
                      help='Model for regulation matching (default: gemini-1.5-flash)')
    return parser.parse_args()

def main():
    args = parse_arguments()
    api_key = get_api_key()
    if not api_key:
        return

    required_files = [args.manual, args.regs, args.titles]
    if not validate_files(required_files):
        return

    try:
        # Initialize matcher with both models
        matcher = EnhancedManualRegulationMatcher(
            api_key=api_key,
            extraction_model=args.extraction_model,
            matching_model=args.matching_model,
            titles_filepath=args.titles
        )

        print(f"\nProcessing manual '{args.manual}' with regulations from '{args.regs}'...")
        print(f"Using {args.extraction_model} for statement extraction")
        print(f"Using {args.matching_model} for regulation matching")
        
        # Process manual
        results = matcher.process_manual(args.manual, args.regs)
        
        if not results:
            print("\nNo matches found. Please check your input files and try again.")
            return

        # Output results to console
        print("\nMatching Results:")
        print("=" * 80)
        for statement, matches in results.items():
            print(f"\nStatement:")
            print(statement[:200] + "..." if len(statement) > 200 else statement)
            print("\nRelevant Sections:")
            for section, title in matches:
                print(f"- {section}: {title}")
            print("-" * 80)

        # Save results to file
        save_results(results, args.output)
        print(f"\nResults have been saved to: {args.output}")

    except Exception as e:
        print(f"\nAn error occurred while processing: {str(e)}")
        print("Please check your input files and API key, then try again.")

if __name__ == "__main__":
    main()