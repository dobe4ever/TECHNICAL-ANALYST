import anthropic
from utils import get_tag
from prompts import img_sys, analist_sys

# Defaults to os.environ.get("ANTHROPIC_API_KEY")
client = anthropic.Anthropic()


def img_class_asst(encoded_image, media_type):
    if encoded_image:
        r = client.messages.create(
            model="claude-3-haiku-20240307",
            max_tokens=10,
            temperature=0,
            system=img_sys,
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
        res = r.content[0].text
        if 'y' not in res: return "Only images of charts accepted. Try again."
        

def analist_asst(encoded_image, media_type):
    if encoded_image:
        an = client.messages.create(
            model="claude-3-haiku-20240307",
            # model="claude-3-sonnet-20240229",
            # model="claude-3-opus-20240229",
            max_tokens=3000,
            temperature=0.2,
            system=analist_sys,
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
        text = an.content[0].text
        # chart_details = re.search(r'<chart details>(.*?)</chart details>', text, re.DOTALL).group(1)
        # chart_analysis = re.search(r'<chart analysis>(.*?)</chart analysis>', text, re.DOTALL).group(1)
        key_chart_info = get_tag("key chart inf", text)
        expected_market_behaviour = get_tag("expected market behaviour", text)
        prediction_and_confidence = get_tag("prediction and confidence", text)
        invalidation_conditions = get_tag("invalidation conditions", text)
        final = f"{key_chart_info}{expected_market_behaviour}{prediction_and_confidence}{invalidation_conditions}"

        return final
    else:
        return "No image uploaded."


