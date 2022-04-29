import glob
from jinja2 import Template
import os
import sys



#Creating option for user to add new content files or regen pages
def add_or_regen_content():
    print("This is argv:", sys.argv)
    command = sys.argv[1]
    print(command)
    if command == "build":
        print("Build was specified")
    
    elif command == "new":
        print("New page was specified")
        new_title = input('Enter new pages title: ')
        new_path = './content/' + new_title + '.html'
        open(new_path, 'x')
    else:
        print("Please specify 'build' or 'new'")
    

#Scrapping all files from any folder (in this case the content folder) and storing them in an accesible format
def extract_path_and_name(all_content_files):

    content_files_path = []
    content_file_name = []

#experimenting with alternative methods of generating these lists
    # '''
    # content_files_path = list(
    #     map(lambda file: os.path.basename(file),
    #     all_content_files)
    # )
    # content_file_name = list(map(lambda file_path: os.path.splitext(file_path)[0], content_files_path)
    # '''

    for file in all_content_files:
        file_path = os.path.basename(file)
        name_only, extension = os.path.splitext(file_path)

        content_files_path.append(file_path)
        content_file_name.append(name_only)

    return zip(content_files_path, content_file_name)

#Creating list of dictionaries with all relevant infor for content pages
def create_pages_dict(path_and_filename):

    pages = []

    for path, name in path_and_filename:
        filename = "./content/" + path
        title = name
        file_output = "./docs/" + path

        file_instance = {
            'filename': filename,
            'output': file_output,
            'title': title,
        }
        pages.append(file_instance)
    
    return pages



#Inserting content into base template
def content_replace(template, content_file, title, pages):
    combined_file = template.render(
        content = content_file,
        title = title,
        pages = pages,
        )
  
    return combined_file


#Outputing finished files
def main():
    add_or_regen_content()
    all_content_files = glob.glob("./content/*.html")
    path_and_filename = extract_path_and_name(all_content_files)
    pages = create_pages_dict(path_and_filename)
    base_template = open("./templates/base.html").read()
    template = Template(base_template)
    #for loop to generate each content page from filepaths specified outside of function
    for page in pages:
        content_file = open(page['filename']).read()
        title = page['title']
        output_file = page['output']
        combined_file = content_replace(template, content_file, title, pages)
        
        open(output_file, 'w+').write(combined_file)






# A different method for extracting the file name so it could be used for definig the output path
# html_extension = ''
# for file in all_content_files:
#     html_extension = file.replace('./content/', '')
#     content_files.append(html_extension)
# print(content_files)
