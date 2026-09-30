import csv
import random

def load_vocab():
    vocab_list = []
    with open(r"C:\Users\ASUS\Desktop\data\vocab.csv", "r", encoding="utf-8-sig") as f:
        reader = csv.reader(f)
        next(reader)   # 跳过第一行表头
        for row in reader:
            item = {
                "word": row[0],
                "pinyin": row[1],
                "meaning": row[2],
                "hsk": int(row[3]),
                "pos": row[4]
            }
            vocab_list.append(item)
    return vocab_list

def save_to_file(content, filename):
    with open(filename, "w", encoding="utf-8") as f:
        f.write(content)

def filter_by_hsk(vocab_list, level):
    result = []
    for w in vocab_list:
        if w["hsk"] == level:
            result.append(w)
    return result

def gen_sentence_exercise(word_list):
    out = "==== HSK词汇造句练习 ====\n请使用下面词语写句子\n\n"
    for idx, w in enumerate(word_list, 1):
        out += f"{idx}. {w['word']}（{w['pinyin']}）：________\n"
    return out

def gen_choice_exercise(word_list):
    if len(word_list) < 4:
        return "词汇数量不足，无法生成选择题！至少需要4个词汇。\n"
    content = "==== HSK词汇选择题练习 ====\n选出匹配释义的正确词语\n\n"
    for index, correct_word in enumerate(word_list, 1):
        distract_pool = [w for w in word_list if w["word"] != correct_word["word"]]
        distractors = random.sample(distract_pool, k=3)
        options = distractors + [correct_word]
        random.shuffle(options)
        content += f"{index}. 释义：{correct_word['meaning']}（{correct_word['pinyin']}）\n"
        opt_letter = ["A", "B", "C", "D"]
        for letter, opt_word in zip(opt_letter, options):
            content += f"   {letter}. {opt_word['word']}\n"
        content += "\n"
    return content

if __name__ == "__main__":
    all_vocab = load_vocab()
    hsk4_words = filter_by_hsk(all_vocab,4)
    print(f"总共读取词汇：{len(all_vocab)} 个")
    print(f"筛选得到HSK4词汇：{len(hsk4_words)} 个")
    sentence_text = gen_sentence_exercise(hsk4_words)
    save_to_file(sentence_text, "造句练习.txt")
    print("✅已生成：造句练习.txt")
    choice_text = gen_choice_exercise(hsk4_words)
    save_to_file(choice_text, "选择题练习.txt")
    print("✅已生成：选择题练习.txt")