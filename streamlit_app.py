import streamlit as st
import json
import requests


def main():
    prompt_id = "d27ebecc-6e11-44da-9057-9166a82af99c"
    api_key = "ww-KyaGm2qynorDsCD1HhxmuRQbJZgiChX4IrENuuhJRTxCD6aYu6MaI1"
    user_prompt = st.text_input("Enter something")
    generate_button = st.button("Generate")

    if generate_button:
        # Describe the prompt (shows just the inputs for now)
        # r1 = requests.get(f"https://app.wordware.ai/api/prompt/{prompt_id}/describe",
        #                   headers={"Authorization": f"Bearer {api_key}"})
        if(len(user_prompt)):
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
                        # We can print values as they're generated
                        # if value['type'] == 'generation':
                        #     if value['state'] == "start":
                        #         st.write("\nNEW GENERATION -", value['label'])
                        #     else:
                        #         st.write("\nEND GENERATION -", value['label'])
                        # elif value['type'] == "chunk":
                        #     st.write(value['value'], end="")
                        if value['type'] == "outputs":
                            # Or we can read from the outputs at the end
                            # Currently we include everything by ID and by label - this will likely change in future in a breaking
                            # change but with ample warning
                            st.write("\nFINAL OUTPUTS:")
                            raw_output = value["values"]["diverse_variations (new)"]
                            outputs = raw_output.split("\n")
                            for i,output in enumerate(outputs):
                                if(len(output)):
                                    outputs[i] = output.split(".",1)[1].strip()
                                    st.write(outputs[i])


if __name__ == '__main__':
    main()