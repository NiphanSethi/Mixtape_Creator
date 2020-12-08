try:
    import tkinter as tk
    import os
    from urllib import request, parse
    from pytube import YouTube
    import youtube_dl

except Exception as e:
    print("Please install the required modules to execute the program: {}".format(e))
    exit()

##################################################################################################################

class MixtapeCreator:

    @staticmethod
    def read_songs_file(path_to_songs_list, mixtape_dir, state, root, total_songs):
        file = open(path_to_songs_list, "r")
        unsuccessful_downloads = MixtapeCreator.create_mixtape(file, mixtape_dir, state, root, total_songs)
        file.close()
        return unsuccessful_downloads
    
    @staticmethod
    def determine_url(line):
        query_string = parse.urlencode({"search_query" : line})
        html_content = request.urlopen("https://www.youtube.com/results?" + query_string)
        html_content = html_content.read().decode()
        index = html_content.find("/watch?v=")
        video_url = "https://www.youtube.com"
        for i in range(index, index + 20):
            video_url += html_content[i]
        return video_url
    
    @staticmethod
    def determine_filename(line):
        invalid_chars = "_*<>\'?\n%|:\"}{/\\"
        temp = line
        filename = ""

        for char in temp:
            if char in invalid_chars:
                temp = temp.replace(char, '')

        for i in range(0, len(temp)):
            if i == 0:
                filename = temp[i].upper() if temp[i].islower() else temp[i]
            else:
                if temp[i - 1] == ' ' and temp[i].isalpha() and temp[i].islower():
                    filename += temp[i].upper()
                else:
                    filename += temp[i]
        return filename
    
    @staticmethod
    def download_vid(mixtape_dir, audio_filename, video_url):
        
        ydl_opts = {
            "format" : "bestaudio/best",
            "extractaudio" : True,
            "audioformat" : "mp3",
            "outtmpl" : mixtape_dir + '/' + audio_filename + ".mp3"
        }

        print(audio_filename)
        print(video_url)
        
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            ydl.download([video_url])
    
    @staticmethod
    def update(root, state, message):
        state.configure(text = message)
        root.update()

    @staticmethod
    def create_mixtape(file, mixtape_dir, state, root, total_songs):
        num_downloaded = 0
        unsuccessful_downloads = []
        # iterate through all songs listed in the file
        for line in file:
            # Skip empty lines in file
            if line == '\n' or line == "":
                continue
            
            try:
                if ":" not in line:
                    MixtapeCreator.update(root, state, "Error :     Line {} incorrectly formatted, skipping download...".format(num_downloaded + 1))
                    continue

                # Determine filename of audio
                audio_filename = MixtapeCreator.determine_filename(line)
                audio_filename = audio_filename.replace("  ", "-")
                # Determine url of youtube video
                video_url = MixtapeCreator.determine_url(line.replace(':', '-'))
                # Download audio of Youtube Video in mp3 format
                MixtapeCreator.download_vid(mixtape_dir, audio_filename, video_url)
                # Increment counter by 1 
                num_downloaded += 1
                # Update GUI to show number of songs successfully downloaded
                MixtapeCreator.update(root, state, "Please Wait :     Creating... ({}/{} songs successfully downloaded)".format(num_downloaded, total_songs))
            except Exception:
                unsuccessful_downloads.append(line)

        return unsuccessful_downloads
            
            
    
    
##################################################################################################################

class InputValidator:
    
    def __init__(self, songs_list_path, save_to_dir, mixtape_title):
        self.songs_list_path = songs_list_path
        self.save_to_dir = save_to_dir
        self.mixtape_title = mixtape_title
        self.determine_mixtape_path()
    
    # This method is invoked as the callback for pressing the "Create Mixtape" button
    # Instead of creating a new object for each mainloop iteration, an object is only created 
    # upon the click of the "Create Mixtape" button. 
    @staticmethod
    def create_instance(songs_list_path, save_to_dir, mixtape_title):
        return InputValidator(songs_list_path, save_to_dir, mixtape_title)

    def validate_input(self, root, state, songs_list_entry, dir_entry, title_entry):
        if self.has_empty_fields():
            state.configure(text = "Please fill all fields")
        elif not self.is_valid_path(self.songs_list_path.user_entry.get()):
            state.configure(text = "Invalid field entry : the specified path to the songs list does not exist")
        elif not self.is_valid_path(self.save_to_dir.user_entry.get()):
            state.configure(text = "Invalid field entry : the specified save-to directory does not exist")
        elif self.is_valid_path(self.mixtape_path):
            state.configure(text = "Invalid field entry : mixtape title conflicts with another directory in the path specified")
        else:
            try:
                total_songs = self.count_num_songs(self.songs_list_path.user_entry.get())
                os.mkdir(self.mixtape_path)
                MixtapeCreator.update(root, state, "Please Wait :     Creating... (0/{} songs successfully downloaded)".format(total_songs))
                unsuccessful_downloads = MixtapeCreator.read_songs_file(self.songs_list_path.user_entry.get(), self.mixtape_path, state, root, total_songs)
                self.determine_final_state(root, state, unsuccessful_downloads, total_songs)
            except Exception:
                state.configure(text = "Invalid field entry : mixtape title must not contain special characters")
    
    # update and display final state of the application based on output
    def determine_final_state(self, root, state, unsuccessful_downloads, total_songs):
        if len(unsuccessful_downloads) == 0:
            print("Your Mixtape Has Successfully Been Created!")
            MixtapeCreator.update(root, state, "Completed : All songs successfully downloaded!")
        else:
            if len(unsuccessful_downloads) == total_songs:
                print("Poor Internet Connection Prevented the Application from Executing!")
                MixtapeCreator.update(root, state, "Complete Failure : Poor internet connection prevented downloads")
                os.rmdir(self.mixtape_path)
            else:
                print("Your Mixtape Has Been Created!")
                MixtapeCreator.update(root, state, "Completed : Partial success (please view the \"Unsuccessful_Downloads.txt\"  file in the mixtape directory)")
                # create file with unsuccessful downloads in directory
                with open(self.mixtape_path + "/Unsuccessful_Downloads.txt", "w") as filehandle:
                    for song in unsuccessful_downloads:
                        filehandle.write("%s" % song)
        
    def determine_mixtape_path(self):
        self.mixtape_path = self.save_to_dir.user_entry.get() + '/' + self.mixtape_title.user_entry.get()

    def has_empty_fields(self):
        if self.songs_list_path.user_entry.cget("state") == tk.DISABLED or \
           self.save_to_dir.user_entry.cget("state") == tk.DISABLED or \
           self.mixtape_title.user_entry.cget("state") == tk.DISABLED:
            return True
        else:
            return False

    @staticmethod
    def is_valid_path(path_entered):
        if os.path.exists(path_entered):
            return True
        else:
            return False
    
    def count_num_songs(self, file_path):
        num_songs = 0
        file = open(file_path, "r")

        for line in file:
            if line == '\n' or line == "":
                continue
            num_songs += 1

        file.close()
        return num_songs


##################################################################################################################