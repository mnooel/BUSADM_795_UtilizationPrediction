# BUSADM_795_UtilizationPrediction
A project studying the capabilities of advanced analytics and data science to predict future utilization rates in an 
advertising service agency. 

Creator: Michael Noel Menomonee Falls WI
#
><h3>Major Components:</h3>
>
><ul>
><li>**database_access**: Python package with Connection objects.</li>
><li>**docs**: Directory used by engines. Data in .csv format is read from and placed here.</li>
><li>**logs**: Directory of python process and runtime logs.</li>
><li>**SQL**: Directory of .sql files utilized by engines to read queries.</li>
></ul>

#

<h5>database_access package</h5>  

>The database_access package contains a python file connections.py. 
>The main class of the file is the BaseConnection class, with built in methods to select and insert data into a database. 
>It has other methods as well such as to query meta data from the database. 
>It is used as the parent class of the following classes.  
>  
>The two other classes are database specific classes. For the project we are pulling from an erp database. 
>The SourceDbConnection connection is used for this db. 
>The user utilized to access the db in the connection is read only, but to be safe,
>this class was created with write_permission as false for redundancy. 
>The LiteDbConnection, is the connection used to read and write sql locally. 
>
>By pulling the data from the source and storing it locally I am able to give the data to my partner without giving him access to the entire erp database.

<h5>docs</h5>  

>The docs directory contains mostly .csv files used for reference or for datatype reference for columns.

<h5>logs</h5>  

>The logs directory just houses the log files from python. 
>These logs are mostly to assure that select and insert statements executed successfully.

<h5>project_scripts</h5>  
>The project scripts directory house... python scripts. 
>These scripts could be for anything from automating the migration of multiple tables over a period of time to performing analysis.

<h5>project_scripts</h5>

>The SQL directory is dedicated to housing .sql files. 
>These are utilized by the connections to make queries from the databases.
