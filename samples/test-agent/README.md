# Resume Fixer Agent

An AI-powered resume analysis and improvement agent specifically designed for software engineering professionals.

## Description

This agent uses AI and web research to analyze resumes against current industry best practices, identify strengths and weaknesses, and provide specific, actionable improvements. It's perfect for software engineers looking to optimize their resumes for both human recruiters and ATS (Applicant Tracking Systems).

## Features

- **Web Research**: Automatically researches current best practices for software engineering resumes
- **Comprehensive Analysis**: Evaluates resume against industry standards
- **Scoring System**: Provides an overall score (0-100) for your resume
- **Actionable Feedback**: Lists specific strengths, weaknesses, and improvements
- **Improved Sections**: Generates ready-to-use improved versions of key resume sections

## Input

**Provide EITHER `resume_text` OR `resume_file_path` (not both)**

- `resume_text` (string, optional): The full text of your resume as a string
- `resume_file_path` (string, optional): Path to your resume file (PDF or TXT)
- `target_role` (string, optional): Target role (default: "Software Engineer")
- `years_experience` (integer, optional): Years of experience (default: 0)

### Supported File Formats

- **PDF** (.pdf) - Recommended for formatted resumes
- **Plain Text** (.txt) - Simple text resumes
- **DOCX** (.docx) - Requires additional library (not yet supported)

## Output

- `overall_score` (integer): Resume quality score from 0-100
- `strengths` (list): Top strengths identified in the resume
- `weaknesses` (list): Areas that need improvement
- `specific_improvements` (list): Actionable recommendations
- `best_practices` (string): Summary of current industry best practices
- `improved_sections` (object): Rewritten sections ready to use

## Setup

1. Set up your environment variables in `.env`:
```bash
ANTHROPIC_API_KEY=your_api_key_here
TAVILY_API_KEY=your_tavily_api_key_here
```

2. Install dependencies:
```bash
cd samples/test-agent
uv sync
```

## Usage

### Option 1: Upload a Resume File (PDF or TXT)

**Recommended for most users**

```bash
cd samples/test-agent
uv run uipath run agent '{
  "resume_file_path": "path/to/your/resume.pdf",
  "target_role": "Senior Software Engineer",
  "years_experience": 5
}'
```

Or with the sample file:
```bash
uv run uipath run agent --input-file sample-file-input.json
```

### Option 2: Paste Resume Text Directly

```bash
cd samples/test-agent
uv run uipath run agent '{
  "resume_text": "Your full resume text here...",
  "target_role": "Senior Software Engineer",
  "years_experience": 5
}'
```

### Option 3: Using an Input File with Text

Create an `input.json` file:
```json
{
  "resume_text": "John Doe\nSoftware Engineer\n\nExperience:\n- Built web applications\n- Worked with databases\n\nSkills:\nPython, JavaScript, SQL",
  "target_role": "Full Stack Developer",
  "years_experience": 3
}
```

Then run:
```bash
uv run uipath run agent --input-file input.json
```

## Example Output

```
overall_score: 75
strengths:
  - Clear technical skills section
  - Good project descriptions
  - Quantified achievements
weaknesses:
  - Missing keywords for ATS
  - Inconsistent formatting
  - Lacks action verbs
specific_improvements:
  - Add more technical keywords relevant to the role
  - Use consistent bullet point formatting
  - Start each bullet with strong action verbs
improved_sections:
  professional_summary: "Results-driven Software Engineer with 5+ years..."
  sample_bullet: "• Architected microservices platform serving 1M+ users..."
```

## How It Works

The agent follows a 5-step pipeline:

1. **Load Resume** - Extracts text from PDF/TXT file or uses provided text
2. **Research Best Practices** - Searches the web for current resume best practices
3. **Analyze Resume** - Compares your resume against those standards
4. **Generate Improvements** - Creates improved versions of key sections
5. **Finalize Output** - Packages everything into actionable recommendations

## Graph Structure

```
START → load_resume → research_best_practices → analyze_resume → generate_improvements → finalize_output → END
```

## Structure

- `graph.py`: Main agent implementation with LangGraph (4 nodes)
- `langgraph.json`: LangGraph configuration
- `pyproject.toml`: Python project configuration and dependencies

