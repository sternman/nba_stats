create a virutal environment
    make a new folder for this project, think of our repo folder, something like that

    vs code:
        open new window, point to that folder
        press ctrl+shift+p and type python create -- in the list, select create environment
        it will prompt you to make an environment called .venv, click enter (not conda)
        click python version
        wait for it to complete

    command-line interface (cli):
        navigate to that folder from command prompt 
        type python -m venv \path\to\your\python\work\environment_name  (example c:\src\nba_stats\venv)
        wait for it to make the environment
    
    we need to install packages. I think vs code can do this, but I still do it classically though pip and cli

    open a cli window if you dont have one open and navigate to your code folder

    type cd .venv/scripts
    type activate

    you will notice the command prompt change to say (.venv) at the start of the line

    now lets install packages!

    I put the libraries needed for this example in requirements.txt, so we will install the contents

    type pip install -r requirements.txt

    it will now download and install these libraries to your new virtual environment (venv).
    note, venvs are unique to projects and should be installed in the parent folder of the project. you cannot install more than one per project.
    
    once completed, you can run the code sample

    streamlit run stats.py

    a web browser should open up displaying what this sample app does
