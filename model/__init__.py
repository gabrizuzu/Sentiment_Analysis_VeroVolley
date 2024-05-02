import numpy as np
import pandas as pd
import os
from tqdm import tqdm
import json

import torch
import torch.nn as nn

import transformers
from transformers import (
    AutoModelForCausalLM,
    AutoTokenizer,
    BitsAndBytesConfig,
    TrainingArguments,
    pipeline,
    logging,
)
from datasets import Dataset, load_dataset
from peft import LoraConfig, PeftConfig
import bitsandbytes as bnb
from trl import SFTTrainer

from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
from sklearn.model_selection import train_test_split

max_seq_length = 2048

# Models
model_gemma = {"model": "google/gemma-2b", "name": "Gemma-2B"}
model_gemma_7b = {"model": "google/gemma-7b", "name": "Gemma-7B"}
model_llama = {"model": "meta-llama/Meta-Llama-3-8B", "name": "Llama"}


def get_model(model_base, model_name):
    """Model Initialization

    The model is initialized with specific paramethers for the optimization of the sentiment analysis.

    In specific, we load:
    - The model with the byte rules.
    - The tokenizer with the limit of characters to generate.
    - The End-Of-Sequence Token, to define where to stop the text generation.

    Keyword arguments:
    model_base -- the name of the base huggingface model
    imag -- the name of the model used (either base of folder to tuned)
    """
    tokenizer_model_name = model_base

    # Use Pretrained model
    model_name = f"./models/Llama"

    tokenizer = AutoTokenizer.from_pretrained(
        tokenizer_model_name, max_seq_length=max_seq_length
    )

    compute_dtype = getattr(torch, "float16")

    bnb_config = BitsAndBytesConfig(
        load_in_4bit=True,
        bnb_4bit_use_double_quant=False,
        bnb_4bit_quant_type="nf4",
        bnb_4bit_compute_dtype=compute_dtype,
    )

    model = AutoModelForCausalLM.from_pretrained(
        model_name,
        device_map="auto",
        quantization_config=bnb_config,
    )

    model.config.use_cache = False
    model.config.pretraining_tp = 1

    tokenizer.pad_token = tokenizer.eos_token
    tokenizer.pad_token_id = tokenizer.eos_token_id

    return model, tokenizer


def generate_prompt(data_point, EOS_TOKEN):
    return (
        f"""generate_prompt
            Analyze the sentiment of the news headline enclosed in square brackets,
            determine if it is positive, neutral, or negative, and return the answer as
            the corresponding sentiment label "positive" or "neutral" or "negative"

            [{data_point["text"]}] = {data_point["label_text"]}
            """.strip()
        + EOS_TOKEN
    )


def generate_test_prompt(data_point):
    text = data_point
    if not isinstance(data_point, str):
        text = data_point["text"]

    return f"""
            Analyze the sentiment of the news headline enclosed in square brackets,
            determine if it is positive, neutral, or negative, and return the answer as
            the corresponding sentiment label "positive" or "neutral" or "negative"

            [{text}] =

            """.strip()


def get_training_dataset(tokenizer):
    df = load_dataset("SetFit/tweet_sentiment_extraction")
    df = pd.DataFrame(df["train"])

    X_train = list()
    X_test = list()
    for sentiment in ["positive", "neutral", "negative"]:
        train, test = train_test_split(
            df[df.label_text == sentiment],
            train_size=600,
            test_size=600,
            random_state=42,
        )
        X_train.append(train)
        X_test.append(test)

    X_train = pd.concat(X_train).sample(frac=1, random_state=10)
    X_test = pd.concat(X_test)

    eval_idx = [
        idx for idx in df.index if idx not in list(train.index) + list(test.index)
    ]
    X_eval = df[df.index.isin(eval_idx)]
    X_eval = X_eval.groupby("label_text", group_keys=False).apply(
        lambda x: x.sample(n=100, random_state=10, replace=True)
    )
    X_train = X_train.reset_index(drop=True)

    X_train = pd.DataFrame(
        X_train.apply(lambda x: generate_prompt(x, tokenizer.eos_token), axis=1),
        columns=["text"],
    )
    X_eval = pd.DataFrame(
        X_eval.apply(lambda x: generate_prompt(x, tokenizer.eos_token), axis=1),
        columns=["text"],
    )

    y_true = pd.DataFrame(X_test).label_text
    X_test = pd.DataFrame(X_test.apply(generate_test_prompt, axis=1), columns=["text"])

    train_data = Dataset.from_pandas(X_train)
    eval_data = Dataset.from_pandas(X_eval)

    return train_data, eval_data, X_test, y_true


def evaluate(y_true, y_pred):
    print()
    labels = ["positive", "neutral", "negative"]
    mapping = {"positive": 2, "neutral": 1, "none": 1, "negative": 0}

    def map_func(x):
        return mapping.get(x, 1)

    y_true = np.vectorize(map_func)(y_true)
    y_pred = np.vectorize(map_func)(y_pred)

    # Calculate accuracy
    accuracy = accuracy_score(y_true=y_true, y_pred=y_pred)
    print(f"Accuracy: {accuracy:.3f}")

    # Generate accuracy report
    unique_labels = set(y_true)  # Get unique labels

    for label in unique_labels:
        label_indices = [i for i in range(len(y_true)) if y_true[i] == label]
        label_y_true = [y_true[i] for i in label_indices]
        label_y_pred = [y_pred[i] for i in label_indices]
        accuracy = accuracy_score(label_y_true, label_y_pred)
        print(f"Accuracy for label {label}: {accuracy:.3f}")

    # Generate classification report
    class_report = classification_report(y_true=y_true, y_pred=y_pred)
    print("\nClassification Report:")
    print(class_report)

    # Generate confusion matrix
    conf_matrix = confusion_matrix(y_true=y_true, y_pred=y_pred, labels=[0, 1, 2])
    print("\nConfusion Matrix:")
    print(conf_matrix)


def predict(X_test, model, tokenizer):
    y_pred = []
    for i in tqdm(range(len(X_test))):
        prompt = X_test.iloc[i]["text"]
        input_ids = tokenizer(prompt, return_tensors="pt").to("cuda")
        outputs = model.generate(
            **input_ids,
            max_new_tokens=1,
            temperature=0.001,
            pad_token_id=tokenizer.eos_token_id,
        )
        result = tokenizer.decode(outputs[0])
        answer = result.split("=")[-1].lower()
        if "positive" in answer:
            y_pred.append("positive")
        elif "negative" in answer:
            y_pred.append("negative")
        elif "neutral" in answer:
            y_pred.append("neutral")
        else:
            y_pred.append("none")
    return y_pred


def predict_json(filename, model, tokenizer):
    try:
        with open(filename) as f:
            json_data = json.load(f)
    except FileNotFoundError:
        print("File not found. Please check the file path and try again.")
        return

    folder = ".".join(filename.split(".")[:-1])

    # save input
    os.makedirs(f"data/{folder}", exist_ok=True)
    with open(f"data/{folder}/input.json", "w") as f:
        json.dump(json_data, f, indent=2)

    # List to collect all texts
    texts = []

    # Iterate over each post and its comments
    for post in json_data:
        # Append the post caption text
        texts.append(generate_test_prompt(post["caption_text"]))
        # Append each comment text
        for comment in post["comments"]:
            texts.append(generate_test_prompt(comment["text"]))

    # Convert the list of texts into a DataFrame in one go
    df = pd.DataFrame(texts, columns=["text"])
    # Predict emotions
    y_pred = predict(df, model, tokenizer)
    print()

    # Assign emotion to posts and comments
    index = 0
    for post in json_data:
        post["sentiment"] = y_pred[index]
        index += 1
        print("-" * 30)
        print(f"\n{post['sentiment']}: {post['caption_text']}")
        for comment in post["comments"]:
            comment["sentiment"] = y_pred[index]
            index += 1
            print(f"  {comment['sentiment']}: {comment['text']}")

    # Save output
    with open(f"data/{folder}/output.json", "w") as f:
        json.dump(json_data, f, indent=2)


def train(model, tokenizer, train_data, eval_data, save_folder):
    peft_config = LoraConfig(
        lora_alpha=16,
        lora_dropout=0,
        r=64,
        bias="none",
        task_type="CAUSAL_LM",
        target_modules=[
            "q_proj",
            "k_proj",
            "v_proj",
            "o_proj",
            "gate_proj",
            "up_proj",
            "down_proj",
        ],
    )

    training_arguments = TrainingArguments(
        output_dir="logs",
        num_train_epochs=1,
        gradient_checkpointing=True,
        per_device_train_batch_size=1,
        gradient_accumulation_steps=8,
        optim="paged_adamw_32bit",
        save_steps=0,
        logging_steps=25,
        learning_rate=2e-4,
        weight_decay=0.001,
        fp16=True,
        bf16=False,
        max_grad_norm=0.3,
        max_steps=-1,
        warmup_ratio=0.03,
        group_by_length=False,
        evaluation_strategy="steps",
        load_best_model_at_end=True,
        eval_steps=112,
        eval_accumulation_steps=1,
        lr_scheduler_type="cosine",
        report_to="tensorboard",
    )

    trainer = SFTTrainer(
        model=model,
        train_dataset=train_data,
        eval_dataset=eval_data,
        peft_config=peft_config,
        dataset_text_field="text",
        tokenizer=tokenizer,
        max_seq_length=max_seq_length,
        args=training_arguments,
        packing=False,
    )

    # Train model
    trainer.train()

    # Save trained model
    trainer.model.save_pretrained(save_folder)
