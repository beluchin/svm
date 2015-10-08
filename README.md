# svm
Spartans video manager

Use this command line tool to rename videos in YouTube. The following subcommands are available: `rename`, `rename-many`, `undo`, and `reset-credentials`. The subcommands are invoked via the `svm.bat` command (or `svm` on a Mac) as in:

    svm.bat <subcommand> ...
    
Help messages are available for the tool and for each subcommand:

    svm.bat -h
    svm.bat rename -h
    
To rename a video, you need to provide the YouTube video id and the new title in a comma-separated pair:

    svm.bat rename the_video_id,the_new_title
    
If the new title has spaces, you would need to wrap the entire new title in quotes:

    svm.bat rename 98745lfgdklsf,'this new title has spaces'
    
Notice that you could use this command to rename multiple videos:

    svm.bat rename 9879ldjfH,'first video' kjgI0_984k,'the second video'
    
(btw, the new titles may not contain commas)

The first time you run the `rename` command, you will be directed to a webpage that will request permission to grant the tool access to your YouTube data for a specific account. Should you want to use the tool to rename videos stored under another account, you would first need to `reset-credentials` in which case the authorization flow will run again on the next `rename` subcommand:
    
    svm.bat reset-credentials

To rename many videos in one go, use the `rename-many` subcommand that takes as its single argument a text file of comma-separated pairs similar to the ones the `rename` subcommand takes (one pair per line in the text file; no need to quote the titles in the file if they contain commas):

    svm.bat rename-many /the/name/of/the/file
    
Finally, should you make a mistake, you could undo your last action with the `undo` subcommand. The `undo` subcommand takes no arguments and only supports reverting the titles of the videos referenced in the last rename action:

    svm.bat undo
