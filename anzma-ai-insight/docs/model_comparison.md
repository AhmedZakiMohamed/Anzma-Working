# Local Model Comparison

## 1. Test Environment

| Component | Specification |
|---|---|
| CPU | Intel Core i5-10300H, 4 cores / 8 threads |
| GPU | NVIDIA GTX 1650, 4 GB VRAM |
| System RAM | 7.9 GB |
| Runtime | Ollama v0.40.13 |
| Context size | 2048 tokens |
| API | Local Ollama API |
| Execution | Local inference |
| Interface | Python CLI and Streamlit |

Models evaluated:
- Qwen 2.5 3B (`qwen2.5:3b`)
- Llama 3.2 3B (`llama3.2:3b`)

## 2. Model Characteristics

| Metric | Qwen 2.5 3B | Llama 3.2 3B |
|---|---|---|
| Parameters | 3B | 3B |
| Quantization | Q4_K_M | Exact quantization not recorded |
| Approximate model size | 1.9 GB | Approximately 2.0 GB |

## 3. English Performance: Cold vs. Warm

The following are preliminary single-run measurements, not statistical averages.

| Measurement | Qwen 2.5 3B | Llama 3.2 3B |
|---|---:|---:|
| Cold load time | 149.06 s | 120.85 s |
| Cold generation speed | 54.77 tokens/s | 59.46 tokens/s |
| Warm load time | 0.42 s | 0.41 s |
| Warm generation speed | 57.85 tokens/s | 58.27 tokens/s |

Cold means the model was not already loaded in memory. Warm means the model was already loaded.

**Performance observations:**
- Llama loaded approximately 28.21 seconds faster in the recorded cold-start comparison.
- Warm generation speeds were very close.
- These results are preliminary and should not be treated as statistically established performance differences.
- Model loading time may also be affected by storage performance and system memory availability.

## 4. Arabic vs. English Evaluation

Both models were evaluated using English and Arabic prompts, including general explanations, project-awareness questions, and a synthetic building-security scenario.

English example:

"Explain in two sentences what an access control system is."

Arabic example:

"اشرح في جملتين ما هو نظام التحكم في الدخول."

Recorded Arabic measurements:

| Measurement | Qwen 2.5 3B | Llama 3.2 3B |
|---|---:|---:|
| Cold load time | 123.19 s | Not recorded |
| Generation speed | 54.40 tokens/s | Not recorded |

A complete four-way Arabic/English performance comparison was not recorded. Arabic token counts, consistent generation-time measurements, and time-to-first-token were not measured for both models under identical conditions.

### Language quality observations

- Qwen sometimes produced understandable Arabic, but other tests included mixed-language text, unnatural wording, and even an unexpected Chinese response.
- Llama performed well in several English tests but also produced malformed or mixed-language Arabic.
- Both models demonstrated inconsistent compliance with the requirement to answer in the same language as the question.
- Neither model was reliable enough to be considered a professional Arabic assistant without human review.

## 5. Memory and Hardware Observations

At a context size of 2048, Llama was observed using approximately 2.3 GB of GPU memory according to the recorded NVIDIA monitoring output.

At a context size of 4096, Llama required more memory and was observed running partly on CPU and partly on GPU.

Equivalent detailed memory measurements for Qwen were not recorded. Therefore, a direct memory comparison is not available.

## 6. Chatbot and Project-Awareness Evaluation

Both models were tested through the local Streamlit chatbot using the same general project context.

The tests checked:
- Whether the model could explain the purpose of Anzma AI Insight.
- Whether it could distinguish implemented features from planned features.
- Whether it could answer general AI and machine-learning questions.
- Whether it could preserve conversation context.
- Whether it followed the requested response language.

### Qwen 2.5 3B

- Produced a useful English explanation of the current prototype in one test.
- Failed to maintain English in some English-language questions.
- Produced inconsistent and sometimes corrupted Arabic.
- Correctly acknowledged that live security monitoring, anomaly detection, and dashboard integration were not implemented when explicitly asked.
- Successfully recalled the synthetic building name "Building Alpha" in a conversation-history test, although it also produced an unexpected Chinese response.

### Llama 3.2 3B

- Produced a clear English explanation of the prototype.
- Occasionally claimed that the system learns from user interactions and improves over time, which is not an implemented feature.
- Answered an AI-versus-machine-learning question more clearly in English.
- Correctly acknowledged several features that were not implemented.
- Successfully recalled "Building Alpha" in a conversation-history test.
- Also produced inconsistent and malformed Arabic responses.

These tests demonstrate that conversation history and system prompts improve behavior but do not guarantee factual accuracy or language consistency.

## 7. Practical Security Scenario

Both models were tested with the following synthetic scenario:

"A restricted door recorded three denied access attempts within five minutes. Give me three possible explanations and safe investigation steps. Do not assume a cause."

The evaluation considered:
- Identification of possible causes.
- Safe investigation recommendations.
- Clarity and organization.
- Arabic and English response quality.
- Avoidance of unsupported assumptions.

### Results

**Qwen 2.5 3B**
- Its English project explanation was generally useful.
- Its security response had language-consistency problems and included questionable or generic recommendations.
- Its Arabic security response did not provide a satisfactory investigation answer.

**Llama 3.2 3B**
- Its English security response was reasonably organized.
- It suggested possible explanations such as incorrect credentials, a jammed door, or possible tampering.
- It recommended checking access logs and CCTV, but some recommendations still required better relevance and human verification.
- Its Arabic security response failed to provide a useful answer.

All scenarios used synthetic information. Model-generated findings must be verified by a qualified and authorized human operator.

## 8. Selection Decision

**Llama 3.2 3B is the provisional default model.**

Reasons:
- It performed slightly better in the recorded English cold-start benchmark.
- Its warm generation speed was close to Qwen.
- Its English explanations and English security-scenario response were more useful overall in the latest qualitative tests.
- It demonstrated useful conversation-history recall.

Qwen 2.5 3B remains available as an alternative, particularly for further Arabic-language evaluation.

This is a preliminary engineering decision based on limited tests, not a universal model ranking. Neither model has demonstrated sufficiently reliable professional Arabic output.

## 9. Limitations and Further Testing

The following measurements remain incomplete:

- Repeated benchmark runs and statistical averages.
- Complete Arabic and English token counts for both models.
- Consistent time-to-first-token measurements.
- Equivalent RAM and VRAM measurements for both models.
- Exact Llama quantization metadata.
- More controlled Arabic quality tests.
- A controlled offline test with the network disconnected.

The recorded results should be treated as preliminary observations. The chatbot is a local prototype and does not currently provide live security monitoring, anomaly detection, dashboard integration, or direct building-device control.