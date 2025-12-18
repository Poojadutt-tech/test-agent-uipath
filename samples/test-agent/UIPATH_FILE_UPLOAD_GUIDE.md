# 📤 How to Upload Resume Files in UiPath

## 🎯 The Simple Answer

When you deploy this agent to UiPath, you have **2 main options** for uploading resume files:

---

## ✅ **Option 1: Convert PDF to Base64 in UiPath Studio (Recommended)**

This is the **easiest and most common** approach.

### In UiPath Studio Workflow:

```vb
' Step 1: Read the PDF file as bytes
Dim pdfBytes As Byte() = File.ReadAllBytes("C:\Users\YourName\Documents\resume.pdf")

' Step 2: Convert to Base64 string
Dim base64Resume As String = Convert.ToBase64String(pdfBytes)

' Step 3: Call the agent with base64 data
Dim agentInput As New Dictionary(Of String, Object) From {
    {"resume_base64", base64Resume},
    {"target_role", "Software Engineer"},
    {"years_experience", 7}
}

' Step 4: Invoke the agent
Dim result = Await InvokeAgent("resume-fixer", agentInput)

' Step 5: Use the results
Console.WriteLine("Resume Score: " & result("overall_score"))
Console.WriteLine("Strengths: " & String.Join(", ", result("strengths")))
```

### Why This Works:
- ✅ No file storage needed
- ✅ Works immediately after deployment
- ✅ Simple to implement
- ✅ Secure (file content is sent directly)

---

## ✅ **Option 2: Use UiPath File Picker Activity**

If you want users to select their resume file interactively:

### In UiPath Studio Workflow:

```vb
' Step 1: Let user pick a file
Dim filePath As String
' Use "File Select Dialog" activity
' Output: filePath

' Step 2: Read and convert to base64
Dim pdfBytes As Byte() = File.ReadAllBytes(filePath)
Dim base64Resume As String = Convert.ToBase64String(pdfBytes)

' Step 3: Call the agent
Dim agentInput As New Dictionary(Of String, Object) From {
    {"resume_base64", base64Resume},
    {"target_role", "Software Engineer"},
    {"years_experience", 7}
}

Dim result = Await InvokeAgent("resume-fixer", agentInput)
```

### Why This Works:
- ✅ User-friendly file selection
- ✅ Works with any PDF on user's computer
- ✅ No hardcoded file paths

---

## 📋 Complete UiPath Studio Example

Here's a full workflow you can copy:

```vb
' ============================================
' RESUME FIXER AGENT - UIPATH WORKFLOW
' ============================================

' 1. GET RESUME FILE
Dim resumeFilePath As String = "C:\Users\Pooja\Documents\PoojaDuttResumeMain.pdf"
' Or use File Select Dialog activity to let user choose

' 2. READ FILE AS BYTES
Dim resumeBytes As Byte() = File.ReadAllBytes(resumeFilePath)

' 3. CONVERT TO BASE64
Dim resumeBase64 As String = Convert.ToBase64String(resumeBytes)

' 4. PREPARE INPUT
Dim agentInput As New Dictionary(Of String, Object) From {
    {"resume_base64", resumeBase64},
    {"target_role", "Senior Software Engineer"},
    {"years_experience", 7}
}

' 5. CALL AGENT
Dim agentResult = Await InvokeAgent("resume-fixer", agentInput)

' 6. EXTRACT RESULTS
Dim score As Integer = CInt(agentResult("overall_score"))
Dim strengths As List(Of String) = CType(agentResult("strengths"), List(Of String))
Dim weaknesses As List(Of String) = CType(agentResult("weaknesses"), List(Of String))
Dim improvements As List(Of String) = CType(agentResult("specific_improvements"), List(Of String))
Dim improvedSections As Dictionary(Of String, String) = CType(agentResult("improved_sections"), Dictionary(Of String, String))

' 7. DISPLAY OR USE RESULTS
Console.WriteLine("=== RESUME ANALYSIS ===")
Console.WriteLine("Overall Score: " & score & "/100")
Console.WriteLine("")
Console.WriteLine("Strengths:")
For Each strength In strengths
    Console.WriteLine("  ✓ " & strength)
Next
Console.WriteLine("")
Console.WriteLine("Areas to Improve:")
For Each weakness In weaknesses
    Console.WriteLine("  ✗ " & weakness)
Next
Console.WriteLine("")
Console.WriteLine("Recommended Improvements:")
For Each improvement In improvements
    Console.WriteLine("  → " & improvement)
Next
Console.WriteLine("")
Console.WriteLine("Improved Professional Summary:")
Console.WriteLine(improvedSections("professional_summary"))
```

---

## 🚀 Quick Start Steps

1. **Deploy agent to UiPath Cloud** (using `uipath deploy` or UiPath Studio)
2. **Create a new workflow** in UiPath Studio
3. **Add "Invoke Agent" activity**
4. **Select your deployed agent** ("resume-fixer")
5. **Use the code above** to prepare the input
6. **Run the workflow!**

---

## 💡 Key Points

- **Always use `resume_base64`** when calling from UiPath
- **Don't use `resume_file_path`** in UiPath (that's only for local testing)
- **File size limit**: Keep PDFs under 10MB for best performance
- **Supported formats**: PDF and TXT (PDF recommended)

---

## 🔧 Troubleshooting

### "File not found" error
- Check the file path is correct
- Use full path: `C:\Users\...\resume.pdf`

### "Invalid base64" error
- Make sure you're reading the file as bytes: `File.ReadAllBytes()`
- Use `Convert.ToBase64String()` to convert

### Agent returns error
- Check that `resume_base64` is not empty
- Verify the PDF is not corrupted
- Make sure `target_role` and `years_experience` are provided

---

## ✅ That's It!

The key is: **Read PDF → Convert to Base64 → Pass to Agent**

Simple! 🎉

