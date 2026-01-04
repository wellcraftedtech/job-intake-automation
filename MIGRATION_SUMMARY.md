# Migration Summary: Anthropic Claude → OpenAI GPT

## What Changed

Successfully migrated the Legal Job Intake Automation POC from Anthropic's Claude API to OpenAI's GPT API.

## Files Modified

### 1. **requirements.txt**
- Replaced `anthropic` with `openai`

### 2. **.env**
- Changed `ANTHROPIC_API_KEY` to `OPENAI_API_KEY`
- **Action Required:** Add your OpenAI API key

### 3. **extract_job.py**
- Imported `OpenAI` instead of `Anthropic`
- Renamed function: `extract_with_claude()` → `extract_with_gpt()`
- Updated API call to use `client.chat.completions.create()`
- Changed model from `claude-3-5-sonnet-20240620` to `gpt-4o`
- Added `temperature=0.1` for consistent outputs

### 4. **process_batch.py**
- Updated import to use `extract_with_gpt`
- Changed API key reference to `OPENAI_API_KEY`

### 5. **app.py**
- Updated import to use `extract_with_gpt`
- Changed all API key references
- Updated UI messages: "Claude AI" → "GPT"

### 6. **TESTING_GUIDE.md**
- Updated all references from Anthropic/Claude to OpenAI/GPT
- Adjusted performance benchmarks for GPT-4o

## Next Steps

1. **Get OpenAI API Key:**
   - Go to https://platform.openai.com/api-keys
   - Create a new API key
   - Copy it to your `.env` file

2. **Update .env file:**
   ```bash
   OPENAI_API_KEY=sk-proj-YOUR_ACTUAL_KEY_HERE
   ```

3. **Restart Streamlit:**
   - Stop the current app (Ctrl+C)
   - Run: `streamlit run app.py`

4. **Test the integration:**
   - Try processing a single email
   - Verify extraction quality
   - Compare results with previous Claude outputs

## API Differences

| Feature | Claude (Before) | GPT (Now) |
|---------|----------------|-----------|
| Model | claude-3-5-sonnet-20240620 | gpt-4o |
| API Style | Messages API | Chat Completions |
| System Prompt | Separate parameter | First message with role="system" |
| Response Access | `message.content[0].text` | `response.choices[0].message.content` |
| Temperature | Not set (default) | 0.1 (for consistency) |

## Expected Performance

- **Speed:** GPT-4o is typically faster (1-3 sec vs 2-4 sec per email)
- **Accuracy:** Similar extraction quality (~92-96%)
- **Cost:** GPT-4o is generally more cost-effective
- **Rate Limits:** Check your OpenAI tier for limits

## Troubleshooting

### If you get authentication errors:
```bash
# Verify API key is set
cat .env
# Should show: OPENAI_API_KEY=sk-proj-...
```

### If extraction quality differs:
- The prompt in `extraction_prompt.txt` works for both models
- GPT-4o may format responses slightly differently
- Adjust temperature if needed (currently 0.1)

## Rollback (if needed)

To switch back to Claude:
1. Change `openai` to `anthropic` in requirements.txt
2. Rename functions back to `extract_with_claude`
3. Update API key references
4. Restore original API call structure

---

**Migration completed:** January 3, 2026  
**Status:** ✅ Ready to test
