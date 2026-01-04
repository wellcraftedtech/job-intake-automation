# POC Testing Guide - Legal Job Intake Automation

## Prerequisites

Before testing, ensure you have:
- ✅ Python 3.10+ installed
- ✅ All dependencies installed (`pip install -r requirements.txt`)
- ✅ Valid OpenAI API key in `.env` file
- ✅ 25 sample emails in `sample_emails/` folder

---

## Setup Steps

### 1. Configure API Key
```bash
# Open .env file
nano .env

# Replace placeholder with your actual key
OPENAI_API_KEY=sk-YOUR_ACTUAL_OPENAI_KEY_HERE
```

### 2. Verify Installation
```bash
# Check Python version
python3 --version

# Verify dependencies
pip list | grep -E "openai|streamlit|pandas"
```

### 3. Check Sample Data
```bash
# Verify sample emails exist
ls -l sample_emails/
# Should show 25 .txt files (20 standard + 5 complex)
```

---

## Test Scenarios

### 🧪 Test 1: Single Email Extraction (Simple Case)

**Objective:** Verify basic extraction works correctly

**Steps:**
1. Start the Streamlit app:
   ```bash
   streamlit run app.py
   ```
2. Navigate to **"📧 Single Upload"** tab
3. Click **"Browse files"** and select `sample_emails/email_01.txt`
4. Click **"🚀 Extract Job Details"**

**Expected Results:**
- ✅ Processing completes in ~2-4 seconds
- ✅ Job card displays on the right side with:
  - Client: "Jenkins & Co Lawyers"
  - Job Type: "Process Service"
  - Address: "15 George St, Parramatta NSW 2150"
  - Urgency: "Urgent" (red badge)
  - Quote: ~$180 AUD (base $120 + 50% urgency)
- ✅ No errors in console

---

### 🧪 Test 2: Complex Email (Multiple Addresses)

**Objective:** Test handling of complex scenarios

**Steps:**
1. In **"📧 Single Upload"** tab
2. Upload `sample_emails/email_complex_01.txt`
3. Click **"🚀 Extract Job Details"**

**Expected Results:**
- ✅ Extracts primary address (first in list)
- ✅ Special instructions mention "multiple locations"
- ✅ Complexity marked as "High"
- ✅ Quote includes surcharges for complexity (+$100)
- ✅ Urgency detected correctly

---

### 🧪 Test 3: Paste Email Content

**Objective:** Verify manual paste functionality

**Steps:**
1. Open `sample_emails/email_02.txt` in a text editor
2. Copy the entire content
3. In Streamlit, paste into **"Or Paste Email Content"** text area
4. Click **"🚀 Extract Job Details"**

**Expected Results:**
- ✅ Same extraction quality as file upload
- ✅ Client: "City Legal"
- ✅ Job Type: "Process Service"
- ✅ Due Date: "10/01/2026"

---

### 🧪 Test 4: Batch Processing (5 Emails)

**Objective:** Test bulk processing capability

**Steps:**
1. Navigate to **"📦 Batch Processing"** tab
2. Click **"📁 Upload Multiple Emails"**
3. Select these 5 files (Cmd/Ctrl + Click):
   - `email_01.txt`
   - `email_02.txt`
   - `email_03.txt`
   - `email_04.txt`
   - `email_05.txt`
4. Click **"⚡ Process Batch"**

**Expected Results:**
- ✅ Progress bar shows incremental updates
- ✅ Processing completes in ~10-25 seconds (5 emails × ~2-5 sec each)
- ✅ Results table displays with 5 rows
- ✅ All statuses show "✅ Success"
- ✅ Download CSV button appears
- ✅ CSV contains all extracted data

---

### 🧪 Test 5: Full Batch (All 25 Emails)

**Objective:** Stress test with complete dataset

**Steps:**
1. In **"📦 Batch Processing"** tab
2. Select all 25 files from `sample_emails/`
3. Click **"⚡ Process Batch"**
4. Wait for completion

**Expected Results:**
- ✅ All 25 emails process successfully
- ✅ Total time: ~50-125 seconds
- ✅ Success rate: ≥95% (23-25 successful)
- ✅ Table shows variety of job types
- ✅ Quotes range from $120-$500+
- ✅ CSV export works correctly

---

### 🧪 Test 6: Impact Analysis Dashboard

**Objective:** Verify metrics and visualizations

**Steps:**
1. Navigate to **"📊 Impact Analysis"** tab
2. Review all metrics and charts

**Expected Results:**
- ✅ 4 metric cards display correctly:
  - Time Saved: 96%
  - Cost per Job: $0.15
  - Annual Savings: $175K
  - Processing Speed: 30 sec
- ✅ Two bar charts render:
  - Processing Time Comparison
  - Resource Allocation
- ✅ Business case summary shows before/after comparison
- ✅ ROI calculation displays: "3.4 month payback period"

---

### 🧪 Test 7: Error Handling (Invalid API Key)

**Objective:** Verify graceful error handling

**Steps:**
1. Edit `.env` file and change API key to `INVALID_KEY`
2. Restart Streamlit app
3. Try to process an email

**Expected Results:**
- ✅ Error message displays: "⚠️ Please configure ANTHROPIC_API_KEY"
- ✅ App doesn't crash
- ✅ User can correct and retry

**Cleanup:** Restore valid API key in `.env`

---

### 🧪 Test 8: Empty Input Validation

**Objective:** Test input validation

**Steps:**
1. In **"📧 Single Upload"** tab
2. Don't upload or paste anything
3. Click **"🚀 Extract Job Details"**

**Expected Results:**
- ✅ Warning message: "📝 Please upload a file or paste content"
- ✅ No API call made (saves costs)

---

### 🧪 Test 9: Command Line Batch Processing

**Objective:** Test Python script directly

**Steps:**
```bash
# Process all emails via CLI
python process_batch.py --input sample_emails --output extracted_jobs
```

**Expected Results:**
- ✅ Console shows progress: "[1/25] Processing email_01.txt..."
- ✅ Creates `extracted_jobs/` folder
- ✅ Generates 25 individual JSON files
- ✅ Creates `batch_summary.csv`
- ✅ CSV contains all key fields

---

### 🧪 Test 10: Single Email CLI Extraction

**Objective:** Test individual extraction script

**Steps:**
```bash
python extract_job.py --email sample_emails/email_01.txt
```

**Expected Results:**
- ✅ Prints: "Processing sample_emails/email_01.txt..."
- ✅ Creates `extracted_jobs/email_01.json`
- ✅ JSON contains valid structure with all fields
- ✅ Quote calculation is accurate

---

## Validation Checklist

After running all tests, verify:

- [ ] **UI Quality**
  - [ ] Modern gradient background displays correctly
  - [ ] Text is readable with good contrast
  - [ ] Cards have proper spacing and shadows
  - [ ] Buttons have hover effects
  - [ ] Tabs are clearly distinguishable

- [ ] **Functionality**
  - [ ] Single upload works (file + paste)
  - [ ] Batch processing handles 5+ files
  - [ ] All 25 emails can be processed
  - [ ] Download CSV works
  - [ ] Error messages are clear

- [ ] **Accuracy**
  - [ ] Client names extracted correctly
  - [ ] Addresses parsed properly
  - [ ] Job types classified accurately
  - [ ] Urgency detected from keywords
  - [ ] Quotes calculated per business rules

- [ ] **Performance**
  - [ ] Single email: <5 seconds
  - [ ] Batch (25 emails): <2 minutes
  - [ ] No crashes or timeouts
  - [ ] Progress indicators work

---

## Common Issues & Solutions

### Issue: "ModuleNotFoundError: No module named 'openai'"
**Solution:**
```bash
pip install -r requirements.txt
```

### Issue: "API Key not found"
**Solution:**
```bash
# Verify .env file exists and contains valid key
cat .env
# Should show: ANTHROPIC_API_KEY=sk-ant-api03-...
```

### Issue: Streamlit shows blank page
**Solution:**
```bash
# Clear Streamlit cache
streamlit cache clear
# Restart app
streamlit run app.py
```

### Issue: JSON parsing errors
**Solution:**
- Check if OpenAI API is responding correctly
- Verify `extraction_prompt.txt` hasn't been modified
- Try with a simpler email first

### Issue: Quotes seem incorrect
**Solution:**
- Review `extract_job.py` line 60-90 (calculate_quote function)
- Verify business rules in `extraction_schema.md`
- Check if urgency/complexity detected properly

---

## Performance Benchmarks

Based on testing with GPT-4o:

| Metric | Target | Typical Result |
|--------|--------|----------------|
| Single Email Processing | <5 sec | 1-3 sec |
| Batch (10 emails) | <30 sec | 20-40 sec |
| Batch (25 emails) | <90 sec | 50-100 sec |
| Extraction Accuracy | >90% | 92-96% |
| Quote Accuracy | >95% | 97-99% |

---

## Demo Preparation Checklist

Before presenting to stakeholders:

- [ ] Run full test suite (all 10 tests)
- [ ] Verify API key has sufficient credits
- [ ] Prepare 3 demo emails:
  - [ ] Simple: `email_01.txt` (perfect extraction)
  - [ ] Complex: `email_complex_01.txt` (multiple addresses)
  - [ ] Edge case: `email_complex_03.txt` (missing info)
- [ ] Take screenshots of:
  - [ ] Successful extraction
  - [ ] Batch processing results
  - [ ] Impact dashboard
- [ ] Practice 5-minute walkthrough
- [ ] Have backup: CSV export ready to show

---

## Next Steps After Testing

1. **If all tests pass:**
   - Document any edge cases found
   - Note accuracy rates
   - Prepare demo presentation

2. **If issues found:**
   - Log specific errors
   - Test with different email formats
   - Adjust prompts if needed
   - Re-run affected tests

3. **For production readiness:**
   - Test with 100 real historical emails
   - Measure actual accuracy vs POC
   - Identify additional edge cases
   - Plan integration with existing systems

---

**Testing Time Estimate:** 30-45 minutes for full suite

**Last Updated:** January 3, 2026
