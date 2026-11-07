# Voice workflow

1. List the lines the part needs (script template). Search `sentences.tsv` in the voice bank for each; reuse what fits.
2. Write the new lines as one tagged script, sentences separated by `<break time="0.6s"/>`, speed 1.0 (tutorials).
3. Check credits (get_current_user) and the voice (get_voice), then one create_speech_without_player request, wav 48 kHz.
   Download the file at once; record the request id, duration and sentence spans.
4. Cut every sentence at the real silence nearest HeyGen's break positions; check each cut with speech-to-text.
5. Measure word times per sentence (faster-whisper word timestamps, proportional fallback) for captions and cues.
6. Add the file (mp3), the tagged text, the spans and words to the voice bank branch, with rows in `sentences.tsv` and the
   README table. Tell MTG the credits used (about 2 per 500 characters).
