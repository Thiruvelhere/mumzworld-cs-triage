import json, os, time
from openai import OpenAI
from schema import TriageResult
from prompts import SYSTEM_PROMPT, FEW_SHOT_EXAMPLES
from pydantic import ValidationError
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(
    base_url='http://localhost:11434/v1',
    api_key='ollama'
)

def build_messages(email_text: str) -> list:
    messages = [{'role': 'system', 'content': SYSTEM_PROMPT}]
    for ex in FEW_SHOT_EXAMPLES:
        messages.append({'role': 'user', 'content': ex['input']})
        messages.append({'role': 'assistant',
            'content': json.dumps(ex['output'], ensure_ascii=False)})
    messages.append({'role': 'user', 'content': email_text})
    return messages

def triage_email(email_text: str) -> dict:
    messages = build_messages(email_text)

    for attempt in range(3):
        try:
            response = client.chat.completions.create(
                model='llama3.1:8b',
                messages=messages,
                temperature=0.1
            )
            break
        except Exception as e:
            print(f"  Error on attempt {attempt+1}/3: {str(e)[:100]}")
            time.sleep(3)
    else:
        return {'error': 'All attempts failed', 'validation_failed': True}

    raw = response.choices[0].message.content

    # strip markdown code fences if model wraps JSON in ```json ... ```
    if '```' in raw:
        raw = raw.split('```')[1]
        if raw.startswith('json'):
            raw = raw[4:]

    try:
        parsed = json.loads(raw)
        result = TriageResult(**parsed)
    except (json.JSONDecodeError, ValidationError) as e:
        return {
            'error': str(e),
            'raw_output': raw,
            'validation_failed': True
        }

    if result.confidence and result.confidence < 0.5:
        result.intent = 'escalate'

    if result.out_of_scope:
        result.reply_en = None
        result.reply_ar = None

    return result.model_dump()