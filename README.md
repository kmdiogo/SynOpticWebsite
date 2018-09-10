# SynOptic Website
This repository contains all of the source code for SynOptic's official web service built in Django.
The repository holds all source files as well as project files associated with the PyCharm project (excluding venv). 

### INSTRUCTIONS FOR PUSHING TO MASTER - PLEASE READ BEFORE COMMITTING
* Please make sure that you do not add the goddamn virtual environment (venv) to the repo, there are so many fucking
(literally thousands) of files in there and it'd be a pain in the ass to manage them. It's better to just create the venv
from the included requirements.txt file if pulling from scratch
* Please for the love of fuck add a commit message. If I see any ghost committers on this shit I will track you down and commit my foot
in your ass
* Adhere to our coding standards. I'll write them in this readme file so you stupid ass fucks can refer to them. Look, it's literally
below this bullet point, so don't miss it

### CODING STANDARDS
Yeah so these standards are primarily for front-end files and shit. So listen up dickheads
1. Embed any page specific css and javascript in the html file for now
2. Any css that can be considered generic or applicable to more than page must be in site.css
3. Comment your fucking code. I don't want to see 10,000 lines of javascript with shitty variable names and terrible coding style without
comments. At least if you explain your rancid putrid pile of shit code, I can maybe understand it. Also, make sure you comment where
only it's necessary. I don't ever want to see this bullshit:
```javascript
var myCockLength = 12;   // Create a variable that holds the length of my dick in inches
```
Like holy shit I know what the fuck that line is doing, I don't need some random ass dickhead telling me how to assign values to a variable
