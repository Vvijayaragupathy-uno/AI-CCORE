from github import Github
import os

def upload_file_to_github(uploaded_file, folder_path, repo_name, github_token):
    g = Github(github_token)
    repo = g.get_repo(repo_name)
    file_content = uploaded_file.getvalue()
    file_path = f"{folder_path}/{uploaded_file.name}"

    try:
        # Check if the folder exists, if not create it
        repo.get_contents(folder_path)
    except:
        repo.create_file(
            path=f"{folder_path}/.gitkeep",
            message=f"Create {folder_path} folder",
            content="",
            branch="main"
        )

    try:
        # Update the file if it already exists
        existing_file = repo.get_contents(file_path)
        repo.update_file(file_path, f"Update {uploaded_file.name} via Streamlit", file_content, existing_file.sha)
        return f"Document '{uploaded_file.name}' updated successfully in the '{folder_path}' folder on GitHub!"
    except:
        # Create the file if it doesn't exist
        repo.create_file(file_path, f"Add {uploaded_file.name} via Streamlit", file_content)
        return f"Document '{uploaded_file.name}' uploaded successfully to the '{folder_path}' folder on GitHub!"
