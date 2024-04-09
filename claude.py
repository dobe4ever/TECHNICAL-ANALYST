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
1, read:
Read the technical data shown in the provided chart. Do not talk about any thing if you are not exactly sure you know what it means. Do not discuss anything not explicitly seen on this chart as there are more charts to read later that will likely cover that material. Do not leave any details un-narrated as some of your viewers are vision-impaired, so if you don't narrate everything specifically they won't know. Use excruciating detail.

2, interpret:
Draw upon your deep understanding of technical analysis concepts, principles, and indicators to generate a comprehensive assessment of the asset's price action, trends, and potential future behavior. 

3, recap:
Finish with a bullet list of the key points.

4, recommendations:
Recommended trading strategies for different traders with different personal situations. 
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
            # model="claude-3-haiku-20240307",
            model="claude-3-sonnet-20240229",
            # model="claude-3-opus-20240229",
            max_tokens=3000,
            temperature=0.2,
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

