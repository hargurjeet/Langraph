# Agent Based Search Using LangGraph

This repository contains a Streamlit application that utilizes AI agents to perform web searches and display the results. The application is built using the LangGraph library, LangChain, and Streamlit.

## Features

- Accepts user text input for queries.
- Uses AI agents to process the input and perform web searches.
- Displays the final output and detailed processing steps.
- Customizable UI with Streamlit.

## Installation

1. Clone the repository:
    ```sh
    git clone https://github.com/yourusername/Langraph.git
    cd Langraph
    ```

2. Create a virtual environment and activate it:
    ```sh
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. Install the required packages:
    ```sh
    pip install -r requirements.txt
    ```

4. Set up environment variables:
    - Create a `.env` file in the root directory of the project.
    - Add your API keys to the `.env` file:
        ```env
        OPENAI_API_KEY=your_openai_api_key
        TAVILY_API_KEY=your_tavily_api_key
        ```

## Usage

1. Run the Streamlit application:
    ```sh
    streamlit run app.py
    ```

2. Open your web browser and go to `http://localhost:8501`.

3. Enter your query in the text area and click the "Search with Agents" button.

## Project Structure

- `app.py`: The main Streamlit application file.
- `requirements.txt`: The list of required Python packages.
- `experiments.ipynb`: Jupyter notebook with experiments and examples of using LangGraph and LangChain.

## Example Queries

- "What is the weather in San Francisco?"
- "Who won the Super Bowl in 2024? In what state is the winning team headquarters located? What is the GDP of that state?"

## Detailed Processing

The application uses the following steps to process user input:

1. **Initialize AI Agent**: An AI agent is initialized with the `TavilySearchResults` tool and a prompt.
2. **Process User Input**: The user input is processed by the AI agent.
3. **Invoke Graph**: The AI agent's graph is invoked with the processed messages.
4. **Display Results**: The final output and detailed processing steps are displayed in the Streamlit app.

## Customization

You can customize the application by modifying the following sections in `app.py`:

- **Prompt**: Update the prompt to change the behavior of the AI agent.
- **Tools**: Add or remove tools used by the AI agent.
- **UI**: Customize the Streamlit UI using custom CSS or additional Streamlit components.

## Contributing

Contributions are welcome! Please open an issue or submit a pull request for any improvements or bug fixes.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
