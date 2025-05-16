<h1 align="center">GTA: Graph Theory Agent and Benchmark for Algorithmic Graph Reasoning with LLMs</h1>

## Introduction

This repository provides partial datasets and the automated code for generating graph problem instances as described in the paper "GTA: Graph Theory Agent and Benchmark for Algorithmic Graph Reasoning with LLMs." Our work introduces **GT Bench**, a challenging new benchmark featuring 44 diverse graph problem types designed to evaluate the ability of LLMs to perform multi-step algorithmic reasoning. We also propose the **Graph Theory Agent (GTA)**, a novel framework that enhances LLM graph reasoning by employing an adaptive input representation selector and decomposing algorithmic solutions.

Here you will find:
*   Code to automatically generate graph problem instances for GT Bench.
*   Sample datasets used in our evaluations.

For full details on the methodology, benchmark, agent framework, and experimental results, please refer to our paper.

## Installation

To set up the environment for running the code, please follow these steps:

```bash
conda create -n gta python=3.9
conda activate gta
pip install -r requirements.txt
```

## Configuration

To use models that require API keys (e.g., OpenAI models, or models hosted on services like DeepInfra), you need to configure your credentials.

1.  Create a file named `.env` in the `utils/` directory of this project.
2.  Add the necessary API keys and credentials to this file. You only need to add keys for the models or data sources you intend to use.

Here is an example structure for your `.env` file:

```properties
# For OpenAI models
OPENAI_API_KEY=your_openai_api_key

# For models hosted on DeepInfra (if you are using it as an OpenAI-compatible endpoint)
DEEPINFRA_BASE_URL=https://api.deepinfra.com/v1/openai
DEEPINFRA_API_KEY=your_deepinfra_api_key

# Add other API keys as needed for different services
# ANOTHER_SERVICE_API_KEY=your_other_service_key
```
Make sure the `.env` file is placed in the correct `utils/` directory.

## Usage

The main scripts provided are:

*   `graph.py`: This script is used for generating the underlying graph structures based on various parameters.
*   `question.py`: This script generates the actual problem instances, which include a natural language question description and the corresponding graph structure (in one of the supported formats).
    *   You can control the number of questions generated per problem type using the `--questions` command-line argument.
    *   The scale and types of graphs generated for different tasks can be adjusted by modifying the `TASKS` configuration (likely a dictionary or list) within the `question.py` script.
*   `evaluation.py`: This script is used to evaluate the performance of different LLMs on the generated graph problems.
    *   You can control which models are evaluated by modifying the `models` list or variable within the script.
    *   You can select the input graph representation types (e.g., Natural Language, Adjacency List, Adjacency Matrix, Structured Language) for evaluation by modifying the `data_formats` list or variable within the script.

## Citation

If you use GT Bench, GTA, or the associated code in your research, please cite our paper:

```bibtex
@article{xu2025gta,
  title={GTA: Graph Theory Agent and Benchmark for Algorithmic Graph Reasoning with LLMs},
  author={Xu, Zixiang and Wang, Yanbo and Wang, Chenxi and Gao, Lang and Song, Zirui and Huang, Yue and Chen, Zhaorun and Zhang, Xiangliang and Chen, Xiuying},
  year={2025},
  note={Under review}
}
```