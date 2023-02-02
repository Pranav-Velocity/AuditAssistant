def handle_uploaded_file(f, folder_name, file_name):  
    with open('./../static/upload/'+folder_name+'/' + file_name, 'wb+') as destination:  
        for chunk in f.chunks():  
            destination.write(chunk)  