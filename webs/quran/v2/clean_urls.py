import re

file_path = "index.html"
with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

# JSON içerisindeki url: "..." bilgisini sil
# Örnek: image: { url: "...", alt: "Kur'an", icon: "fa-book-open" }
# Dönüşeceği şekil: image: { alt: "Kur'an", icon: "fa-book-open" }
pattern = re.compile(r'url:\s*"[^"]*",\s*')
new_content = pattern.sub('', content)

# Yorum bloğunu güncelle: `url` kaldırıldı
comment_pattern = re.compile(r'\s*url\s*→ Wikimedia Commons vb. açık lisanslı direkt link\n')
new_content = comment_pattern.sub('\n', new_content)
new_content = new_content.replace("image      : { url, alt, icon }", "image      : { alt, icon }")

with open(file_path, "w", encoding="utf-8") as f:
    f.write(new_content)

print("URL cleaning done.")
