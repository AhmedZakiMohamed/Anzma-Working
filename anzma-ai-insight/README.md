# Anzma Tech – Anzma AI Insight

**A Local Bilingual AI Chatbot Powered by Ollama**

## 1. Project Overview

Anzma AI Insight is a local AI chatbot prototype developed for Anzma Tech. Its objective is to build, test, and evaluate a bilingual AI assistant capable of answering questions in Arabic and English while running language models locally through Ollama.

The project focuses on three main engineering requirements:

- **Local execution:** Run inference locally without depending on cloud AI APIs or API keys.
- **Model evaluation:** Compare two quantized language models under consistent test conditions.
- **Practical application:** Develop a Python chatbot with model selection, conversation history, and a graphical interface.

Rather than selecting a model based only on its reputation, both candidates were tested on the available hardware and evaluated for startup behavior, generation speed, language quality, conversation memory, and security-related responses.

The current implementation includes:
- A Python chatbot connected to Ollama's local API.
- A Streamlit graphical user interface.
- Model selection between Qwen 2.5 3B and Llama 3.2 3B.
- Arabic and English input.
- Conversation history.
- A system prompt designed to improve response quality and accuracy.

**Project scope:** This is a local chatbot prototype. It does not currently connect to real building devices, access-control systems, CCTV infrastructure, operational dashboards, or live security data.

## 2. Engineering Environment and Constraints

### Hardware

| Component | Specification |
|---|---|
| CPU | Intel Core i5-10300H |
| GPU | NVIDIA GTX 1650, 4 GB VRAM |
| RAM | Approximately 8 GB |
| Operating system | Windows |
| Python | 3.11.9 |
| Ollama | 0.40.13 |

### Storage Architecture

A storage constraint was identified early: the system drive had limited available space, while the E: drive had sufficient capacity.

To avoid filling the system drive, the project and model storage were organized on E:.

| Component | Location |
|---|---|
| Project directory | `E:\anzma-ai-insight` |
| Ollama installation | `E:\Ollama` |
| Model directory | `E:\ollama-models` |
| Python virtual environment | `E:\anzma-ai-insight\.venv` |

The `OLLAMA_MODELS` environment variable was configured to point to the E: drive.

This was an important deployment consideration because local language models can consume several gigabytes of storage.

### Development Tools

- Python 3.11
- Git
- Visual Studio Code
- Ollama
- Requests
- Streamlit

## 3. Model Selection

Two local quantized models were selected for comparison.

| Model | Parameters | Quantization | Approximate size |
|---|---:|---|---:|
| Qwen 2.5 3B | 3B | Q4_K_M | 1.9 GB |
| Llama 3.2 3B | 3B | Local Ollama quantized build; exact quantization not recorded | 2.0 GB |

Both models were installed locally and accessed through Ollama.

The comparison used the same hardware and a context setting of 2048 tokens for the initial performance benchmark.

The models were also tested using the same qualitative questions to compare their responses.

## 4. Initial Performance Benchmark: Cold vs. Warm State

The first stage of testing focused on understanding the difference between model startup time and actual generation performance.

- **Cold state:** The model was not already loaded in memory. The first request included model-loading overhead.
- **Warm state:** The model was already loaded, so the next request measured generation with substantially less startup overhead.

### English Benchmark Results

Test prompt:

> Explain in two sentences what an access control system is.

Context setting: 2048 tokens.

API method: Ollama `/api/generate`, with streaming disabled.

| Metric | Llama 3.2 3B | Qwen 2.5 3B |
|---|---:|---:|
| Cold model load | 120.85 s | 149.06 s |
| Cold generation speed | 59.46 tokens/s | 54.77 tokens/s |
| Warm model load | 0.41 s | 0.42 s |
| Warm generation speed | 58.27 tokens/s | 57.85 tokens/s |

### Initial Observations

1. Llama loaded approximately 28 seconds faster in the recorded cold-start test.
2. Llama achieved a higher cold generation rate in this test.
3. Once loaded, both models generated responses at very similar speeds.
4. Warm model loading was negligible compared with cold startup.

These results show why startup latency and generation throughput should be evaluated separately.

The measurements are preliminary single-run observations, not statistically averaged benchmark results.

## 5. Arabic vs. English Performance

The next stage investigated whether both models could handle Arabic and English effectively.

Example English prompt:

> Explain in two sentences what an access control system is.

Example Arabic prompt:

> اشرح في جملتين ما هو نظام التحكم في الدخول.

The purpose was to evaluate both generation performance and language quality.

### Recorded Language-Related Measurements

| Test | Model | Cold load | Generation speed |
|---|---|---:|---:|
| English | Llama 3.2 3B | 120.85 s | 59.46 tokens/s |
| English | Qwen 2.5 3B | 149.06 s | 54.77 tokens/s |
| Arabic | Qwen 2.5 3B | 123.19 s | 54.40 tokens/s |
| Arabic | Llama 3.2 3B | Not recorded | Not recorded |

**Measurement limitation:** The Arabic and English tests were not fully captured as a four-way benchmark. A matching Arabic benchmark record for Llama and a warm Arabic benchmark record for Qwen were not retained. Exact generated token counts for each response were also not retained.

Therefore, these figures should be treated as recorded generation throughput, not as a complete Arabic-versus-English token-count comparison.

### Language Quality Observations

Speed alone was insufficient to select the best model.

- Qwen initially produced some understandable Arabic, although responses were sometimes awkward or technically weak.
- Llama performed better in the tested English technical explanation.
- Both models produced mixed-language and malformed Arabic in later application tests.
- Both models sometimes failed to follow the requested response language.
- UTF-8 request encoding was configured to support Arabic input and output.

This helped distinguish two separate engineering concerns: correct text encoding and the underlying model's Arabic generation quality.

## 6. Python Application Development

After establishing the initial model comparison, the chatbot application was developed in Python.

The implementation communicates with Ollama through its local HTTP API rather than a cloud AI service.

### Application Architecture

1. The user starts the local Ollama server.
2. The user launches the chatbot interface.
3. The user selects a model.
4. The application sends the selected model and conversation history to Ollama.
5. Ollama generates a response locally.
6. The application displays the response and maintains conversation history.

### Application Components

| File | Purpose |
|---|---|
| `chatbot.py` | Chatbot logic, model configuration, system prompt, and local API communication |
| `app.py` | Streamlit graphical interface |
| `requirements.txt` | Python dependencies |
| `start-ollama.ps1` | Starts Ollama with the configured local model directory |
| `README.md` | Installation, usage, and project documentation |
| `docs/model_comparison.md` | Detailed model benchmark and evaluation results |

### Main Technologies

- Python 3.11
- Requests
- Streamlit
- Ollama
- Local HTTP endpoint: `http://localhost:11434/api/chat`
- UTF-8 input/output handling

### Model Selection

The application allows users to choose either model without changing the source code:

```python
MODELS = {
    "1": "qwen2.5:3b",
    "2": "llama3.2:3b"
}
```

### Local API Communication

The chatbot sends the conversation to Ollama using the following approach:

```python
payload = {
    "model": model,
    "messages": conversation,
    "stream": False,
    "options": {
        "num_ctx": 2048
    }
}

response = requests.post(
    "http://localhost:11434/api/chat",
    json=payload,
    timeout=300
)

response.raise_for_status()
result = response.json()
answer = result["message"]["content"]
```

### Application Features

- Interactive model selection.
- Arabic and English input.
- Conversation history.
- System prompt instructions.
- UTF-8 support.
- Local Ollama communication.
- Connection and timeout error handling.
- Conversation clearing in the graphical interface.
- Command-line chatbot alternative.

## 7. Streamlit Graphical Interface

A graphical interface was added using Streamlit to make the project easier to demonstrate and use.

The interface includes:

- An application title and description.
- A model-selection menu.
- A chat input field.
- User and assistant message display.
- A conversation history.
- A clear-conversation button.
- A loading indicator while the model generates a response.
- Error messages when Ollama is unavailable or a request fails.

The Streamlit application communicates with the same local Ollama server used by the command-line chatbot.

### Running the Interface

The Ollama server must be running before launching Streamlit.

Start Ollama:

```powershell
.\start-ollama.ps1
```

Then launch Streamlit in a separate PowerShell window:

```powershell
python -m streamlit run app.py
```

Open the local application in a browser:

`http://localhost:8501`

Streamlit provides the graphical interface, while Ollama remains responsible for running the models locally.

## 8. System Prompt Engineering and Iterative Improvement

The first implementation used a security-focused system prompt.

Testing revealed that prompt instructions and model behavior both influenced response quality.

For example, the assistant sometimes answered general questions with unnecessary security-related information because the original prompt strongly specialized it in physical security.

Arabic tests also revealed that asking a model to respond in Arabic was not enough to guarantee natural Arabic output.

### Problems Identified

- Mixing English technical terms into Arabic sentences.
- Producing malformed or incomplete Arabic words.
- Giving generic or repetitive recommendations.
- Inventing technical details.
- Failing to distinguish possible causes from confirmed causes.
- Over-specializing answers when the user asked a general question.
- Claiming features that the application does not implement.

### Prompt Improvement Objectives

The system prompt was revised to include explicit language and answer-quality instructions.

The updated instructions aim to:

1. Detect the language of the user's message.
2. Respond in the same language.
3. Use clear, professional Modern Standard Arabic for Arabic questions.
4. Avoid unnecessary English words in Arabic sentences.
5. Avoid inventing facts, system features, or incidents.
6. Distinguish possible causes from confirmed causes.
7. Recommend safe and authorized investigation steps.
8. Use previous conversation messages when answering follow-up questions.
9. Admit when information is not available in the conversation.
10. Avoid claiming that the chatbot learns from user interactions or improves automatically.

The prompt also clarifies that real-time monitoring, anomaly detection, dashboard integration, and direct building-device connections are not implemented.

### Important Engineering Observation

Prompt engineering can guide model behavior, but it cannot fully compensate for limitations in the underlying language model.

The tests below demonstrate that both models still have weaknesses despite explicit language instructions.

## 9. Comparative Model Quality Evaluation

Both models were tested through the Streamlit application using the same set of questions.

The evaluation covered:

- English project explanation.
- Arabic project explanation.
- General AI and machine learning knowledge.
- Awareness of current project capabilities.
- Security-related reasoning.
- Conversation memory.

### Test Results

| Evaluation | Qwen 2.5 3B | Llama 3.2 3B |
|---|---|---|
| English project explanation | Good | Good |
| Arabic project explanation | Poor: mixed and corrupted language | Poor: mixed and corrupted language |
| AI vs. ML explanation | Answered in Arabic despite English question | Good English explanation |
| Project capability awareness | Passed | Passed |
| English security scenario | Poor language consistency and questionable advice | Reasonable suggestions, with limitations |
| Arabic security scenario | Failed | Failed |
| Conversation memory | Passed | Passed |

### Qwen 2.5 3B Observations

**Strengths:**
- Correctly described the project's basic purpose.
- Correctly identified that real-time monitoring and dashboard integration are not currently implemented.
- Remembered the test building name, Building Alpha.

**Weaknesses:**
- Answered English questions in Arabic during testing.
- Produced mixed Arabic, English, and other-language text.
- Generated malformed Arabic terminology.
- Its security investigation recommendations included questionable actions, such as resetting systems without establishing whether this was necessary.
- Its Arabic security response was not sufficiently clear or reliable.

### Llama 3.2 3B Observations

**Strengths:**
- Produced a stronger English explanation of artificial intelligence and machine learning.
- Correctly identified that advanced monitoring and dashboard features are not currently implemented.
- Remembered Building Alpha.
- Its English security response suggested reviewing access logs and authorized CCTV footage.
- Its English security response provided several plausible explanations.

**Weaknesses:**
- Produced inconsistent Arabic responses with malformed words and mixed-language sentences.
- Sometimes answered Arabic questions with English or mixed-language text.
- Its Arabic security response failed to provide a useful investigation.
- It incorrectly claimed that the chatbot learns from user interactions and improves over time. This functionality is not implemented.

### Conversation Memory Test

Both models were tested using the following sequence:

First message:

> My test building is called Building Alpha.

Follow-up:

> What is the name of my test building?

Both models successfully retrieved the name from the conversation history.

This confirms that conversation-history handling worked in these particular tests. It does not establish perfect memory across all conversations.

## 10. Model Selection Decision

**Llama 3.2 3B is the provisional default model.**

This decision is based on the latest qualitative tests and the recorded performance measurements.

Reasons:

- Stronger English technical explanations in the observed tests.
- Better English response consistency.
- More useful English security scenario response than Qwen in the tested example.
- Comparable warm generation speed to Qwen.
- Successful conversation-memory test.

Qwen 2.5 3B remains available as an alternative model and can be useful for further Arabic-language evaluation.

**Important limitation:** Neither model currently provides sufficiently consistent Arabic output for a professional bilingual deployment.

The selection is provisional and applies to this prototype and its observed test results. It does not mean Llama is universally superior.

## 11. Example Security Scenario

The application was tested using a synthetic building-security event:

> A restricted door recorded three denied access attempts within five minutes.

The expected behavior was to identify possible explanations without assuming that an intrusion had occurred.

Possible explanations include:

- An expired or unauthorized access credential.
- Incorrect access permissions.
- A card-reader or door-controller malfunction.
- A possible unauthorized access attempt.

### Expected Investigation Approach

1. Preserve the relevant access-control logs.
2. Verify timestamps and credential identifiers.
3. Review relevant camera footage where authorized.
4. Check the door reader and controller status through authorized personnel.
5. Confirm access permissions with an authorized administrator.
6. Document findings and escalate according to site procedures.

Denied access attempts alone are not proof of an intrusion.

### Observed Model Limitations

Llama provided a reasonably structured English response, but some of its suggested explanations were not strongly connected to the recorded access-denied events.

Qwen's response had language consistency and technical precision problems.

Neither model provided a satisfactory Arabic security response.

All security-related outputs must be reviewed by qualified personnel. The prototype should not be used to make autonomous security decisions.

## 12. Privacy and Local Execution

The Python application communicates with the local Ollama server through:

`http://localhost:11434`

No cloud AI API or API key is required by the Python application.

The models are stored locally on the E: drive.

The startup configuration includes:

```powershell
$env:OLLAMA_MODELS = "E:\ollama-models"
$env:OLLAMA_NO_CLOUD = "1"
```

The project is designed for local inference and does not intentionally send chatbot prompts to a cloud AI API.

**Offline verification status:** The complete disconnected-network test must still be performed and documented before claiming that offline operation has been independently verified.

The startup script also contains machine-specific paths. These paths must be adjusted when setting up the project on another computer.

## 13. Installation and Running Instructions

### Requirements

- Windows.
- Python 3.11 or a compatible version.
- Git.
- Ollama installed locally.
- Qwen 2.5 3B and Llama 3.2 3B downloaded through Ollama.
- Sufficient available memory and storage.

### Step 1: Clone the Repository

```powershell
git clone https://github.com/Amr-69/anzma-ai-insight.git
cd anzma-ai-insight
```

### Step 2: Create a Virtual Environment

```powershell
python -m venv .venv
```

Activate it:

```powershell
.\.venv\Scripts\Activate.ps1
```

### Step 3: Install Dependencies

```powershell
pip install -r requirements.txt
```

### Step 4: Configure Ollama

Install Ollama and download the required models if they are not already installed:

```powershell
ollama pull qwen2.5:3b
ollama pull llama3.2:3b
```

Configure model storage on the desired drive if necessary.

The included startup script uses the original development machine's E: drive paths. Adjust it for your environment before running it elsewhere.

### Step 5: Start Ollama

```powershell
.\start-ollama.ps1
```

Keep the Ollama server running.

### Step 6: Launch the Streamlit Application

Open another PowerShell window in the project directory, activate the virtual environment, and run:

```powershell
.\.venv\Scripts\Activate.ps1
python -m streamlit run app.py
```

Open:

`http://localhost:8501`

### Optional: Run the Command-Line Chatbot

```powershell
python chatbot.py
```

Select the desired model from the displayed menu.

## 14. GitHub Repository and Project Structure

Repository:

https://github.com/Amr-69/anzma-ai-insight

The repository contains the application source code, installation requirements, documentation, and startup configuration.

Expected project structure:

```text
anzma-ai-insight/
│
├── app.py
├── chatbot.py
├── start-ollama.ps1
├── requirements.txt
├── README.md
├── .gitignore
│
└── docs/
    └── model_comparison.md
```

Local virtual environments, downloaded model files, and temporary test files should not be committed to the repository.

## 15. Limitations and Future Improvements

This prototype has several known limitations:

- Arabic technical response quality is inconsistent.
- Models sometimes ignore the requested response language.
- Results can vary between model runs.
- Benchmark measurements are preliminary single-run observations.
- Complete Arabic and English token-count records were not retained.
- Cold startup takes significantly longer than warm inference.
- The application does not connect to real access-control hardware or company security systems.
- The models can produce incorrect or unsupported information.
- AI-generated security recommendations require human verification.
- Offline operation still requires a documented disconnected-network test.

### Potential Future Improvements

- Repeated benchmark runs with averages and standard deviations.
- Separate Arabic and English token-count and throughput measurements.
- Streaming responses to improve perceived responsiveness.
- More robust Arabic terminology evaluation.
- Automated tests for conversation memory.
- Better model-specific prompt evaluation.
- Improved error handling and application testing.
- A documented offline deployment procedure.
- Future integration with verified operational data, subject to project requirements and authorization.

## 16. Engineering Approach and Lessons Learned

The project was approached as an engineering problem rather than simply a model-installation exercise.

The work was divided into distinct stages:

1. **Environment preparation:** Establish Python, Git, Ollama, and dedicated E: drive storage.
2. **Model acquisition:** Install two comparable local models.
3. **Performance measurement:** Separate cold-start latency from warm generation speed.
4. **Language evaluation:** Test Arabic and English rather than relying on English benchmarks alone.
5. **Application development:** Build a Python interface with model selection and conversation history.
6. **Graphical interface:** Add Streamlit for a practical live demonstration.
7. **Problem diagnosis:** Investigate UTF-8 encoding and distinguish technical communication issues from model-quality issues.
8. **Prompt iteration:** Improve the system prompt based on observed failures.
9. **Comparative evaluation:** Retest both models using the same questions and synthetic security scenarios.
10. **Decision-making:** Select a provisional default model based on recorded performance and observed response quality.

The main lesson was that building a successful local AI application requires more than downloading a model. It requires controlled testing, resource management, application design, language evaluation, error diagnosis, and evidence-based model selection.

---

## Project Status

**Current status:** Local chatbot prototype implemented, Streamlit interface added, two local models installed, and preliminary performance and quality comparisons completed.

**Remaining delivery activities:**
- Final system prompt improvement and retesting.
- Final code and Git repository review.
- Offline operation verification.
- Final live demonstration.
- Final documentation and model comparison updates.