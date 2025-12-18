# 🚀 Deploy Resume Fixer Agent to UiPath Cloud

## Quick Steps

Follow these steps to deploy your agent to UiPath Cloud:

---

## 📋 Step 1: Update Package Information

Edit `pyproject.toml` to add your details:

```toml
[project]
name = "resume-fixer-agent"
version = "1.0.0"
description = "AI-powered resume analysis and improvement agent for software engineers"
authors = [
    { name = "Pooja Dutt", email = "pooja@example.com" }
]
```

**Important:** 
- Description must NOT contain these characters: `&`, `<`, `>`, `"`, `'`, `;`
- Author information is required

---

## 📋 Step 2: Authenticate with UiPath Cloud

Run the authentication command:

```bash
uipath auth
```

**What happens:**
1. ✅ Browser opens for authentication
2. ✅ Login with your UiPath credentials
3. ✅ Select your tenant (organization)
4. ✅ Credentials saved to `.env` file

**Example:**
```
👇 Select tenant:
  0: DefaultTenant
  1: MyCompany
  2: TestTenant
...
Select tenant: 1
```

---

## 📋 Step 3: Package Your Agent

Create a `.nupkg` package file:

```bash
uipath pack
```

**Output:**
```
⠋ Packaging project ...
Name       : resume-fixer-agent
Version    : 1.0.0
Description: AI-powered resume analysis and improvement agent
Authors    : Pooja Dutt
✓  Project successfully packaged.
```

**What it creates:**
- `resume-fixer-agent.1.0.0.nupkg` file in your project directory

---

## 📋 Step 4: Publish to UiPath Cloud

### Option A: Publish to My Workspace (Easiest)

```bash
uipath publish --my-workspace
```

**Output:**
```
⠙ Publishing most recent package: resume-fixer-agent.1.0.0.nupkg ...
✓  Package published successfully!
⠦ Getting process information ...
🔗 Process configuration link: https://cloud.uipath.com/...
💡 Use the link above to configure any environment variables
```

**Benefits:**
- ✅ Process is auto-created for you
- ✅ Ready to use immediately
- ✅ Perfect for testing

### Option B: Publish to Specific Feed

```bash
uipath publish
```

**Then select feed:**
```
👇 Select package feed:
  0: Orchestrator Tenant Processes Feed
  1: Orchestrator Shared Folder Feed
  2: Orchestrator Personal Workspace Feed
...
Select feed number: 2
```

---

## 📋 Step 5: Configure Environment Variables

Click the link from Step 4 to configure your API keys:

**Required Environment Variables:**
- `ANTHROPIC_API_KEY` - Your Claude API key
- `TAVILY_API_KEY` - Your Tavily search API key (optional)

**In UiPath Cloud:**
1. Click the process configuration link
2. Go to "Environment Variables" section
3. Add your API keys
4. Click "Save"

---

## 📋 Step 6: Test Your Agent

### From UiPath Studio:

1. **Create new workflow**
2. **Add "Invoke Agent" activity**
3. **Configure:**
   - Agent: `resume-fixer-agent`
   - Input: See example below
4. **Run!**

**Example Input:**

```vb
' Read resume PDF
Dim pdfBytes As Byte() = File.ReadAllBytes("C:\Users\Pooja\Documents\resume.pdf")
Dim base64Resume As String = Convert.ToBase64String(pdfBytes)

' Create input
Dim agentInput As New Dictionary(Of String, Object) From {
    {"resume_base64", base64Resume},
    {"target_role", "Software Engineer"},
    {"years_experience", 7}
}

' Invoke agent
Dim result = Await InvokeAgent("resume-fixer-agent", agentInput)

' Get results
Dim score As Integer = CInt(result("overall_score"))
Dim strengths As List(Of String) = CType(result("strengths"), List(Of String))
```

---

## 🎯 Complete Command Sequence

Here's the full sequence from start to finish:

```bash
# 1. Authenticate
uipath auth

# 2. Package
uipath pack

# 3. Publish
uipath publish --my-workspace

# 4. Configure environment variables (use the link from publish output)
```

---

## 🔧 Troubleshooting

### "Description contains invalid characters"
- Remove `&`, `<`, `>`, `"`, `'`, `;` from description in `pyproject.toml`

### "Author information required"
- Add `authors = [{ name = "Your Name", email = "your@email.com" }]` to `pyproject.toml`

### "Authentication failed"
- Run `uipath auth` again
- Make sure you have access to UiPath Cloud

### "Package not found"
- Run `uipath pack` first
- Check that `.nupkg` file exists in your directory

---

## ✅ You're Done!

Your agent is now deployed and ready to use in UiPath! 🎉

**Next Steps:**
- Create workflows in UiPath Studio
- Use the agent to analyze resumes
- See `UIPATH_FILE_UPLOAD_GUIDE.md` for usage examples

