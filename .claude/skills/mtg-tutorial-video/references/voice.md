# Voice workflow

1. List the lines the part needs (script template). Search `sentences.tsv` in the voice bank for each; reuse what fits.
2. Write the new lines as one tagged script, sentences separated by `<break time="0.6s"/>`, speed 1.0 (tutorials).
3. Check credits (get_current_user) and the voice (get_voice), then one create_speech_without_player request, wav 48 kHz.
   Download the file at once; record the request id, duration and sentence spans.
4. Cut every sentence at the real silence nearest HeyGen's break positions; check each cut with speech-to-text.
5. Measure word times per sentence (faster-whisper word timestamps, proportional fallback) for captions and cues.
6. Add the file (mp3), the tagged text, the spans and words to the voice bank branch, with rows in `sentences.tsv` and the
   README table. Tell MTG the credits used (about 2 per 500 characters).

**Closing track rule (MTG, 8 Nov 2026):** a video longer than 60 seconds gets the full 51.36 s track "They Call Me MTG",
starting 51.36 s before the end, soft under speech (about -14 dB while he speaks) and ending on the last frame; a video of
60 seconds or less gets only its last line ("Let's get this crypto, wherever I go!", 48.38 s to the end of the track)
right after his last word.

**Every word in full (MTG, 28 Nov 2026: "I want everything to be said in full, no truncated words").** HeyGen's word timestamps end
0.1 to 0.5 s before the sound does, so never cut a line at its last word's end time. Cut each line at the middle of the real pause
around it in the TTS file (frames below -45 dBFS, longest run between the two lines): keep a 0.06 s tail into the silence and
a 0.04 s lead-in, fades of 8 ms only inside the silence. A line that was replaced but is still in the file counts as a neighbour.
Banked lines get the same treatment in their source take. Check before rendering: no voice span overlaps the next.
