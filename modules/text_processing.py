import re 



def remove_wiki_markup(txt):
    
    """removes the wiki markup from the given text"""
    
    txt = re.sub(r"\[\[.*?\]\]", "", txt) # internal links like: '[[WP:NETPOS]]'
    txt = re.sub(r"&[a-zA-Z]+;|&#[0-9]+;", "", txt) # html entities like: '&nbsp;–&nbsp';
    txt = re.sub(r"'''(.*?)'''", r"\1", txt) # bold
    txt = re.sub(r"''(.*?)''", r"\1", txt) # italic
    txt = re.sub(r"<.*?>", "", txt) # html
    txt = re.sub(r"\[\[.*?\|([^\]]*?)\]\]", r"\1", txt) # links
    txt = re.sub(r"\[http[^\]]*?\]", "", txt) # external links 
    txt = re.sub(r"\{\{.*?\}\}", "", txt) # templates 
    txt = re.sub(r"==([^=]+)==", r"\1", txt) # header 
    txt = re.sub(r"==([^=]+)==", r"\1", txt) # dash
    txt = re.sub(r'--', ' ', txt)
    return txt 
