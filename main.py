
import pandas as pd
import os
import subprocess
import shutil
import stat

def download_github_repo(repo_url, destination_folder):
    try:
        command = f"git clone {repo_url} {destination_folder}"
        subprocess.run(command, shell=True)
    except Exception as e:
        print(f"Error while cloning GitHub repository {repo_url}: {e}")

def run_designitejava(repo_folder, output_folder, designite_jar_path):
    try:
        designite_command = f"java -jar {designite_jar_path} -i {repo_folder} -o {output_folder}"
        subprocess.run(designite_command, shell=True)
    except Exception as e:
        print(f"Error while running DesigniteJava on {repo_folder}: {e}")
    

def delete_temp_folder(temp_folder):
    print("Deleting " + temp_folder)
    
    if not os.path.exists(temp_folder):
        return
    
    # Ensure that all files and folders within the temp folder are writable
    for dirpath, dirnames, filenames in os.walk(temp_folder):
        for filename in filenames + dirnames:
            filepath = os.path.join(dirpath, filename)
            os.chmod(filepath, stat.S_IWRITE)
    
    # Attempt to remove the temp folder
    try:
        shutil.rmtree(temp_folder)
    except Exception as exception:
        print('Error while deleting temp folder')
        print(exception)
        exit(1)

def record_and_remove_results(repo_name, repo_folder, output_folder, results_csv_path):
    architecture_csv_path = os.path.join(output_folder, 'ArchitectureSmells.csv')
    design_csv_path = os.path.join(output_folder, 'DesignSmells.csv')

    try:
        # read Architecture Smells CSV file
        architecture_col_names = ["Project Name", "Package Name", "Architecture Smell", "Cause of the Smell"]
        architecture_df = pd.read_csv(architecture_csv_path, names=architecture_col_names)
        architecture_smells_count = len(architecture_df)
        
        # read Design Smells CSV file
        design_col_names = ["Project Name", "Package Name", "Type Name", "Design Smell", "Cause of the Smell"]
        design_df = pd.read_csv(design_csv_path, names=design_col_names)
        design_smells_count = len(design_df)

        # record result
        result_df = pd.DataFrame({'repo': [repo_name],
                                  'architecture_smell': [architecture_smells_count],
                                  'design_smell': [design_smells_count]})
        result_df.to_csv(results_csv_path, mode='a', header=not os.path.exists(results_csv_path), index=False)

    except FileNotFoundError as e:
        print(f"Error reading CSV files: {e}")

    # delete repo folder and generated CSV file
    delete_temp_folder(repo_folder)
    delete_temp_folder(output_folder)

def main():
    # read CSV file
    current_directory = os.path.dirname(os.path.abspath(__file__))
    csv_path = os.path.join(current_directory, 'dataset.csv')
    df = pd.read_csv(csv_path)

     # get java projects
    java_projects = df[df['language'].str.lower() == 'java'].head(3)

    # create folder for repos
    destination_folder = 'java_repos'
    os.makedirs(destination_folder, exist_ok=True)

     # set absolute path of  DesigniteJava.jar 
    designite_jar_path = os.path.join(current_directory, 'DesigniteJava.jar')

    # create result file
    results_csv_path = os.path.join(current_directory, 'results.csv')
    result_df = pd.DataFrame(columns=['repo', 'architecture_smell', 'design_smell'])
    result_df.to_csv(results_csv_path, mode='w', header=True, index=False)
    

    # download each repo and analyze
    for index, row in java_projects.iterrows():
        repo_name = row['repository']
        repo_url = f"https://github.com/{repo_name}.git"
        repo_folder = os.path.join(destination_folder, repo_name)
        try:
            download_github_repo(repo_url, repo_folder)
            
            # run DesigniteJava tool
            output_folder = os.path.join('result', repo_name)
            os.makedirs(output_folder, exist_ok=True)
            run_designitejava(repo_folder, output_folder, designite_jar_path)

            # record result and delete generated file and downloaded repo
            record_and_remove_results(repo_name, repo_folder, output_folder, results_csv_path)
        except Exception as e:
            print(f"Error processing repository {repo_name}: {e}")

    shutil.move(results_csv_path, os.path.join(current_directory, 'results.csv'))

if __name__ == "__main__":
    main()
