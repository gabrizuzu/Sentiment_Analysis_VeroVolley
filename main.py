from model import get_model, predict_json, model_llama

# Get Model
model_base = model_llama
model, tokenizer = get_model(model_base["model"], model_base["name"])

filename = "test.json"

# Predict
predict_json(filename, model, tokenizer)
