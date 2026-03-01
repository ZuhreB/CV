import difflib

def generate_html_diff(old_text: str, new_text: str) -> str:
    """İki metin arasındaki farkları HTML ve inline CSS ile renklendirerek döndürür."""
    # Metinleri satır satır ayırıyoruz
    old_lines = old_text.splitlines()
    new_lines = new_text.splitlines()
    
    diff = difflib.ndiff(old_lines, new_lines)
    
    html_output = []
    html_output.append('<div style="font-family: sans-serif; line-height: 1.6; font-size: 15px; padding: 15px; background: white; color: #333; border-radius: 8px; border: 1px solid #ddd;">')
    
    for line in diff:
        # ndiff formatı: 
        # '- ' silinen satır, '+ ' eklenen satır, '  ' değişmeyen satır, '? ' ipucu (göz ardı edeceğiz)
        prefix = line[0:2]
        content = line[2:]
        
        if prefix == '- ':
            # Eski, silinmiş veya değiştirilmiş içerik - Kırmızı arka plan ve üstü çizili
            html_output.append(
                f'<div style="background-color: #ffeef0; color: #b71c1c; text-decoration: line-through; padding: 2px 5px; margin: 2px 0;">{content}</div>'
            )
        elif prefix == '+ ':
            # Yeni eklenen içerik - Yeşil arka plan
            html_output.append(
                f'<div style="background-color: #e6ffed; color: #1b5e20; padding: 2px 5px; margin: 2px 0;"><strong>+</strong> {content}</div>'
            )
        elif prefix == '  ':
            # Değişmeyen içerik (veya çok benzer olanlar)
            if content.strip(): # Sadece boş olmayan satırları gösterelim (Çok uzun olmasın)
                html_output.append(f'<div style="color: #666; padding: 2px 5px; margin: 2px 0;">{content}</div>')
    
    html_output.append('</div>')
    return "\n".join(html_output)
