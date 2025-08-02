import time

def send_prompt_with_retry(client, prompt_text, idx, max_retries=5):
    refusal_count = 0
    antwort = ""
    refusal_detected = False

    while refusal_count < max_retries:
        try:
            response = client.responses.create(
                model="gpt-4o",
                input=[{"role": "user", "content": [{"type": "input_text", "text": prompt_text}]}]
            )

            if hasattr(response, "output") and response.output:
                first_output = response.output[0]

                if isinstance(first_output, dict) and first_output.get("type") == "refusal":
                    refusal_count += 1
                    print(f"--- Verweigerung (Versuch {refusal_count}) in Zeile {idx} ---")
                    print(first_output.get("refusal", "[Keine Nachricht vom Modell]"))
                    time.sleep(2)
                    continue

                else:
                    antwort = response.output_text.strip()
                    print(f"--- Antwort von ChatGPT für Zeile {idx} ---")
                    print(antwort)
                    return antwort, False

            else:
                antwort = response.output_text.strip()
                print(f"--- Antwort (Fallback) von ChatGPT für Zeile {idx} ---")
                print(antwort)
                return antwort, False

        except Exception as e:
            refusal_count += 1
            print(f"--- Fehler bei Zeile {idx} (Versuch {refusal_count}) ---")
            print(str(e))
            time.sleep(2)

    print(f"Abbruch nach {max_retries} Verweigerungen bei Zeile {idx}")
    return "[Refused after 5 attempts]", True
