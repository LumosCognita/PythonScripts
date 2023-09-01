import configparser
import os
import openai


config = configparser.ConfigParser()

THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))

config.read(os.path.join(THIS_FOLDER,'config.ini'))

openai.api_key = config.get('OPENAI', 'OPENAI_API_KEY')

def read_article(file_path):
    with open(file_path, 'r') as file:
        return file.read().replace('\n', ' ')
    
def save_quiz_questions(file_path, json_data):
    with open(file_path, 'w') as file:
        return file.write(json_data)
    
def generate_question(article_body):
    prompt = f"{article_body}"
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", 
             "content": "You're a career expert that can generate 25 multiple-choice questions for assessment purposes based on an a given article's content, respond with a JSON object. The format should include questions array, each with question, options, each option has id and label, and an answer which is the id of the correct option"},
            {"role": "user", "content": prompt}
        ])

    return response['choices'][0]['message']['content']

if __name__ == '__main__':
    article_text = read_article('./Software_Engineer.txt')
    print(len(article_text))
    model_result = generate_question(article_text)

    print(type(model_result))
    print(model_result)

    save_quiz_questions('./result.json', model_result)
