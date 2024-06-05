from transformers import AutoTokenizer, AutoModel

model_name = "intfloat/multilingual-e5-base"
model_path = f"model/{model_name}"

# Download and save model and tokenizer
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModel.from_pretrained(model_name)

tokenizer.save_pretrained(model_path)
model.save_pretrained(model_path)