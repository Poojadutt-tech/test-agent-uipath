from langchain_anthropic import ChatAnthropic
from langchain_tavily import TavilySearch
from langchain_core.messages import HumanMessage, SystemMessage, BaseMessage
from langgraph.constants import START, END
from langgraph.graph import StateGraph
from pydantic import BaseModel, Field
from uipath.tracing import traced
from typing import Optional
import PyPDF2
import io
import base64
import os


class ResumeInput(BaseModel):
    """Input model for resume analysis.

    Can be empty - user will be prompted to upload resume via form.
    Or provide ONE of: resume_text, resume_file_path (local), or resume_base64 (UiPath deployment).
    """
    resume_text: Optional[str] = None
    resume_file_path: Optional[str] = None  # Path to PDF/TXT file (local testing only)
    resume_base64: Optional[str] = None  # Base64 encoded PDF (for UiPath deployment)
    target_role: Optional[str] = None  # Will prompt if not provided
    years_experience: Optional[int] = None  # Will prompt if not provided


class ResumeOutput(BaseModel):
    """Output model with analysis and recommendations."""
    overall_score: int  # 0-100
    strengths: list[str]
    weaknesses: list[str]
    specific_improvements: list[str]
    best_practices: str
    improved_sections: dict[str, str]


class State(BaseModel):
    """Internal state for resume processing."""
    resume_text: str = ""  # Will be populated from text, file, or base64
    resume_file_path: Optional[str] = None
    resume_base64: Optional[str] = None
    target_role: str = "Software Engineer"
    years_experience: int = 0
    best_practices: str = ""
    resume_analysis: str = ""
    strengths: list[str] = []
    weaknesses: list[str] = []
    specific_improvements: list[str] = []
    improved_sections: dict[str, str] = {}
    overall_score: int = 0


# Structured output models for LLM responses
class ResumeAnalysis(BaseModel):
    """Structured output from resume analysis."""
    score: int = Field(description="Overall resume quality score from 0-100")
    strengths: list[str] = Field(description="List of 3-5 key strengths in the resume")
    weaknesses: list[str] = Field(description="List of 3-5 areas that need improvement")
    improvements: list[str] = Field(description="List of 3-5 specific actionable improvements")


class ImprovedSections(BaseModel):
    """Structured output for improved resume sections."""
    professional_summary: str = Field(description="Improved professional summary (2-3 sentences)")
    sample_bullet: str = Field(description="One improved bullet point for experience section")
    technical_skills: str = Field(description="Improved technical skills section formatted for ATS")


def extract_text_from_pdf(file_path: str) -> str:
    """Extract text from a PDF file."""
    with open(file_path, 'rb') as file:
        pdf_reader = PyPDF2.PdfReader(file)
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text() + "\n"
    return text.strip()


def extract_text_from_pdf_bytes(pdf_bytes: bytes) -> str:
    """Extract text from PDF bytes (for base64 input)."""
    pdf_reader = PyPDF2.PdfReader(io.BytesIO(pdf_bytes))
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text() + "\n"
    return text.strip()


def extract_text_from_txt(file_path: str) -> str:
    """Extract text from a TXT file."""
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read().strip()


def extract_text_from_file(file_path: str) -> str:
    """Extract text from various file formats."""
    if file_path.lower().endswith('.pdf'):
        return extract_text_from_pdf(file_path)
    elif file_path.lower().endswith('.txt'):
        return extract_text_from_txt(file_path)
    elif file_path.lower().endswith('.docx'):
        # For DOCX support, we'd need python-docx library
        raise ValueError("DOCX support requires python-docx library. Please convert to PDF or TXT.")
    else:
        raise ValueError(f"Unsupported file format. Supported: .pdf, .txt")


@traced(name="load_resume")
async def load_resume(state: State) -> State:
    """Load resume from file, base64, or text."""
    if state.resume_file_path:
        # Local file path (for testing)
        state.resume_text = extract_text_from_file(state.resume_file_path)
    elif state.resume_base64:
        # Base64 encoded PDF (for UiPath deployment)
        pdf_bytes = base64.b64decode(state.resume_base64)
        state.resume_text = extract_text_from_pdf_bytes(pdf_bytes)
    elif not state.resume_text:
        raise ValueError("Must provide one of: resume_text, resume_file_path, or resume_base64")

    return state


# Initialize tools and LLM
# Make Tavily optional - only initialize if API key is available
tavily_tool = None
if os.getenv("TAVILY_API_KEY"):
    tavily_tool = TavilySearch(max_results=5)

# Using Claude 3.5 Haiku - faster and cheaper, good for resume analysis
llm = ChatAnthropic(model="claude-3-5-haiku-20241022")


@traced(name="research_best_practices")
async def research_best_practices(state: State) -> State:
    """Research current best practices for software engineering resumes."""
    search_query = f"best practices for {state.target_role} resume {state.years_experience} years experience 2025"

    system_msg = SystemMessage(content="""You are a resume expert. Research and summarize the top 5-7
    best practices for software engineering resumes. Focus on: format, content structure,
    technical skills presentation, project descriptions, and ATS optimization.""")

    # Use Tavily to search if available, otherwise use LLM's built-in knowledge
    if tavily_tool:
        # Use Tavily to search for best practices
        search_results = tavily_tool.invoke({"query": search_query})

        # Summarize findings with LLM
        summary_prompt = f"""Based on these search results about resume best practices:

{search_results}

Provide a concise summary of the top 7 best practices for a {state.target_role} resume
with {state.years_experience} years of experience. Format as a numbered list."""
    else:
        # No Tavily - use LLM's built-in knowledge
        summary_prompt = f"""Provide a concise summary of the top 7 best practices for a {state.target_role} resume
with {state.years_experience} years of experience in 2025. Focus on: format, content structure,
technical skills presentation, project descriptions, and ATS optimization. Format as a numbered list."""

    response = await llm.ainvoke([
        system_msg,
        HumanMessage(content=summary_prompt)
    ])

    state.best_practices = response.content if isinstance(response.content, str) else str(response.content)
    return state


@traced(name="analyze_resume")
async def analyze_resume(state: State) -> State:
    """Analyze the resume against best practices using structured output."""
    analysis_prompt = f"""Analyze this software engineering resume against current best practices.

BEST PRACTICES TO FOLLOW:
{state.best_practices}

RESUME TO ANALYZE:
{state.resume_text}

TARGET ROLE: {state.target_role}
EXPERIENCE LEVEL: {state.years_experience} years

Provide a comprehensive analysis with:
- An overall quality score (0-100)
- 3-5 key strengths (what's working well)
- 3-5 critical weaknesses (what needs improvement)
- 3-5 specific, actionable improvements

Be specific and reference actual content from the resume."""

    # Use structured output - LLM will return a ResumeAnalysis object
    structured_llm = llm.with_structured_output(ResumeAnalysis)

    analysis: ResumeAnalysis = await structured_llm.ainvoke([
        SystemMessage(content="You are a professional resume analyst. Provide detailed, actionable feedback."),
        HumanMessage(content=analysis_prompt)
    ])

    # Store structured results directly - no parsing needed!
    state.overall_score = analysis.score
    state.strengths = analysis.strengths
    state.weaknesses = analysis.weaknesses
    state.specific_improvements = analysis.improvements
    state.resume_analysis = f"Score: {analysis.score}\n\nStrengths:\n" + "\n".join(f"- {s}" for s in analysis.strengths) + "\n\nWeaknesses:\n" + "\n".join(f"- {w}" for w in analysis.weaknesses)

    return state


@traced(name="generate_improvements")
async def generate_improvements(state: State) -> State:
    """Generate specific improved sections of the resume using structured output."""
    improvement_prompt = f"""Based on this resume analysis:

WEAKNESSES:
{chr(10).join(f"- {w}" for w in state.weaknesses)}

IMPROVEMENTS NEEDED:
{chr(10).join(f"- {i}" for i in state.specific_improvements)}

ORIGINAL RESUME:
{state.resume_text}

Generate improved versions of the following sections:
1. Professional Summary (2-3 sentences)
2. A sample improved bullet point for experience section
3. Technical Skills section (formatted for ATS)

Provide these as separate, ready-to-use text that can be copied directly into a resume."""

    # Use structured output - LLM will return an ImprovedSections object
    structured_llm = llm.with_structured_output(ImprovedSections)

    improvements: ImprovedSections = await structured_llm.ainvoke([
        SystemMessage(content="You are a professional resume writer. Create polished, ATS-friendly content."),
        HumanMessage(content=improvement_prompt)
    ])

    # Store structured results directly - no parsing needed!
    state.improved_sections = {
        "professional_summary": improvements.professional_summary,
        "sample_bullet": improvements.sample_bullet,
        "technical_skills": improvements.technical_skills
    }

    return state


@traced(name="finalize_output")
async def finalize_output(state: State) -> ResumeOutput:
    """Create final output with all recommendations."""
    return ResumeOutput(
        overall_score=state.overall_score,
        strengths=state.strengths,
        weaknesses=state.weaknesses,
        specific_improvements=state.specific_improvements,
        best_practices=state.best_practices,
        improved_sections=state.improved_sections
    )


# Build the graph
builder = StateGraph(
    state_schema=State,
    input=ResumeInput,
    output=ResumeOutput
)

# Add nodes
builder.add_node("load_resume", load_resume)
builder.add_node("research_best_practices", research_best_practices)
builder.add_node("analyze_resume", analyze_resume)
builder.add_node("generate_improvements", generate_improvements)
builder.add_node("finalize_output", finalize_output)

# Add edges - linear flow
builder.add_edge(START, "load_resume")
builder.add_edge("load_resume", "research_best_practices")
builder.add_edge("research_best_practices", "analyze_resume")
builder.add_edge("analyze_resume", "generate_improvements")
builder.add_edge("generate_improvements", "finalize_output")
builder.add_edge("finalize_output", END)

graph = builder.compile()

