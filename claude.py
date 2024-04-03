import anthropic

# Defaults to os.environ.get("ANTHROPIC_API_KEY")
client = anthropic.Anthropic()


def is_chart(encoded_image, media_type):
    if encoded_image:
        message = client.messages.create(
            model="claude-3-haiku-20240307",
            max_tokens=10,
            temperature=0,
            system="<context>\nImage classification\n</context>\n\n<task>\nOnly respond \"YES\" or \"NO\" (Without quotes)\n\nIs the image provided one of the following charts:\n\nCandlestick\nBar\nLine\nPoint and Figure\nRenko\nKagi\nEquivolume\nTick\nA chart where technical analysis can be performed\n</task>",
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "image",
                            "source": {
                                "type": "base64",
                                "media_type": media_type,
                                "data": encoded_image
                            }
                        }
                    ]
                }
            ]
        )
        response = message.content[0].text
        print(response)
        return str(response)
    else:
        return "No image uploaded."

def analyze_img(encoded_image, media_type):
    if encoded_image:
        message = client.messages.create(
            model="claude-3-haiku-20240307",
            # model="claude-3-sonnet-20240229",
            # model="claude-3-opus-20240229",
            max_tokens=2500,
            temperature=0,
            system="<context>Technical analysis</context>\n\ntask>Your task is to analyze the chart provided and write a comprehensive assessment based solely on technical analysis, without considering any information other than what's visible on the chart.</task>",
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "image",
                            "source": {
                                "type": "base64",
                                "media_type": media_type,
                                "data": encoded_image
                            }
                        }
                    ]
                }
            ]
        )
        response = message.content[0].text
        return str(response)
    else:
        return "No image uploaded."

