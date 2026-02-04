---
name: meeting-summarizer
description: Use when you need to transcribe and summarize meeting recordings from Fireflies or local audio files, extract action items with assignees and deadlines, and send structured summaries to Slack
---

# Meeting Summarizer

Automated meeting transcription and analysis system.

## Overview

Converts audio recordings into structured meeting summaries with decisions and action items. Monitors folders for new recordings, transcribes with Whisper, analyzes with Claude, and notifies via Slack.

**Core principle:** Automate the entire pipeline from audio file to actionable summary.

## When to Use

Use this skill when:
- You have meeting recordings (mp3, m4a, wav) that need transcription
- You need to extract action items, decisions, and summaries from meetings
- You want automated processing of Fireflies exports or local recordings
- You need to send meeting summaries to Slack automatically

Do NOT use when:
- You only need simple audio transcription (use Whisper API directly)
- Meeting notes are already in text format (use Claude directly)
- You need real-time transcription during meetings (use live transcription tools)

## Core Pattern

**Before:** Manual transcription, reading through long transcripts, manually extracting action items

**After:** Drop audio file, get structured summary with action items in Slack


## Quick Reference

| Task | Command |
|------|---------|
| Process single file | `python scripts/process_meeting.py <file.mp3>` |
| Monitor folder | `python scripts/monitor_meetings.py` |
| Batch process | `python scripts/process_all.py` |
| Initialize config | `python scripts/init_config.py` |
| Test setup | `python scripts/test_setup.py` |

## Implementation

### Setup (5 minutes)

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Initialize configuration
python scripts/init_config.py

# 3. Set API keys (choose one method)
# Method A: Edit config file
nano ~/.meeting-summarizer/config.yaml

# Method B: Use environment variables
export OPENAI_API_KEY='sk-...'
export ANTHROPIC_API_KEY='sk-ant-...'
export SLACK_WEBHOOK_URL='https://hooks.slack.com/...'
```

### Configuration

Config file: `~/.meeting-summarizer/config.yaml`

```yaml
openai:
  api_key: "sk-..."

anthropic:
  api_key: "sk-ant-..."

slack:
  webhook_url: "https://hooks.slack.com/services/..."

monitoring:
  folder: "~/meeting-recordings"
  check_interval: 60

processing:
  cache_transcripts: true
  cache_dir: "~/.meeting-summarizer/cache"
```

### Processing Pipeline

```
Audio File (mp3/m4a/wav)
  ↓
Transcriber (Whisper API)
  ↓
Analyzer (Claude Sonnet 4.5)
  ↓
Notifier (Slack Webhook)
  ↓
Structured Summary
```

### Output Structure

The analyzer produces:
- **Summary**: 2-3 paragraph overview
- **Decisions**: List of key decisions made
- **Action Items**: Array of objects with:
  - `description`: What needs to be done
  - `assignee`: Who is responsible
  - `deadline`: When it's due

### Cost Optimization

- File hash deduplication prevents reprocessing
- Transcript caching saves on repeated analysis
- Batch processing mode for multiple files

**Typical costs (1 hour meeting):**
- Whisper transcription: $0.36
- Claude analysis: $0.03
- Total: ~$0.39 per meeting

## Common Mistakes

### Mistake 1: Not setting API keys
**Symptom:** "Error: OPENAI_API_KEY not set"
**Fix:** Set environment variables or edit config.yaml

### Mistake 2: Wrong audio format
**Symptom:** Transcription fails with format error
**Fix:** Whisper supports: mp3, mp4, mpeg, mpga, m4a, wav, webm

### Mistake 3: Large file timeout
**Symptom:** Transcription times out on long recordings
**Fix:** Split audio into chunks or increase timeout in transcriber.py

### Mistake 4: Slack notification fails silently
**Symptom:** Processing completes but no Slack message
**Fix:** Verify webhook URL is active, check network connectivity

### Mistake 5: Duplicate processing
**Symptom:** Same file processed multiple times
**Fix:** Enable cache_transcripts in config, check file hash logic

## Real-World Impact

**Before:** 2 hours to manually transcribe and summarize a 1-hour meeting
**After:** 3 minutes automated processing, structured output ready for distribution

**Cost:** ~$8/month for 20 meetings vs. $200+ for manual transcription services
