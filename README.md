# svm
Spartans swim team video manager

Use this command line tool to rename/get lists of videos in YouTube. The available subcommands are listed on the tool help message:

    svm.bat -h
    
The help message for the subcommands themselves is available via:

    svm.bat <subcommand> -h
    
You may rename videos in a playlist with the `rename-in-playlist` subcommand. The subcommand takes in as arguments the **playlist id** and a file of comma-separated old-to-new title mappings (one mapping per line):

    svm.bat rename-in-playlist <playlistId> /the/path/to/the/file/with/mappings

Notice that the playlist id can be extracted from the playlist url. Given the playlist URL:

    https://www.youtube.com/playlist?list=PL-gKBqMRNkt53ia4nVwanw_mrk1MDsI8J
    
the id is `PL-gKBqMRNkt53ia4nVwanw_mrk1MDsI8J`.

The subcommand `link-to-title` can be used to get the mappings of links from a playlist:

    smv.bat link-to-title <playlistId>
    
It displays the mapping on the console. To redirect the output to a file:

    smv.bat link-to-title <playlist> > /the/output/file

Please, refer to the list of subcommands on the tool's help message for further info.

The first time you run a subcommand that access YouTube, you will be directed to a webpage that will request permission to grant the tool access to your YouTube data for a specific account. Further operations will act upon the data pertaining to that account the tool was granted access to. 

Should you want to use the tool to manage videos stored under another account, you would first need to `reset-credentials` in which case the authorization flow will run again on the next subcommand that accesses YouTube:
    
    svm.bat reset-credentials

Finally, should you make a mistake, you could undo your last rename action with the `undo` subcommand. The `undo` subcommand takes no arguments and only supports reverting the titles of the videos that got renamed in the last rename action:

    svm.bat undo
