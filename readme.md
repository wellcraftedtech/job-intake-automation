# AI-Powered Job Intake Automation - Legal Support Services POC

## 3-Day Implementation Plan (Step-by-Step)

---

## DAY 1: DATA PREPARATION & SETUP

### Step 1: Create Sample Email Dataset (2 hours)
1. Open ChatGPT or Claude in a separate tab
2. Use this prompt to generate 20 sample emails:
   - "Generate 20 realistic legal service job request emails for an Australian legal support company. Include mix of: court document service, process service, occupancy checks, enforcement attendance. Vary formats: some structured, some unstructured in email body, some with PDF attachment references. Include client names, addresses in Sydney/Melbourne, due dates, special instructions."
3. Save each email as a separate .txt file in a folder called `/sample_emails`
4. Create 5 "complex" emails with:
   - Multiple addresses
   - Encrypted PDF mentions
   - Urgent/rush requests
   - Missing information (to test exception handling)

### Step 2: Environment Setup (1 hour)
1. Create a new folder: `rs-job-intake-poc`
2. Install Python (if not installed)
3. Create virtual environment:
   - Open terminal in your project folder
   - Create venv
4. Install required packages:
   - anthropic
   - streamlit
   - pandas
   - python-dotenv
5. Get Anthropic API key from console.anthropic.com
6. Create `.env` file and add your API key

### Step 3: Define Extraction Schema (1 hour)
1. Create a document listing all fields to extract:
   - Client name
   - Matter number (if present)
   - Job type (dropdown: Court Filing, Process Service, Occupancy Check, Enforcement, Lockout)
   - Service address
   - Defendant/Recipient name
   - Due date / SLA deadline
   - Special instructions
   - Urgency level (Normal/Urgent)
   - Number of attachments mentioned
   - Requires quote (Yes/No)
   - Estimated complexity (Low/Medium/High)
2. Create a JSON template showing the exact output format you want
3. Write business rules for auto-quoting:
   - Court Filing: $150 base
   - Process Service: $120 metro, $200 regional
   - Occupancy Check: $180
   - Urgent jobs: +50% surcharge
   - Multiple addresses: +$80 per additional

---

## DAY 2: BUILD CORE FUNCTIONALITY

### Step 4: Create Claude Extraction Prompt (2 hours)
1. Open a text editor
2. Write a detailed system prompt that:
   - Explains the context (Australian legal support company)
   - Lists all fields to extract
   - Provides examples of each job type
   - Instructs Claude to return ONLY valid JSON
   - Handles missing information (return null for missing fields)
   - Specifies date format (DD/MM/YYYY)
3. Test the prompt manually:
   - Go to claude.ai
   - Paste your prompt + 3 sample emails
   - Verify JSON output is correct
   - Refine prompt based on results
   - Save final prompt as `extraction_prompt.txt`

### Step 5: Build Simple Python Script (3 hours)
1. Create `extract_job.py` with these functions:
   - `load_email(filepath)` - reads email text file
   - `extract_with_claude(email_text, api_key)` - calls Claude API
   - `calculate_quote(job_data)` - applies pricing rules
   - `save_results(job_data, output_folder)` - saves JSON output
2. Create `process_batch.py`:
   - Loops through all emails in `/sample_emails`
   - Processes each with Claude
   - Saves results to `/extracted_jobs`
   - Creates a summary CSV with all extracted jobs
3. Test with 5 emails first
4. Fix any JSON parsing errors
5. Run on all 20 emails

### Step 6: Build Streamlit Interface (3 hours)
1. Create `app.py` with these sections:
   - **Header**: Title, description, RS branding colors
   - **Upload Section**: File uploader for .txt or .eml files
   - **Processing Section**: Button to trigger extraction
   - **Results Section**: 
     - Original email display (collapsible)
     - Extracted data in formatted cards
     - Confidence indicators
     - Auto-generated quote
   - **Metrics Dashboard**:
     - Time saved counter
     - Accuracy meter
     - Jobs processed today
2. Add simple styling with Streamlit theming
3. Test locally with `streamlit run app.py`

---

## DAY 3: POLISH & DEMO PREPARATION

### Step 7: Create Batch Processing View (2 hours)
1. Add a second tab in Streamlit for "Batch Processing"
2. Allow upload of multiple emails at once
3. Show processing progress bar
4. Display results in a data table with:
   - Email subject
   - Extracted client name
   - Job type
   - Due date
   - Quote amount
   - Status (Ready / Needs Review)
5. Add "Export to CSV" button
6. Add "Exception Queue" tab showing jobs needing human review

### Step 8: Add Metrics Dashboard (2 hours)
1. Create a third tab called "Impact Analysis"
2. Show comparison metrics:
   - **Before AI**: 3 FTEs × 5 mins/job × 125 jobs = 10.4 hours/day
   - **After AI**: 0.5 FTE × 1 min/review × 25 exceptions = 0.4 hours/day
   - **Time Saved**: 96% reduction
   - **Annual Cost Saving**: Calculate based on $70k/FTE
3. Add visual charts:
   - Bar chart: Manual vs AI processing time
   - Pie chart: Job type distribution
   - Line chart: Accuracy over time (simulate data)
4. Show ROI calculation:
   - Implementation cost: $X
   - Annual savings: $Y
   - Payback period: Z months

### Step 9: Prepare Demo Script (2 hours)
1. Write a 10-minute demo script with these beats:
   - **Problem** (2 min): Show email inbox chaos, explain manual process
   - **Solution** (3 min): Upload email, click extract, show results
   - **Batch Processing** (2 min): Process 10 emails instantly
   - **Impact** (2 min): Show metrics dashboard
   - **Scale Story** (1 min): "This is just Legal Services. Imagine across all 7 service lines..."
2. Prepare 3 demo emails:
   - One simple, perfect extraction
   - One complex with multiple addresses
   - One with missing info → shows exception handling
3. Record a practice run, time yourself
4. Create backup screenshots in case of demo failure

### Step 10: Deploy & Share (2 hours)
1. Push code to GitHub (create public repo)
2. Deploy to Streamlit Cloud:
   - Go to share.streamlit.io
   - Connect GitHub repo
   - Deploy app
   - Get public URL
3. Create a simple landing page (optional):
   - Problem statement
   - Live demo link
   - Key metrics
   - "Book a call" CTA
4. Prepare handoff materials:
   - Link to live demo
   - PDF of metrics dashboard
   - Sample extracted jobs CSV
   - 2-minute explainer video (record your screen)

---

## BONUS: QUICK WINS TO ADD IF TIME PERMITS

### Optional Enhancements (Pick 1-2 if ahead of schedule)

**Enhancement 1: Email Auto-Classification** (1 hour)
- Before extraction, classify email as:
  - Valid job request
  - Quote request only
  - Inquiry/question
  - Spam/irrelevant
- Show classification confidence score

**Enhancement 2: Agent Allocation Suggestion** (1 hour)
- Create a simple agent database (5 agents with locations/specialties)
- After extraction, suggest best agent based on:
  - Job location (nearest agent)
  - Job type (agent specialty)
  - Current workload (random for POC)

**Enhancement 3: Client Portal Preview** (1.5 hours)
- Add a "Client View" tab
- Show what the client would see:
  - Job status: Received → Processing → Assigned
  - Assigned agent details
  - Estimated completion date
  - Real-time updates (simulated)

**Enhancement 4: Audit Trail** (1 hour)
- Log every extraction with timestamp
- Show what was auto-extracted vs manually reviewed
- Create compliance report format

---

## FINAL CHECKLIST BEFORE DEMO

- [ ] All 20 sample emails process without errors
- [ ] Demo runs smoothly in under 10 minutes
- [ ] Metrics show clear ROI (>90% time savings)
- [ ] Live URL works on mobile and desktop
- [ ] Backup screenshots ready
- [ ] GitHub repo is public and well-documented
- [ ] API key is in environment variable (not hardcoded)
- [ ] Error handling works (try uploading invalid file)
- [ ] "Exception queue" shows appropriate edge cases
- [ ] Quote calculations are accurate and documented

---

## DEMO DAY PRESENTATION STRUCTURE

### Opening (2 min)
- "RS processes 14,500 legal service jobs per year"
- "Currently requires 3 full-time staff just for job loading"
- "80% of jobs arrive as unstructured emails"
- "Let me show you how AI can automate this..."

### Live Demo (5 min)
1. Show sample email (messy, unstructured)
2. Upload to interface
3. Click "Extract Job Details"
4. Show extracted structured data
5. Show auto-generated quote
6. Process batch of 10 emails
7. Show exception queue

### Impact Analysis (2 min)
- Show metrics dashboard
- Highlight 96% time reduction
- Annual cost savings calculation
- "This is just one service line..."

### Scaling Vision (1 min)
- "Same AI, 7 service lines"
- "60,000+ jobs per year across RS"
- "Foundation for broader transformation"
- "Ready to build full POC with your actual data"

---

## TOOLS & RESOURCES NEEDED

- Anthropic API account (free tier is fine for POC)
- Python 3.10+
- Text editor (VS Code recommended)
- GitHub account
- Streamlit Cloud account (free)
- ChatGPT/Claude access for generating sample data
- 3 days of focused time (6-8 hours per day)

---

## PROJECT STRUCTURE

```
rs-job-intake-poc/
│
├── .env                          # API keys (DON'T COMMIT)
├── .gitignore                    # Ignore .env and venv
├── requirements.txt              # Python dependencies
├── README.md                     # Project documentation
│
├── app.py                        # Main Streamlit application
├── extract_job.py                # Core extraction logic
├── process_batch.py              # Batch processing script
├── extraction_prompt.txt         # Claude system prompt
│
├── sample_emails/                # Input test data
│   ├── email_001.txt
│   ├── email_002.txt
│   └── ...
│
├── extracted_jobs/               # Output JSON files
│   ├── job_001.json
│   ├── job_002.json
│   └── ...
│
├── assets/                       # Images, logos, etc.
│   └── rs_logo.png
│
└── docs/                         # Documentation
    ├── demo_script.md
    ├── metrics_analysis.md
    └── roi_calculation.xlsx
```

---

## QUICK START COMMANDS

### Initial Setup
```bash
# Create project folder
mkdir rs-job-intake-poc
cd rs-job-intake-poc

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On Mac/Linux:
source venv/bin/activate

# Install dependencies
pip install anthropic streamlit pandas python-dotenv

# Create requirements.txt
pip freeze > requirements.txt

# Create .env file
echo "ANTHROPIC_API_KEY=your_key_here" > .env
```

### Running the POC
```bash
# Single email extraction
python extract_job.py --email sample_emails/email_001.txt

# Batch processing
python process_batch.py --input sample_emails/ --output extracted_jobs/

# Launch Streamlit interface
streamlit run app.py
```

### Deployment
```bash
# Initialize git
git init
git add .
git commit -m "Initial commit: RS Job Intake POC"

# Create GitHub repo and push
git remote add origin https://github.com/your-username/rs-job-intake-poc.git
git push -u origin main

# Deploy to Streamlit Cloud
# Go to share.streamlit.io and follow the wizard
```

---

## SAMPLE JSON OUTPUT SCHEMA

```json
{
  "extraction_metadata": {
    "timestamp": "2026-01-03T14:30:00Z",
    "model": "claude-sonnet-4-20250514",
    "confidence": 0.95,
    "processing_time_ms": 1247
  },
  "job_details": {
    "client_name": "ABC Legal Services",
    "matter_number": "MAT-2024-1234",
    "job_type": "process_service",
    "service_address": {
      "street": "123 George Street",
      "suburb": "Sydney",
      "state": "NSW",
      "postcode": "2000"
    },
    "defendant_name": "John Smith",
    "due_date": "15/01/2026",
    "special_instructions": "Ring doorbell twice, leave with occupant only",
    "urgency": "normal",
    "attachments_mentioned": 2,
    "requires_quote": false,
    "complexity": "low"
  },
  "auto_quote": {
    "base_price": 120.00,
    "surcharges": {
      "urgency": 0.00,
      "complexity": 0.00,
      "additional_addresses": 0.00
    },
    "total": 120.00,
    "currency": "AUD"
  },
  "processing_status": {
    "auto_approved": true,
    "requires_review": false,
    "exception_reason": null,
    "suggested_agent": "Agent_042_Sydney_Metro"
  }
}
```

---

## KEY METRICS TO TRACK

### Operational Metrics
- **Extraction Accuracy**: % of fields correctly extracted
- **Auto-Approval Rate**: % of jobs requiring no human review
- **Processing Time**: Average time per email (target: <30 seconds)
- **Exception Rate**: % of jobs sent to exception queue

### Business Impact Metrics
- **Time Saved**: Hours per day saved
- **Cost Reduction**: Annual FTE cost savings
- **Throughput Increase**: Jobs processed per day increase
- **Error Reduction**: % decrease in manual data entry errors

### Quality Metrics
- **Field Completeness**: % of required fields populated
- **Quote Accuracy**: % of auto-quotes accepted by clients
- **SLA Compliance**: % of jobs processed within SLA
- **Client Satisfaction**: NPS or CSAT score (if collecting feedback)

---

## EXPECTED RESULTS

### Before AI Implementation
- **Job Loading Time**: 5 minutes per job
- **Daily Capacity**: 125 jobs (3 FTEs × 8 hours)
- **Annual Cost**: ~$210,000 (3 FTEs × $70k)
- **Error Rate**: ~8-12% manual entry errors
- **After-Hours Coverage**: None

### After AI Implementation
- **Job Loading Time**: 30 seconds per job (automated)
- **Review Time**: 1 minute per exception (human)
- **Daily Capacity**: Unlimited (auto-scaling)
- **Annual Cost**: ~$35,000 (0.5 FTE + API costs)
- **Error Rate**: <2% (AI extraction errors)
- **After-Hours Coverage**: 24/7 automated processing

### ROI Calculation
- **Annual Savings**: $175,000
- **Implementation Cost**: ~$50,000 (POC + full build)
- **Payback Period**: 3.4 months
- **3-Year NPV**: $475,000

---

## TROUBLESHOOTING GUIDE

### Common Issues & Solutions

**Issue**: Claude returns malformed JSON
- **Solution**: Add more explicit formatting instructions in prompt
- **Solution**: Use JSON schema validation in post-processing
- **Solution**: Implement retry logic with error feedback to Claude

**Issue**: Date parsing errors
- **Solution**: Standardize all dates to DD/MM/YYYY format
- **Solution**: Use dateutil.parser for flexible date parsing
- **Solution**: Add date validation step before saving

**Issue**: Address extraction inconsistent
- **Solution**: Add Australian address validation rules
- **Solution**: Use Australia Post address API for verification
- **Solution**: Flag incomplete addresses for manual review

**Issue**: API rate limits hit during batch processing
- **Solution**: Implement exponential backoff retry logic
- **Solution**: Add rate limiting (e.g., 50 requests/minute)
- **Solution**: Process in smaller batches with delays

**Issue**: Streamlit app crashes on large file uploads
- **Solution**: Add file size validation (max 5MB)
- **Solution**: Implement streaming file processing
- **Solution**: Show progress indicators for long operations

---

## NEXT STEPS AFTER POC

### Phase 1: Validation (Week 1-2)
- [ ] Test with 100 real historical emails
- [ ] Measure actual accuracy vs POC estimates
- [ ] Gather feedback from RS operations team
- [ ] Identify edge cases not covered in POC

### Phase 2: Enhancement (Week 3-4)
- [ ] Integrate with AIMS system (read-only)
- [ ] Add email server integration (Gmail/Outlook)
- [ ] Build agent allocation engine
- [ ] Implement proper exception workflow

### Phase 3: Pilot (Month 2)
- [ ] Deploy to production with 10% of traffic
- [ ] Run parallel with manual process
- [ ] Monitor accuracy and exceptions daily
- [ ] Train operations team on review workflow

### Phase 4: Scale (Month 3)
- [ ] Roll out to 100% of Legal Services jobs
- [ ] Extend to Field Services (similar workflow)
- [ ] Build analytics dashboard
- [ ] Document lessons learned

### Phase 5: Expand (Month 4-6)
- [ ] Apply same pattern to Repossessions
- [ ] Apply same pattern to Audits
- [ ] Implement cross-service-line analytics
- [ ] Build unified job intake platform

---

## SUCCESS CRITERIA

### POC Success Metrics
- ✅ Processes 20/20 sample emails without crashes
- ✅ Extraction accuracy >85% on structured fields
- ✅ Demo runs in <10 minutes
- ✅ Clear ROI shown (>90% time savings)
- ✅ Client expresses interest in full build

### Production Success Metrics (Post-POC)
- 📊 Extraction accuracy >95% on real emails
- 📊 Auto-approval rate >80%
- 📊 Exception review time <2 min per job
- 📊 Zero data loss or security incidents
- 📊 Operations team satisfaction score >8/10

---

## CONTACT & SUPPORT

### For Technical Questions
- Review Anthropic documentation: docs.anthropic.com
- Check Streamlit docs: docs.streamlit.io
- Search GitHub issues in similar projects

### For Business Questions
- Refer to RS Transformation Overview briefing pack
- Review KMC proposal document
- Contact RS stakeholders for clarification

---

**Total Time Estimate: 20-24 hours across 3 days**

**Cost: ~$5-10 in API calls (free tier covers most of it)**

**Deliverables:**
1. ✅ Working demo URL
2. ✅ GitHub repository
3. ✅ Metrics dashboard
4. ✅ Sample extracted jobs dataset
5. ✅ Demo video/screenshots
6. ✅ ROI calculation document

---

*Document Version: 1.0*  
*Last Updated: January 3, 2026*  
*Created for: RS Legal Support Services AI Automation POC*