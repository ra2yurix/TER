# iMovie
Project of the PFE in Polytech Nice Sophia.
___
Since we refactored the project, [here](https://github.com/Diengoumar/stagemam5) is the project link if you are interested in the previous project.  
[Here](https://drive.google.com/drive/folders/19YoMc7CGpPtam95ENyvWgcqu-RJC-Va4?usp=sharing) is the file share of the previous project.  
___
Our project is mainly used to search for movies by text, pictures, text and pictures.  
Steps to successfully run the project:
1. your `python version >= 3.7`.  
    If you want to successfully run this project with `python version < 3.7`, please see this [commit](https://github.com/ra2yurix/TER/commit/ecf2c0fb542cd1baa025e1795617060d230ff0e6), you need to add the deleted code back.
2. Download the python package needed written in `requirements.txt`.   
3. Add the data and trained feature (The [five documents](https://drive.google.com/drive/folders/1P2ra-xMXiF8gcFybTXjgZhVeSD-TTK_Z?usp=sharing) we share) in data folder.
4. Create database -> Run the python file:   
  `data/data_to_mongo.py`
6. Run the command in the terminal:   
  `python manage.py runserver`
