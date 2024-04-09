import anthropic

# Defaults to os.environ.get("ANTHROPIC_API_KEY")
client = anthropic.Anthropic()


is_chart_prompt = """
<context> Image classification </context>

<task>
Only respond "YES" or "NO" (Without quotes)

Is the image provided one of the following charts:

-- Candlestick
-- Bar
-- Line
-- A chart where technical analysis can be performed
</task>
"""
            

# analyze_img_prompt = """
# <context> Technical analysis </context>

# <task>
# Your task is to analyze the chart provided and write a comprehensive assessment based solely on technical analysis concepts, and only considering without considering the available information visible on the given chart.
# </task> """


analyze_img_prompt = """ 
<context> 
Technical analysis & trading 
</context> 
<role> 
You are an expert technical analyst and trader, reading & interpreting charts. 
</role> 
<task> 
Based on the technical details in the provided chart, please provide a thorough technical analysis assessment of the asset's price action, trends, and potential future behavior. Draw upon your deep understanding of technical analysis concepts, principles, and indicators to generate a comprehensive evaluation. Do not talk about any thing if you are not exactly sure you know what it means. Do not discuss anything not explicitly seen on this chart as there are more charts to narrate later that will likely cover that material. Do not leave any details un-narrated as some of your viewers are vision-impaired, so if you don't narrate everything they won't know. Use excruciating detail.
</task> 
"""


def is_chart(encoded_image, media_type):
    if encoded_image:
        message = client.messages.create(
            model="claude-3-haiku-20240307",
            max_tokens=10,
            temperature=0,
            system=is_chart_prompt,
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
            max_tokens=3000,
            temperature=0.5,
            system=analyze_img_prompt,
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

