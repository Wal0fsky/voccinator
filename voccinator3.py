import os
from InquirerPy import inquirer
import csv
import numpy as np
import sys 
import io

# make terminal ready to encode every unicode character (important for e.g. French) | AI used for this function
def configure_terminal_for_utf8() : 
    # Set environment variables
    os.environ["PYTHONUTF8"]       = "1" 
    os.environ["PYTHONIOENCODING"] = "utf-8"
    os.environ["LANG"]             = "en_US.UTF-8"
    os.environ["LC_ALL"]           = "en_US.UTF-8"

    # set some windows specific variables 
    if os.name == "nt" : 
        os.system("chcp 65001 > nul")   
        os.environ["LC_CTYPE"] = "C.UTF-8"

    # define stdin, -out & -err 
    sys.stdin  = io.TextIOWrapper(sys.stdin.buffer,  encoding='utf-8', errors='replace')
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')
    
class VoccinatorV3() : 
    def __init__(self) : 
        # spell out all text that will be printed to the terminal
        self.texts = {
            "welcome" : "--Welcome to Voccinator 3.0--", 
            "no-folder" : "There is no folder to store the learnsets yet. Would you like to create one in your wd (y, N): ", 
            "custom-folder" : "Please choose a custom dir: ", 
            "folder-path-error" : "ERROR: Path to folder with learnsets not valid: check '.path_to_learnsets.txt'", 
            "custom-folder-error" : "ERROR: Custom path not valid.", 
            "select-feature-info" : "Please select a feature below.", 
            "exit-program" : "Exiting voccinator...", 
            "landing-page-header" : "\n--Home--", 
            "create-new-file-header" : "\n--Create New Learnset--", 
            "create-new-file-info" : "You can create a learnset by entering a word and its definition. (write 'exit' to leave the feature)\n", 
            "create-new-file-name" : "Please specify the name of the new learnset: ", 
            "create-new-file-success" : "New learnset successfully created!", 
            "ask-word" : "\nEnter word: ", 
            "ask-definition" : "Enter definition: ", 
            "exit-info" : "Exiting...", 
            "save-info" : "Saving...", 
            "load-info" : "Fetching data...", 
            "edit-file-header" : "\n--Edit Existing Learnset--", 
            "edit-file-info" : "You can now extend a learnset that already exists. (write 'exit' to leave the feature)\n", 
            "select-file-info" : "Please selcet a learnset below.", 
            "show-file-header" : "\n--Show Learnset--", 
            "show-file-info" : "Voccinator will display all words and the corresponding definitions of a learnset.\n", 
            "show-file-info2" : "Learnset Contents", 
            "empty-file-info" : "This learnset is empty.",
            "write-modus-header" : "\n--Write Modus--", 
            "write-modus-info" : "Voccinator provides you with a word, whose definition you have to answer. (write 'exit' to leave the feature)\n",
            "write-modus-success" : "You have defined all Words correctly. Congrats :)", 
            "del-header" : "\n--Delete Item From Learnset", 
            "del-info" : "You can delete a specifc line from a learnset.\n", 
            "del-info2" : "The following lines will be deleted:", 
            "del-check" : "Do you wish to continue (Y, n): ", 
            "del-info3" : "Process cancled: Exiting...", 
            "del-success" : "voccinator has successfully deleted the selected words!", 
            "select-line-info" : "Choose the line that should be deleted", 
            "no-files" : "There are no learnsets available."
        }

        # list for all app features and connect the corresponding method
        self.app_features = [
            {"name" : "Create New Learnset", "value" : self.create_new_file}, 
            {"name" : "Edit Existing Learnset", "value" : self.edit_file}, 
            {"name" : "Show Learnset", "value" : self.show_file}, 
            {"name" : "Write Practise", "value" : self.write_modus}, 
            {"name" : "Delete Words From Learnset", "value" : self.del_word_from_file}, 
            {"name" : "Exit", "value" : self.exit_program}, 
        ]

        # get location of voccinator script
        self.script_dir = os.path.dirname(os.path.abspath(__file__))   

        # welcome user 
        print(self.texts["welcome"])

       # is there already a folder for the learnsets? -> if not creat one.
    def _checkon_learnset_folder(self) :

        # create path to file which stores the path to app data
        file = os.path.join(self.script_dir, ".path_to_learnsets.txt")

        # get path to app data (if path is specified)
        if os.path.isfile(file) :
            with open(file, "r") as f :
                path = f.read().strip()
                if os.path.isdir(path) :
                    self.folder_path = path
                    return
                else :
                    print(self.texts["folder-path-error"])
                    exit()

        # a learnset folder is already sitting in the cwd -> adopt it silently
        cwd_folder = os.path.join(os.getcwd(), "LEARNSETS")
        if os.path.isdir(cwd_folder) :
            self._save_folder_path(file, cwd_folder)
            return

        
        # if no path to app data is specified let the user select one or specify one
        answer = input(self.texts["no-folder"]).strip()

        # custom path?
        if answer.upper() == "N" :
            cfpath = input(self.texts["custom-folder"]).strip()
            if not os.path.isdir(cfpath) :
                print(self.texts["custom-folder-error"])
                exit()
            target = os.path.join(cfpath, "LEARNSETS")
        else :
            target = os.path.join(os.getcwd(), "LEARNSETS")

        # adopt the folder if it already exists, otherwise create it
        try :
            os.makedirs(target, exist_ok=True)
        except OSError :
            print(self.texts["custom-folder-error"])
            exit()

        self.folder_path = target
        with open(file, "w") as f :
            f.write(target)

    # remember where the learnsets live
    def _save_folder_path(self, file, path) :
        self.folder_path = path
        with open(file, "w") as f :
            f.write(path)

    # let user choose a feature -> executre choosen one
    def _choose_features(self) :
        feature = inquirer.select(
            message=self.texts["select-feature-info"], 
            choices=self.app_features
        ).execute()
        feature()

    # let user choose a learnset -> return (name of) learnset 
    def _choose_file(self) : 
        files = os.listdir(self.folder_path)
        if files : 
            files = [{"name" : "".join(f.split(".")[:-1]), "value" : f} for f in files]
            file = inquirer.select(
                message=self.texts["select-file-info"], 
                choices=files
            ).execute()
            return file
        else : 
            print(self.texts["no-files"])

    # edit/create a file by entering a word and its definition
    def _write_to_file(self, name, mode) : 
        with open(os.path.join(self.folder_path, name), mode, encoding="utf-8") as f :
            print(self.texts["create-new-file-success"])
            writer = csv.writer(f, delimiter=";", quotechar="|")
            row = []
            while "exit" not in row : 
                if row : 
                    writer.writerow(row) 
                row = [input(self.texts["ask-word"]).strip(), input(self.texts["ask-definition"]).strip()]      

    # gather the content of a learnset -> return tuple list of contents
    def _read_file(self, name) :
        with open(os.path.join(self.folder_path, name), "r", encoding="utf-8") as f :
            reader = csv.reader(f, delimiter=";", quotechar="|")
            file_content = []
            for row in reader : 
                if row : 
                    w, d = row
                    file_content.append((w, d))
        if not file_content : 
            print(self.texts["empty-file-info"])
        return file_content
    
    # print a list of pairs in a repectable format to the terminal
    def _print_pairs(self, pairs) : 
        for i, (w, d) in enumerate(pairs) : 
            print(f"{i+1}) {w}: {d}")
                
    # landing page
    def landing_page(self) : 
        self._checkon_learnset_folder()
        print(self.texts["landing-page-header"])
        self._choose_features()

    # create a new file
    def create_new_file(self) : 
        print(self.texts["create-new-file-header"])
        print(self.texts["create-new-file-info"])
        file_name = input(self.texts["create-new-file-name"])

        self._write_to_file(file_name + ".csv", "w")
        print(self.texts["exit-info"])

    # edit existing file
    def edit_file(self) : 
        print(self.texts["edit-file-header"])
        print(self.texts["edit-file-info"])

        file_name = self._choose_file()
        if not file_name : 
            return
        self._write_to_file(file_name, "a")
        print(self.texts["exit-info"])

    # Display a learning set
    def show_file(self) : 
        print(self.texts["show-file-header"])
        print(self.texts["show-file-info"])

        file_name = self._choose_file()
        if not file_name : 
            return
        pairs = self._read_file(file_name)

        if pairs : 
            print(self.texts["show-file-info2"])
            self._print_pairs(pairs)
        else : 
            print(self.texts["empty-file-info"])

    # give user word -> ask for definition. User can save/load progress
    def write_modus(self) : 
        print(self.texts["write-modus-header"])
        print(self.texts["write-modus-info"])

        file_name = self._choose_file()
        if not file_name : 
            return
        pairs = self._read_file(file_name)
        if not pairs : 
            return

        all_idx = np.arange(len(pairs))
        np.random.shuffle(all_idx)
       
        while len(all_idx) > 0 : 
            w, d = pairs[all_idx[0]]
            print(w)
            answer = input(self.texts["ask-definition"]).strip()

            if answer == "exit" : 
                return
            elif answer == "save" :
                print(self.texts["save-info"])
                np.save(os.path.join(self.script_dir, ".write_idx.npy"), all_idx)
            elif answer == "load" : 
                print(self.texts["load-info"])
                all_idx = np.load(os.path.join(self.script_dir, ".write_idx.npy"))
            elif answer == d.strip() : 
                all_idx = all_idx[1:]
                print(f"Correct! {len(all_idx)} to go\n")
            else : 
                np.random.shuffle(all_idx)
                print(f"Wrong! Solution: {d}\n")
        print(self.texts["write-modus-success"])

    # delete specific lines form a file
    def del_word_from_file(self) : 
        print(self.texts["write-modus-header"])
        print(self.texts["write-modus-info"])

        file_name = self._choose_file()
        if not file_name : 
            return
        pairs = self._read_file(file_name)
        if not pairs : 
            return 

        idx = inquirer.checkbox(
            message=self.texts["select-line-info"], 
            choices=[{"name" : f"{w}: {d}", "value" : i} for i, (w, d) in enumerate(pairs)]
        ).execute()
        if not idx : 
            print(self.texts["exit-info"])
            return 

        new_pairs = [p for i, p in enumerate(pairs) if i not in idx]

        print(self.texts["del-info2"])
        self._print_pairs([pairs[i] for i in idx])
        check = input(self.texts["del-check"]).strip()
        
        if check == "y" or check == "Y" : 
            with open(os.path.join(self.folder_path, file_name), "w", encoding="utf-8") as f :
                writer = csv.writer(f, delimiter=";", quotechar="|")
                for p in new_pairs :
                    writer.writerow(list(p))
            print(self.texts["del-success"])
        else : 
            print(self.texts["del-info3"])
        
    # exit voccinator
    def exit_program(self) : 
        print(self.texts["exit-program"])
        exit()

if __name__ == "__main__" : 
    # ensure that utf-8 works
    configure_terminal_for_utf8()
    
    # init voccinator
    V = VoccinatorV3() 
    
    # as long as the user doesnt kill the program it will kickstart the landing page
    while True : 
        V.landing_page()