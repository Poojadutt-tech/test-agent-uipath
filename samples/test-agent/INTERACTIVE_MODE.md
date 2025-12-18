# 🎯 Interactive Resume Upload Mode

## Overview

The Resume Fixer Agent supports **human-in-the-loop** resume upload! When you don't provide resume data, the agent will pause and wait for you to provide it.

---

## 🚀 How to Use

### **Option 1: Interactive Mode (with prompt)**

Run with an empty input to trigger the interactive prompt:

```bash
uv run uipath run agent '{}'
```

**What happens:**
1. ✅ Agent starts and detects no resume provided
2. ✅ Agent pauses with instructions on how to provide resume
3. ✅ You resume with your resume data
4. ✅ Agent processes your resume automatically

**To resume execution:**
```bash
# Provide resume via file path (local testing)
uv run uipath run agent '{"resume_file_path": "/path/to/resume.pdf", "target_role": "Software Engineer", "years_experience": 7}' --resume

# Or provide resume as base64 (UiPath deployment)
uv run uipath run agent '{"resume_base64": "JVBERi0x...", "target_role": "Software Engineer", "years_experience": 7}' --resume
```

---

### **Option 2: Direct Input (skip form)**

If you provide resume data in the input, the form is **skipped**:

```bash
# Using file path (local testing)
uv run uipath run agent --input-file pooja-resume-input.json

# Using base64 (UiPath deployment)
uv run uipath run agent '{"resume_base64": "JVBERi0x...", "target_role": "Software Engineer", "years_experience": 7}'

# Using plain text
uv run uipath run agent '{"resume_text": "John Doe...", "target_role": "Software Engineer", "years_experience": 7}'
```

---

## 📋 The Interactive Form

When triggered, you'll see a form with these fields:

### **1. Resume File** (Required)
- **Type**: File upload
- **Accepts**: `.pdf`, `.txt`
- **Description**: Upload your resume file

### **2. Target Role** (Required)
- **Type**: Text input
- **Default**: "Software Engineer"
- **Description**: What position are you applying for?

### **3. Years of Experience** (Required)
- **Type**: Number input
- **Default**: 0
- **Range**: 0-50
- **Description**: How many years of relevant experience?

---

## 🎨 UiPath Integration

### In UiPath Studio

The form will automatically appear in UiPath Action Center when deployed:

```vb
' Simply call the agent with empty input
Dim input As New Dictionary(Of String, Object)

' The form will pop up in Action Center
Dim result = Await agentClient.InvokeAsync("agent", input)

' User fills out the form in Action Center
' Agent continues processing automatically
```

### What Users See in UiPath

1. **Action Center notification** appears
2. User clicks to open the form
3. User uploads resume PDF
4. User fills in target role and experience
5. User submits
6. Agent processes and returns results

---

## 🔧 How It Works

### Flow Diagram

```
START
  ↓
prompt_for_resume (shows form if no resume provided)
  ↓
load_resume (extracts text from uploaded file)
  ↓
research_best_practices
  ↓
analyze_resume
  ↓
generate_improvements
  ↓
finalize_output
  ↓
END
```

### Smart Detection

The `prompt_for_resume` node checks:
- ✅ If `resume_text` is provided → skip form
- ✅ If `resume_file_path` is provided → skip form
- ✅ If `resume_base64` is provided → skip form
- ❌ If **nothing** is provided → **show form**

---

## 💡 Benefits

### For Local Testing
- ✅ No need to create JSON input files
- ✅ Easy to test with different resumes
- ✅ Visual file picker

### For UiPath Deployment
- ✅ User-friendly interface in Action Center
- ✅ No technical knowledge required
- ✅ Guided input with validation
- ✅ Works seamlessly with human-in-the-loop workflows

---

## 📝 Example Usage

### Local Testing (Interactive)
```bash
cd samples/test-agent
uv run uipath run agent '{}'
# Form appears → upload resume → enter details → submit
```

### Local Testing (Direct)
```bash
uv run uipath run agent --input-file pooja-resume-input.json
# No form → processes immediately
```

### UiPath Deployment
```vb
' In UiPath Studio
Dim agentInput As New Dictionary(Of String, Object)
Dim result = Await InvokeAgent("resume-fixer", agentInput)

' User gets Action Center task
' User uploads resume via form
' Result contains analysis and improvements
```

---

## 🎯 Best Practices

1. **For end users**: Use interactive mode (empty input)
2. **For automation**: Provide resume data directly (skip form)
3. **For testing**: Use interactive mode with different resumes
4. **For production**: Deploy to UiPath with Action Center integration

---

## 🚨 Troubleshooting

### Form doesn't appear
- Make sure you're passing empty input: `{}`
- Check that you're not providing any resume data

### File upload fails
- Ensure file is PDF or TXT format
- Check file size (should be < 10MB)
- Verify file is not corrupted

### Form appears when it shouldn't
- You're passing empty input
- Provide `resume_text`, `resume_file_path`, or `resume_base64` to skip form

