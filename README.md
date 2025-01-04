# comply

This tool analyzes canadian aviation operations manuals and automatically matches their content with relevant sections of the Canadian Aviation Regulations (CARs). It uses Google's Gemini Caching AI models to extract meaningful statements from manuals and identify corresponding regulatory requirements.

## Features

- Extracts regulatory and procedural statements from aviation operations manuals
- Matches statements to relevant CARs sections
- Supports processing large documents by chunking
- Handles both statement extraction and regulation matching with separate models
- Provides detailed output with matched regulations and their titles
- Includes retry logic for improved reliability

## Prerequisites

- Python 3.8 or higher
- Google API key with access to Gemini models
- Required input files:
  - Aviation operations manual (text format)
  - Regulations file (text format)
  - JSON file mapping regulation section numbers to titles

## Installation

1. Clone the repository:
```bash
git clone [repository-url]
cd [repository-name]
```

2. Install required packages:
```bash
pip install google-generativeai
```

3. Set up your Google API key:
```bash
export GOOGLE_API_KEY='your-api-key-here'
```

## File Structure

- `main.py` - Main script to run the tool
- `matcher.py` - Core matching logic implementation
- `models.py` - Model configuration and setup
- `myutils.py` - Utility functions for file handling and text processing
- `prompts.py` - AI model prompts and templates

## Usage

Basic usage with default settings:
```bash
python main.py
```

Customize the execution with command-line arguments:
```bash
python main.py \
  --manual path/to/manual.txt \
  --regs path/to/regulations.txt \
  --titles path/to/titles.json \
  --output results.txt \
  --extraction-model gemini-1.5-flash-001 \
  --matching-model gemini-1.5-flash-001
```

### Command Line Arguments

- `--manual`: Path to the manual file (default: manual.txt)
- `--regs`: Path to the regulations file (default: parts47.txt)
- `--titles`: Path to the titles JSON file (default: titles.json)
- `--output`: Path for output file (default: matching_results.txt)
- `--extraction-model`: Model for statement extraction (default: gemini-1.5-flash)
- `--matching-model`: Model for regulation matching (default: gemini-1.5-flash)

## Input File Requirements

### Manual File
- Text file containing the aviation operations manual content
- Should be in plain text format
- No specific formatting requirements

### Regulations File
- Text file containing the Canadian Aviation Regulations
- Should be in plain text format
- Sections should be clearly numbered

### Titles JSON File
Format:
```json
{
  "401.03": "Title of regulation section",
  "605.34": "Another regulation section title"
}
```

## Output Format

The tool generates both console output and a text file containing the results. Each match includes:
- The extracted statement from the manual
- List of relevant regulation sections with their titles

Example output:
```
Statement:
The pilot must maintain a valid license at all times when operating the aircraft.

Relevant Sections:
- 401.03: Requirements for Pilot License
- 401.05: License Validity Period
```

## Error Handling

The tool includes comprehensive error handling for:
- Missing input files
- API authentication issues
- File reading/parsing errors
- Model execution failures
- Invalid regulation section numbers

## Development

### Adding New Features
1. Modify the core matching logic in `matcher.py`
2. Update prompts in `prompts.py` for new extraction patterns
3. Add new utility functions in `myutils.py` as needed

### Testing
Test with different:
- Manual formats and content
- Regulation sections
- Model parameters
- Input file sizes

## Troubleshooting

Common issues and solutions:

1. API Key Issues
   - Ensure GOOGLE_API_KEY is properly set
   - Verify API key has correct permissions

2. File Not Found
   - Check file paths
   - Verify file permissions

3. Model Errors
   - Confirm model names are correct
   - Check API quotas and limits

4. Processing Errors
   - Try reducing chunk size
   - Check input file encoding

## License

This project is licensed under the License - see the LICENSE file for details.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
