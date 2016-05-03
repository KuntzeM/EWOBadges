from distutils.core import setup
import py2exe

setup( 
     name = "Badge",
     version = "1.0", 
     author = "Micky Maus", 
     author_email = "micky@maus.de", 
     script_name = ["main.py"],
     data_files = ["kuntze/createBadges.py", "kuntze/createTextImage.py", "misc/images/fileopen.gif", "kuntze/oneBadge.py", "misc/fonts/agency-fb.ttf", "gui.py", "misc/images/start.gif"]
     )