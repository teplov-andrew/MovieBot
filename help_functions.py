def clear_msg(text):
    text = text.replace(' ', '').lower()
    text = text.replace(';', '')
    text = text.replace(',', '')
    text = text.replace('ё', 'е')
    text = text.replace('Ё', 'е')
    return text


def clean_link(link):
    link = link.replace("'", '')
    return link

