from model import get_model, get_training_dataset, train, predict, evaluate, model_llama

# Get & Train Model
model_base = model_llama
model, tokenizer = get_model(model_base["model"], model_base["model"])
train_dataset, eval_dataset, X_test, y_pred = get_training_dataset(tokenizer)
train(model, tokenizer, train_dataset, eval_dataset, model_base["name"])

# Test Model
y_true = predict(X_test, model, tokenizer)
evaluate(y_true, y_pred)
