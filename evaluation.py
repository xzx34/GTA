import os
import json
import time
from tqdm import tqdm
from utils.tool import get_chat_response
from collections import defaultdict
import concurrent.futures

def load_dataset(file_path):
    """
    Load dataset from JSON file
    
    Args:
        file_path: Path to the JSON file
    
    Returns:
        List of question items
    """
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    return data

def extract_answer(response, task_name):
    """
    Use gpt-4o-mini to extract the final answer from model's response
    
    Args:
        response: The model's response text
        task_name: The name of the task
    
    Returns:
        The extracted answer (boolean or integer depending on task)
    """
    system_message = """
    You are a helpful assistant that extracts the final answer from a model's response to a graph theory question.
    For connectivity, bipartite, eulerian path/circuit, hamiltonian path/circuit questions, extract True/False.
    For other questions like minimum cycle, maximum clique, etc., extract the numerical answer.
    Only return the final answer without any explanation or additional text.
    """
    
    user_message = f"""
    Task: {task_name}
    
    Model Response:
    {response}
    
    Extract only the final answer (True/False or a number). If the answer is not clear, make your best guess.
    """
    
    # Get the extraction from gpt-4o-mini
    extraction = get_chat_response(
        model="gpt-4o-mini",
        system_message=system_message,
        messages=[{"role": "user", "content": user_message}],
        temperature=0.1
    )
    
    # Process the extracted answer
    extraction = extraction.strip().lower()
    
    # For boolean tasks
    if task_name in ["Connectivity", "Bipartite", "Eulerian Path", "Eulerian Circuit", 
                     "Hamiltonian Path", "Hamiltonian Circuit"]:
        if "true" in extraction or "yes" in extraction:
            return True
        elif "false" in extraction or "no" in extraction:
            return False
        else:
            # If unclear, default to False
            return False
    
    # For numerical tasks
    else:
        # Try to extract a number
        for word in extraction.split():
            try:
                return int(word)
            except ValueError:
                continue
        
        # If no number found, return -1 to indicate error
        return -1

def evaluate_model(model_name, data_format, questions, max_questions=None, max_workers=5):
    """
    Evaluate a model on a set of questions with concurrent processing
    
    Args:
        model_name: Name of the model to evaluate
        data_format: Format of the data (natural, structured, matrix, list)
        questions: List of question items
        max_questions: Maximum number of questions to evaluate (for testing)
        max_workers: Maximum number of concurrent workers (default: 5)
    
    Returns:
        List of result items with model responses and correctness
    """
    system_message = ""
    
    # Limit the number of questions if specified
    if max_questions is not None:
        questions = questions[:max_questions]
    
    def process_question(question):
        # Get model response
        response = get_chat_response(
            model=model_name,
            system_message=system_message,
            messages=[{"role": "user", "content": question["prompt"]}],
            temperature=0.1
        )
        
        # Extract answer using gpt-4o-mini
        extracted_answer = extract_answer(response, question["task_name"])
        
        # Check if answer is correct
        is_correct = extracted_answer == question["answer"]
        
        # Create result item
        result_item = {
            "task_name": question["task_name"],
            "graph_type": question["graph_type"],
            "prompt": question["prompt"],
            "expected_answer": question["answer"],
            "model_response": response,
            "extracted_answer": extracted_answer,
            "is_correct": is_correct
        }
        
        return result_item
    
    results = []
    
    # Use ThreadPoolExecutor for concurrent processing
    with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
        # Submit all tasks
        future_to_question = {executor.submit(process_question, question): question for question in questions}
        
        # Process results as they complete
        for future in tqdm(concurrent.futures.as_completed(future_to_question), 
                          total=len(questions), 
                          desc=f"Evaluating {model_name} on {data_format}"):
            try:
                result = future.result()
                results.append(result)
                # Small delay to avoid overwhelming API
                time.sleep(0.1)
            except Exception as exc:
                question = future_to_question[future]
                print(f"Question '{question['task_name']}' generated an exception: {exc}")
    
    return results

def calculate_accuracy(results):
    """
    Calculate accuracy metrics for the evaluation results
    
    Args:
        results: List of result items
    
    Returns:
        Dictionary with overall accuracy and breakdowns by task and graph type
    """
    total = len(results)
    correct = sum(1 for r in results if r["is_correct"])
    
    # Calculate overall accuracy
    overall_accuracy = correct / total if total > 0 else 0
    
    # Breakdown by task
    task_results = defaultdict(lambda: {"correct": 0, "total": 0})
    for r in results:
        task = r["task_name"]
        task_results[task]["total"] += 1
        if r["is_correct"]:
            task_results[task]["correct"] += 1
    
    task_accuracy = {task: res["correct"] / res["total"] if res["total"] > 0 else 0 
                    for task, res in task_results.items()}
    
    # Breakdown by graph type
    graph_type_results = defaultdict(lambda: {"correct": 0, "total": 0})
    for r in results:
        graph_type = r["graph_type"]
        graph_type_results[graph_type]["total"] += 1
        if r["is_correct"]:
            graph_type_results[graph_type]["correct"] += 1
    
    graph_type_accuracy = {gt: res["correct"] / res["total"] if res["total"] > 0 else 0 
                          for gt, res in graph_type_results.items()}
    
    # Breakdown by task and graph type
    task_graph_results = defaultdict(lambda: {"correct": 0, "total": 0})
    for r in results:
        key = f"{r['task_name']}_{r['graph_type']}"
        task_graph_results[key]["total"] += 1
        if r["is_correct"]:
            task_graph_results[key]["correct"] += 1
    
    task_graph_accuracy = {key: res["correct"] / res["total"] if res["total"] > 0 else 0 
                          for key, res in task_graph_results.items()}
    
    return {
        "overall": overall_accuracy,
        "by_task": task_accuracy,
        "by_graph_type": graph_type_accuracy,
        "by_task_and_graph_type": task_graph_accuracy
    }

def run_evaluation(models, data_formats, max_questions=None, max_workers=5):
    """
    Run evaluation for all models and data formats
    
    Args:
        models: List of model names to evaluate
        data_formats: List of data formats to use
        max_questions: Maximum number of questions per format (for testing)
        max_workers: Maximum number of concurrent workers (default: 5)
    
    Returns:
        Dictionary with evaluation results and accuracy metrics
    """
    all_results = {}
    accuracy_summary = {}
    
    # Create result directory if it doesn't exist
    os.makedirs("result", exist_ok=True)
    
    for data_format in data_formats:
        # Load dataset
        file_path = f"data/{data_format}.json"
        questions = load_dataset(file_path)
        
        for model_name in models:
            print(f"Evaluating {model_name} on {data_format} format...")
            
            # Evaluate model with concurrency
            results = evaluate_model(model_name, data_format, questions, max_questions, max_workers)
            
            # Calculate accuracy
            accuracy = calculate_accuracy(results)
            
            # Store results
            result_key = f"{model_name}_{data_format}"
            all_results[result_key] = results
            accuracy_summary[result_key] = accuracy
            
            # Save individual results to JSON
            with open(f"result/{result_key}_results.json", 'w', encoding='utf-8') as f:
                json.dump(results, f, indent=2)
            
            print(f"  Overall Accuracy: {accuracy['overall']:.4f}")
            print(f"  Results saved to result/{result_key}_results.json")
    
    # Create summary
    summary = {
        "models": models,
        "data_formats": data_formats,
        "results": {}
    }
    
    # 尝试从现有的summary.json加载数据
    try:
        if os.path.exists("result/summary.json"):
            with open("result/summary.json", 'r', encoding='utf-8') as f:
                existing_summary = json.load(f)
                # 合并现有数据
                if "results" in existing_summary:
                    summary["results"] = existing_summary["results"]
                # 确保models和data_formats列表包含所有唯一值
                if "models" in existing_summary:
                    summary["models"] = list(set(models + existing_summary["models"]))
                if "data_formats" in existing_summary:
                    summary["data_formats"] = list(set(data_formats + existing_summary["data_formats"]))
    except Exception as e:
        print(f"Warning: Could not load existing summary.json: {e}")
    
    # Overall summary for each model and format
    for model_name in models:
        if model_name not in summary["results"]:
            summary["results"][model_name] = {}
        for data_format in data_formats:
            key = f"{model_name}_{data_format}"
            summary["results"][model_name][data_format] = accuracy_summary[key]
    
    # Save summary to JSON
    with open("result/summary.json", 'w', encoding='utf-8') as f:
        json.dump(summary, f, indent=2)
    
    return all_results, accuracy_summary, summary

if __name__ == "__main__":
    # Models to evaluate
    models = ['gpt-4o-mini','deepseek-r1']
    # Data formats
    data_formats = ['natural', 'structured', 'matrix', 'list']
    #data_formats = ['structured']
    # Run evaluation with all questions and concurrent processing
    # Set max_workers to control concurrency level
    _, _, summary = run_evaluation(models, data_formats, max_questions=None, max_workers=25)
    
    print("\nEvaluation complete. Results saved to result/summary.json") 