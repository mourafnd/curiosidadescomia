from openai import OpenAI
import os
import datetime
import re

# Inicializa o cliente OpenAI
client = OpenAI()

def slugify(text):
    text = text.lower()
    text = re.sub(r"[^\w\s-]", "", text)
    text = re.sub(r"[\s_-]+", "-", text)
    text = re.sub(r"^-+|-+$", "", text)
    return text

# Sugere um tema aleatório para o post
def suggest_theme():
    prompt = "Me sugira um tema curto, curioso e popular para um blog de curiosidades. Apenas o nome do tema."
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=30,
        temperature=1.0
    )
    return response.choices[0].message.content.strip()

# Gera o conteúdo do post com base no tema
def generate_post(theme):
    prompt = (
        f"Gere um post de blog com título e pelo menos 10 curiosidades sobre o tema '{theme}'. "
        f"Use formatação Markdown e linguagem leve e envolvente. Use título com # e subtítulos com ##."
    )
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "Você é um redator de blog criativo."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.85,
        max_tokens=1200
    )

    return response.choices[0].message.content, theme

# Salva o conteúdo gerado em um arquivo Markdown com front matter Hugo
def save_post(content, theme):
    match = re.search(r"# (.+)", content)
    title = match.group(1).strip() if match else f"Curiosidades sobre {theme}"
    slug = slugify(title)
    date = datetime.datetime.now().isoformat()
    filename = f"content/posts/{slug}.md"

    with open(filename, "w", encoding="utf-8") as f:
        f.write(f"---\n")
        f.write(f'title: "{title}"\n')
        f.write(f"date: {date}\n")
        f.write(f"draft: false\n")
        f.write(f"---\n\n")
        f.write(content)

    print(f"✅ Post salvo: {filename}")

def main():
    theme = suggest_theme()
    print(f"🎯 Tema escolhido: {theme}")
    content, _ = generate_post(theme)
    save_post(content, theme)

if __name__ == "__main__":
    main()
