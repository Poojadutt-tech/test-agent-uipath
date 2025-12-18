# 🚀 UiPath Deployment Guide

## File Handling Options for UiPath Cloud

When deploying to UiPath, you have **3 options** for providing resume files:

---

## ✅ **Option 1: Base64 Encoding (Recommended)**

### How It Works
Convert the PDF to base64 string and pass it directly in the input.

### In UiPath Studio
```vb
' Read PDF file as bytes
Dim pdfBytes As Byte() = File.ReadAllBytes("C:\path\to\resume.pdf")

' Convert to base64
Dim base64String As String = Convert.ToBase64String(pdfBytes)

' Create input JSON
Dim input As New Dictionary(Of String, Object) From {
    {"resume_base64", base64String},
    {"target_role", "Software Engineer"},
    {"years_experience", 7}
}

' Call the agent
Dim result = Await agentClient.InvokeAsync("agent", input)
```

### Advantages
- ✅ No external storage needed
- ✅ Works immediately
- ✅ Simple to implement
- ✅ No file path issues

### Disadvantages
- ❌ Large payload size for big PDFs
- ❌ Not ideal for very large files (>5MB)

---

## ✅ **Option 2: UiPath Storage Buckets**

### How It Works
Upload files to UiPath Storage, then reference them by name.

### Setup
1. Create a Storage Bucket in UiPath Orchestrator
2. Upload resume files to the bucket
3. Reference files by name in your agent

### Code Changes Needed
```python
# In graph.py, modify load_resume function:
from uipath.storage import StorageBucket

@traced(name="load_resume")
async def load_resume(state: State) -> State:
    if state.resume_file_path:
        # Check if it's a UiPath storage path
        if state.resume_file_path.startswith("storage://"):
            bucket_name = "resume-uploads"
            file_name = state.resume_file_path.replace("storage://", "")
            
            bucket = StorageBucket(bucket_name)
            pdf_bytes = await bucket.download(file_name)
            state.resume_text = extract_text_from_pdf_bytes(pdf_bytes)
        else:
            # Local file path
            state.resume_text = extract_text_from_file(state.resume_file_path)
    # ... rest of the code
```

### In UiPath Studio
```vb
' Upload file to storage bucket
Dim bucketClient = New StorageBucketClient("resume-uploads")
Await bucketClient.UploadAsync("resume.pdf", "C:\path\to\resume.pdf")

' Call agent with storage path
Dim input As New Dictionary(Of String, Object) From {
    {"resume_file_path", "storage://resume.pdf"},
    {"target_role", "Software Engineer"},
    {"years_experience", 7}
}
```

### Advantages
- ✅ Handles large files
- ✅ Reusable storage
- ✅ Better for multiple files

### Disadvantages
- ❌ Requires storage bucket setup
- ❌ More complex implementation

---

## ✅ **Option 3: Plain Text Input**

### How It Works
Extract text from PDF in UiPath, pass as plain text.

### In UiPath Studio
```vb
' Use UiPath PDF activities to extract text
Dim resumeText As String = ReadPDFText("C:\path\to\resume.pdf")

' Call agent with text
Dim input As New Dictionary(Of String, Object) From {
    {"resume_text", resumeText},
    {"target_role", "Software Engineer"},
    {"years_experience", 7}
}
```

### Advantages
- ✅ Simplest approach
- ✅ No file handling needed
- ✅ Works with any PDF extraction method

### Disadvantages
- ❌ Loses formatting information
- ❌ Requires PDF extraction in UiPath first

---

## 📋 Current Implementation Status

The agent **currently supports all 3 options**:

```json
// Option 1: Base64 (UiPath deployment)
{
  "resume_base64": "JVBERi0xLjQKJeLjz9MKMy...",
  "target_role": "Software Engineer",
  "years_experience": 7
}

// Option 2: File path (local testing)
{
  "resume_file_path": "/path/to/resume.pdf",
  "target_role": "Software Engineer",
  "years_experience": 7
}

// Option 3: Plain text
{
  "resume_text": "John Doe\nSoftware Engineer...",
  "target_role": "Software Engineer",
  "years_experience": 7
}
```

---

## 🎯 Recommendation

**For UiPath deployment**: Use **Option 1 (Base64)** for simplicity, or **Option 2 (Storage Buckets)** for large files.

**For local testing**: Use **Option 2 (File Path)** as you're doing now.

