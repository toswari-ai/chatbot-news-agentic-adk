Goals:

- provide streamlit application that utilize google ADK and LiteLLM to run inference on clarifai.com.
- it is chatbot streamlit application for news searches
- provide query 3 sample cards on top.
- side bar - models selections
- side bar - clear chat button

python env:
- use conda env name agent_312
- if not exist then create it using python=3.12
- 



Agents:

- news search agent - to search news and other queries using Google ADK
- use mcp to run the tools.
- use Litellm to be llm agent and use

References:
    - <https://github.com/Clarifai/examples/tree/main/agents/Google-ADK>
    - <https://google.github.io/adk-docs/tools/built-in-tools/#use-built-in-tools-with-other-tools>
    - <https://google.github.io/adk-docs/tools/mcp-tools/#step-1-define-your-agent-with-mcptoolset>
    - <https://google.github.io/adk-docs/tools/mcp-tools/#using-mcp-tools-in-your-own-agent-out-of-adk-web>
