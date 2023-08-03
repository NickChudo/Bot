from transformers import AutoModelForSeq2SeqLM, T5TokenizerFast
import torch

class corrector:
    # Зададим название выбронной модели из хаба
    MODEL_NAME = 'UrukHan/t5-russian-spell'
    MAX_INPUT = 256

    # Загрузка модели и токенизатора

    def __init__(self):
        self.tokenizer = T5TokenizerFast.from_pretrained(self.MODEL_NAME)
        self.model = AutoModelForSeq2SeqLM.from_pretrained(self.MODEL_NAME)
        self.device = torch.device('cpu')
    # Входные данные (можно массив фраз или текст)
    # input_sequences = ['длавная проблема для абучение ный ронныйсити ребулитцся ковичиство примерев привый шающие количи ство порамиром ный ранный сити', 'когд а вы прдет к нам в госи']   # или можно использовать одиночные фразы:  input_sequences = 'сеглдыя хорош ден'

    def correctize(self, input):
        input_sequences = [input]
        task_prefix = "Spell correct: "                 # Токенизирование данных
        if type(input_sequences) != list: input_sequences = [input_sequences]
        encoded = self.tokenizer(
        [task_prefix + sequence for sequence in input_sequences],
        padding="longest",
        max_length= self.MAX_INPUT,
        truncation=True,
        return_tensors="pt",
        )
        use_gpu = 0
       

        predicts = self.model.generate(**encoded.to(self.device))
        return self.tokenizer.batch_decode(predicts, skip_special_tokens=True)

