from elevenlabs import generate

def text_to_parags(text):
    """Split text into paragraphs."""
    parags = []
    start = 0
    while start < len(text):
        # Find the next period within the max length
        end_period = text.rfind(".", start, start + 499 + 1)
        # Find the next comma within the max length (if no period)
        end_comma = text.rfind(",", start, start + 499 + 1) if end_period == -1 else -1

        # Use the closest valid delimiter
        if end_period != -1:
            end = end_period
        elif end_comma != -1:
            end = end_comma
        else:
            end = start + 499

        # Extract parag without the delimiter
        parag = text[start:end + 1]

        # Remove leading whitespace only for subsequent parags
        if start > 0:
            parag = parag.lstrip()

        parags.append(parag)

        # Update start for the next iteration
        start = end + 1

    return parags

def parags_to_speech(parags):
    """Convert paragraphs to speech and save as MP3 files."""
    mp3s = []
    for parag in parags:
        audio = generate(
            text=parag,
            voice="Bella",
            model="eleven_monolingual_v1"
        )
        mp3s.append(audio)

    # Combine all audios into one
    output_audio = b"".join(mp3s)
    return output_audio