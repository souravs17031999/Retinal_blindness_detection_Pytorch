## Installation :     
Tip : Make sure to install [Numpy](https://pypi.org/project/numpy/), [Pandas](https://pypi.org/project/pandas/), [Matplotlib](https://pypi.org/project/matplotlib/) first and then proceed next.     
* [Torch package](https://pytorch.org/get-started/locally/)    
* [Tkinter](https://tkdocs.com/tutorial/install.html)     
* [HeidiSQL](https://www.heidisql.com/download.php)          
Grab a cup of coffee as these will take some time !   
* [click here](https://support.hypernode.com/knowledgebase/use-heidisql/#Download_HeidiSQL) to start server in HeidiSQL and configure settings by setting username and password.    
## Get, set and go :   
* Create a new database and table accordingly.    
* Then, Go to 'blindness.py' file and change some configuration settings according to your database.
```
connection = sk.connect(
    host="localhost",
    user="root",
    password="********",
    database="********"
)
```
* Now, your DB server must be connected.   
* Finally, you also want 'classifier.pt' file which contains model's dictionery required when it is to be loaded.    
(since, it's a large file you can mail me if you want that file at this id : souravs_1999@rediffmail.com) and put that file in the same directory and then modify the path accordingly in the 'model.py' file.
```
model = load_model('../Desktop/classifier.pt')

```
