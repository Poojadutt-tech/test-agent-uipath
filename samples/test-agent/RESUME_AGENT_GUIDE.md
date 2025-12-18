# Resume Fixer Agent - Developer Guide

## What This Agent Does

The Resume Fixer Agent is an AI-powered tool that:
1. Researches current best practices for software engineering resumes
2. Analyzes your resume against those standards
3. Identifies strengths and weaknesses
4. Generates improved versions of key resume sections
5. Provides actionable recommendations

## Architecture

### Graph Structure (5 Nodes)

```
START
  ↓
load_resume (Extract text from PDF/TXT or use provided text)
  ↓
research_best_practices (Web search for current standards)
  ↓
analyze_resume (Compare resume vs best practices)
  ↓
generate_improvements (Create improved sections)
  ↓
finalize_output (Package recommendations)
  ↓
END
```

### Data Models

**Input (ResumeInput)**
- `resume_text`: string (optional) - Full resume text as string
- `resume_file_path`: string (optional) - Path to PDF/TXT resume file
- `target_role`: string (default: "Software Engineer")
- `years_experience`: int (default: 0)

**Note**: Provide EITHER `resume_text` OR `resume_file_path`, not both.

**State (Internal Processing)**
- All input fields plus:
- `best_practices`: string - Research findings
- `resume_analysis`: string - Analysis results
- `strengths`: list[str] - Identified strengths
- `weaknesses`: list[str] - Areas to improve
- `specific_improvements`: list[str] - Recommendations
- `improved_sections`: dict - Rewritten content
- `overall_score`: int - Quality score 0-100

**Output (ResumeOutput)**
- `overall_score`: int
- `strengths`: list[str]
- `weaknesses`: list[str]
- `specific_improvements`: list[str]
- `best_practices`: string
- `improved_sections`: dict[str, str]

## Key Technologies

- **LangGraph**: State graph orchestration
- **Claude (Anthropic)**: LLM for analysis and content generation
- **Tavily**: Web search for research
- **UiPath SDK**: Tracing and deployment

## Node Details

### 1. load_resume
- **Purpose**: Extract text from resume file or validate text input
- **Tools**: PyPDF2 for PDF parsing
- **Processing**: File format detection and text extraction
- **Output**: Populated `resume_text` in state

### 2. research_best_practices
- **Purpose**: Find current resume best practices
- **Tools**: Tavily web search
- **LLM**: Claude for summarization
- **Output**: Numbered list of 7 best practices

### 3. analyze_resume
- **Purpose**: Evaluate resume quality
- **Input**: Resume text + best practices
- **LLM**: Claude for analysis
- **Output**: Score, strengths, weaknesses, improvements

### 4. generate_improvements
- **Purpose**: Create improved resume sections
- **LLM**: Claude as resume writer
- **Output**: Rewritten professional summary, bullets, skills section

### 5. finalize_output
- **Purpose**: Package all data into output model
- **Processing**: Pure data transformation
- **Output**: ResumeOutput object

## Advanced Patterns Demonstrated

1. **Separate State Model**: Input/State/Output are different
   - Input: User-facing simple model
   - State: Rich internal processing state
   - Output: Structured recommendations

2. **LLM Integration**: Multiple LLM calls with different roles
   - Researcher (summarize findings)
   - Analyst (evaluate quality)
   - Writer (create content)

3. **Tool Usage**: Web search integration
   - Tavily for real-time research
   - Dynamic query construction

4. **Tracing**: All nodes use @traced decorator
   - Enables monitoring in UiPath
   - Tracks execution flow

## Testing Locally

1. Set up API keys in `.env`:
```bash
ANTHROPIC_API_KEY=sk-ant-...
TAVILY_API_KEY=tvly-...
```

2. Run with a file (PDF or TXT):
```bash
uv run uipath run agent --input-file sample-file-input.json
```

3. Or with text input:
```bash
uv run uipath run agent --input-file sample-resume-input.json
```

4. Or with inline JSON (file path):
```bash
uv run uipath run agent '{
  "resume_file_path": "sample-resume.txt",
  "target_role": "Senior Software Engineer",
  "years_experience": 5
}'
```

5. Or with inline JSON (text):
```bash
uv run uipath run agent '{
  "resume_text": "Your resume here...",
  "target_role": "Senior Software Engineer",
  "years_experience": 5
}'
```

## Customization Ideas

### Easy Modifications
- Change target roles (add more role-specific analysis)
- Adjust scoring algorithm
- Add more resume sections to improve
- Customize best practices sources

### Advanced Modifications
- Add conditional routing (different paths for junior vs senior)
- Integrate with resume parsing libraries
- Add human-in-the-loop approval for suggestions
- Connect to job posting APIs for role-specific optimization
- Add ATS compatibility scoring
- Generate multiple resume versions for different roles

## Deployment to UiPath Cloud

1. Ensure all dependencies are in `pyproject.toml`
2. Run `uipath init` to generate entry-points.json
3. Deploy using UiPath deployment tools
4. Configure API keys in UiPath Orchestrator

## Comparison to Other Sample Agents

- **Simpler than**: multi-agent-supervisor (no dynamic routing)
- **More complex than**: calculator-agent (uses LLM + tools)
- **Similar to**: company-research-agent (research + analysis pattern)
- **Different from**: debug-agent (linear vs conditional flow)

## Next Steps

- Add more sophisticated parsing of LLM responses
- Implement structured output for better reliability
- Add support for PDF/DOCX resume uploads
- Create evaluation dataset for testing
- Add support for different resume formats (chronological, functional, hybrid)

