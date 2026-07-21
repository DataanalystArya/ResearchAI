# Multi-Agent Research Assistant

## Overview

The Multi-Agent Research Assistant is an autonomous AI-powered research system designed to perform end-to-end research on any given topic. Unlike traditional chatbots that generate responses solely from pretrained knowledge, this system performs live web searches, retrieves relevant online resources, extracts meaningful information, generates comprehensive research reports, and evaluates the quality of the generated output using multiple specialized AI agents.

The project demonstrates the implementation of an Agentic AI workflow by combining Large Language Models, external tools, LangChain agents, LCEL pipelines, and shared memory into a modular and scalable architecture.

---

## Objectives

The primary objective of this project is to build an intelligent research assistant capable of:

* Performing live internet research.
* Extracting relevant information from multiple web sources.
* Generating structured research reports.
* Evaluating report quality through an automated review process.
* Demonstrating a production-oriented multi-agent AI architecture.

---

## System Architecture

The research workflow consists of four independent AI components working collaboratively.

```
User Query
     │
     ▼
Search Agent
     │
     ▼
Shared State
     │
     ▼
Reader Agent
     │
     ▼
Shared State
     │
     ▼
Writer Chain
     │
     ▼
Research Report
     │
     ▼
Critic Chain
     │
     ▼
Final Evaluated Report
```

---

## Workflow

1. The user provides a research topic.

2. The Search Agent searches the live internet using Tavily Search API and retrieves relevant websites.

3. The Reader Agent visits each website and extracts meaningful textual information using BeautifulSoup.

4. All extracted content is stored inside a shared state for communication between agents.

5. The Writer Chain processes the collected information and generates a comprehensive research report.

6. The Critic Chain evaluates the generated report, assigns a quality score, and provides improvement suggestions before returning the final output.

---

## Core Components

### Search Agent

The Search Agent is responsible for retrieving the latest information from the internet. It uses the Tavily Search API to perform real-time searches and returns structured search results containing titles, URLs, and content snippets.

---

### Reader Agent

The Reader Agent receives the URLs produced by the Search Agent and extracts complete webpage content using BeautifulSoup and the Requests library. HTML elements such as scripts, styles, navigation bars, and footers are removed to obtain clean and readable text.

---

### Writer Chain

The Writer Chain is implemented using LangChain Expression Language (LCEL). It combines all collected information and produces a detailed research report containing an introduction, analysis, findings, key insights, and conclusion.

---

### Critic Chain

The Critic Chain reviews the generated report, evaluates its quality, identifies strengths and weaknesses, assigns a score, and provides constructive feedback for improvement.

---

## Technologies Used

* Python
* LangChain
* LangChain Expression Language (LCEL)
* OpenAI API
* Tavily Search API
* BeautifulSoup4
* Requests
* python-dotenv
* Streamlit
* Rich

---

## Project Structure

```
Multi-Agent-Research-System/
│
├── agents.py
├── tools.py
├── pipeline.py
├── state.py
├── main.py
├── app.py
├── requirements.txt
├── .env
└── README.md
```

---

## Installation

Clone the repository.

```bash
git clone https://github.com/your-username/multi-agent-research-assistant.git
cd multi-agent-research-assistant
```

Create a virtual environment.

```bash
uv venv
```

Activate the environment.

**Windows**

```bash
.venv\Scripts\activate
```

**macOS/Linux**

```bash
source .venv/bin/activate
```

Install project dependencies.

```bash
uv pip install -r requirements.txt
```

Create a `.env` file.

```env
OPENAI_API_KEY=your_openai_api_key
TAVILY_API_KEY=your_tavily_api_key
```

Run the application.

```bash
streamlit run app.py
```

---

## Features

* Live web search using Tavily Search API
* Automated webpage content extraction
* Multi-Agent architecture
* Shared state management
* LCEL-based report generation
* Automated report evaluation
* Modular and scalable codebase
* Production-oriented Agentic AI workflow

---

## Future Enhancements

* PDF report generation
* Citation and reference management
* Long-term conversational memory
* Vector database integration
* Multi-language research support
* Parallel agent execution
* Authentication and user management
* Research history and report storage

---

## Learning Outcomes

This project demonstrates the practical implementation of Agentic AI by integrating Large Language Models with external tools and autonomous workflows. It showcases concepts such as tool calling, shared memory, prompt engineering, web search, web scraping, LCEL pipelines, and multi-agent collaboration in a production-style research automation system.

---

## License

This project is intended for educational and research purposes.

---

## Author

1: Arya verma
2: Ankita Meena
3: Kanishka Singh
4: Bhavya Bhardwaj
5: Pahul Kaur Luthra 

B.Tech Computer Science and Engineering

Indira Gandhi Delhi Technical University for Women (IGDTUW)
