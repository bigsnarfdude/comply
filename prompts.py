# prompts.py

STATEMENT_EXTRACTION_TEMPLATE = '''
Extract regulatory and procedural statements from this aviation operations manual text.
For each section, identify specific requirements that:

- Define mandatory procedures or actions
- Establish record-keeping requirements
- Specify document control processes
- Define responsibilities or duties
- Set operational standards
- Establish safety procedures
- Define compliance requirements

Return each requirement as a complete, self-contained statement.
Include only statements that contain specific requirements, procedures, or standards.
Skip purely descriptive text or background information.

Text to analyze:
"{text}"

Respond with ONLY a JSON array of statements. Format:
[
  "Complete requirement statement 1",
  "Complete requirement statement 2"
]

Important: Return only the JSON array with no additional text, code blocks, or formatting.
'''

MATCHING_TEMPLATE = '''
Analyze this aviation operations manual statement for regulatory requirements:
"{statement}"

1. Identify the key regulatory aspects:
- Personnel requirements or qualifications
- Operational procedures or limitations
- Documentation or record-keeping requirements
- Safety requirements
- Equipment or maintenance requirements

2. Using the provided regulations document, find the 2-3 most relevant 
Canadian Aviation Regulations sections that:
- Directly mandate these requirements
- Establish these standards or procedures
- Define these specific compliance criteria

Return ONLY a JSON array of section numbers, like:
["401.03", "605.34"]

If no direct regulatory requirements exist, return: []
'''

REGULATIONS_SYSTEM_INSTRUCTION = """You are an expert in Canadian Aviation Regulations.
Using the provided regulations text, identify specific CARs sections 
that directly mandate requirements matching each input statement.
Focus on exact regulatory matches and return section numbers as strings."""

def create_statement_extraction_prompt(text: str) -> str:
    return STATEMENT_EXTRACTION_TEMPLATE.format(text=text)

def create_matching_prompt(statement: str) -> str:
    return MATCHING_TEMPLATE.format(statement=statement)