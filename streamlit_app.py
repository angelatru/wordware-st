import streamlit as st
import json
import requests

def main():
    # Initialize session state to store generated prompts
    if 'generated_prompts' not in st.session_state:
        st.session_state.generated_prompts = []

    prompt_id = "d27ebecc-6e11-44da-9057-9166a82af99c"
    api_key = "ww-KyaGm2qynorDsCD1HhxmuRQbJZgiChX4IrENuuhJRTxCD6aYu6MaI1"
    user_prompt = st.text_input("Enter something")
    generate_button = st.button("Generate")

    if generate_button and len(user_prompt):
        r = requests.post(f"https://app.wordware.ai/api/prompt/{prompt_id}/run",
                          json={
                              "inputs": {
                                  "user_generations": user_prompt
                              }
                          },
                          headers={"Authorization": f"Bearer {api_key}"},
                          stream=True
                          )

        # Ensure the request was successful
        if r.status_code != 200:
            st.write("Request failed with status code", r.status_code)
            st.write(json.dumps(r.json(), indent=4))
        else:
            for line in r.iter_lines():
                if line:
                    content = json.loads(line.decode('utf-8'))
                    value = content['value']
                    if value['type'] == "outputs":
                        raw_output = value["values"]["diverse_variations (new)"]
                        outputs = raw_output.split("\n")
                        new_prompts = []
                        for i, output in enumerate(outputs):
                            if len(output):
                                output = output.split(".", 1)[1].strip()
                                new_prompts.append(output)
                                st.write(output)
                        
                        # Append new prompts to the session state variable
                        st.session_state.generated_prompts.extend(new_prompts)

    # Display all generated prompts
    if st.session_state.generated_prompts:
        st.write("\nAll Generated Prompts:")
        for prompt in st.session_state.generated_prompts:
            st.write(prompt)

if __name__ == '__main__':
    main()
