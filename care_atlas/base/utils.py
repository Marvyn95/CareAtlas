import secrets
import os
from django.conf import settings

def file_handler(files):
    file_name_list = []
    for i in files:
        #creating random file name
        random_string = secrets.token_hex(16)
        file_ext = (i.name).split(".")[-1]
        new_file_name = f"{random_string}.{file_ext}"
        
        file_path = os.path.join(settings.BASE_DIR, "media", new_file_name)
        
        #saving file in memory with new name
        with open(file_path, "wb+") as f:
            for chunk in i.chunks():
                f.write(chunk)
                
        #updating file name list
        file_name_list.append(new_file_name)
        
    return file_name_list