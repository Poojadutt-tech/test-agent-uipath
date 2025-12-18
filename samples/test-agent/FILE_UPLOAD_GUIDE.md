# Resume File Upload Guide

## Supported File Formats

The Resume Fixer Agent supports the following file formats:

### ✅ PDF (.pdf)
- **Recommended format** for formatted resumes
- Uses PyPDF2 library for text extraction
- Preserves most text content from formatted documents
- **Best for**: Professional resumes created in Word, Google Docs, etc.

### ✅ Plain Text (.txt)
- Simple text files
- Direct text reading with UTF-8 encoding
- **Best for**: Simple, unformatted resumes

### ⚠️ DOCX (.docx)
- **Not yet supported** (requires python-docx library)
- **Workaround**: Convert to PDF or save as TXT

## How to Use File Upload

### Method 1: Direct File Path in JSON

```bash
uv run uipath run agent '{
  "resume_file_path": "path/to/resume.pdf",
  "target_role": "Senior Software Engineer",
  "years_experience": 5
}'
```

### Method 2: Using Input File

Create `input.json`:
```json
{
  "resume_file_path": "resume.pdf",
  "target_role": "Full Stack Developer",
  "years_experience": 3
}
```

Run:
```bash
uv run uipath run agent --input-file input.json
```

### Method 3: Relative vs Absolute Paths

**Relative path** (from current directory):
```json
{
  "resume_file_path": "my-resume.pdf"
}
```

**Absolute path**:
```json
{
  "resume_file_path": "/Users/username/Documents/resume.pdf"
}
```

## How It Works Internally

### 1. File Detection
The `load_resume` node checks the file extension:
- `.pdf` → Uses PyPDF2 to extract text
- `.txt` → Reads file with UTF-8 encoding
- Other → Raises error

### 2. Text Extraction
```python
def extract_text_from_pdf(file_path: str) -> str:
    with open(file_path, 'rb') as file:
        pdf_reader = PyPDF2.PdfReader(file)
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text() + "\n"
    return text.strip()
```

### 3. State Population
The extracted text is stored in `state.resume_text` and used by subsequent nodes.

## Input Validation

The agent validates that you provide **EITHER**:
- `resume_text` (string) - Direct text input
- `resume_file_path` (string) - Path to file

**Not both!** If you provide both, the file path takes precedence.

## Common Issues & Solutions

### Issue: "File not found"
**Solution**: Check that the file path is correct and the file exists
```bash
# Verify file exists
ls -la resume.pdf
```

### Issue: "Unsupported file format"
**Solution**: Convert to PDF or TXT
- PDF: Use "Save as PDF" in Word/Google Docs
- TXT: Use "Save as Plain Text"

### Issue: "PDF text extraction is garbled"
**Solution**: Some PDFs (especially scanned images) don't have extractable text
- Use OCR tools first (Adobe Acrobat, online OCR)
- Or manually copy/paste text and use `resume_text` instead

### Issue: "Permission denied"
**Solution**: Check file permissions
```bash
chmod 644 resume.pdf
```

## Best Practices

1. **Use PDF for formatted resumes** - Best text extraction
2. **Use TXT for simple resumes** - Fastest processing
3. **Test extraction first** - Run the agent to see if text extracts correctly
4. **Avoid scanned PDFs** - These are images, not text
5. **Use descriptive filenames** - Easier to track and debug

## Example Files

The agent includes sample files for testing:

- `sample-resume.txt` - Plain text resume example
- `sample-file-input.json` - Input file using file path
- `sample-resume-input.json` - Input file using direct text

## Adding DOCX Support (Future)

To add DOCX support, you would:

1. Add dependency to `pyproject.toml`:
```toml
dependencies = [
    ...
    "python-docx>=1.0.0",
]
```

2. Add extraction function in `graph.py`:
```python
from docx import Document

def extract_text_from_docx(file_path: str) -> str:
    doc = Document(file_path)
    return "\n".join([para.text for para in doc.paragraphs])
```

3. Update `extract_text_from_file()` to handle `.docx` extension

