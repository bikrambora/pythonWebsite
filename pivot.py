import cgi
import csv
import sqlite3
import math
import sys
conn = sqlite3.connect('proj7.db')

#SQL DB QUERY GENERATOR
def sql_query(rowField, colField, filter, fVal):
    #BUILD THE QUERY
    c = conn.cursor()
    c.execute('SELECT DISTINCT '+ rowField + ' FROM cancer')
    rows=c.fetchall()
    c.execute('SELECT DISTINCT '+ colField + ' FROM cancer')
    cols=c.fetchall()
    stmt="SELECT "
    stmt+=rowField+" , "

    '''
    stmt2='SELECT Cancer FROM cancer Where EXISTS (SELECT Cancer  FROM cancer WHERE Cancer="Bla" COLLATE NOCASE)'
    c.execute(stmt2)
    value=c.fetchall()
    '''
    
    #CHECKING IF THE FILTER FIELD IS EMPTY
    if fVal != None:
        if(colField!=filter):
            for colCell in cols:
                stmt+="SUM(CASE WHEN "+str(colField)+"="+"'"+str(colCell[0])+"'"+ " THEN no_of_cases END), "
            stmt=stmt[0:len(stmt)-2] 
            stmt+="from cancer "
            stmt+=" where "+filter+"="+"'"+fVal+"'"+" COLLATE NOCASE"
            stmt+=" GROUP BY "+rowField
        else:
            stmt+="SUM(CASE WHEN "+str(filter)+"="+"'"+str(fVal)+"'"+ " THEN no_of_cases END), "
            stmt=stmt[0:len(stmt)-2] 
            stmt+="from cancer "
            stmt+=" GROUP BY "+rowField
    else:
        for colCell in cols:
            stmt+="SUM(CASE WHEN "+str(colField)+"="+"'"+str(colCell[0])+"'"+ " THEN no_of_cases END), "
        stmt=stmt[0:len(stmt)-2] 
        stmt+="from cancer "
        stmt+=" GROUP BY "+rowField
    c.execute(stmt)
    
    #WRITING QUERY OUTPUT TO CSV
    f = open('Graphs/data.csv','w');
    lines=c.fetchall()
    f.write(rowField)

    #FILTER CHECKING
    if(colField!=filter or ((colField==filter) and (fVal==None))):
        for colCell in cols:
            f.write(","+str(colCell[0]))
    elif(fVal!=None):
        f.write(","+str(fVal))
    
    f.write('\n')
    writer = csv.writer(f)
    for line in lines:
        writer.writerow(line)
    
    f.close()
    conn.close()       
    return stmt

#PIVOT TABLE BUILDER
def pivot_table (sql_str):
    input_file = csv.reader(open("Graphs/data.csv", "rU"))
    header = input_file.next()
    color = ['#FF6109', '#F5670A', '#EB6E0C', '#E1750E', '#D77C10', '#CD8312', '#C38A14', '#B99116', '#AF9818', '#A59F1A', '#9BA61C', '#91AD1E', '#87B420', '#7DBB22', '#73C224', '#69C926', '#5FD028', '#55D72A', '#4BD32C', '#41E52E']

    print 'Content-Type: text/html\n'
    print '''<html>
               <head>     
                   <link href="http://fonts.googleapis.com/css?family=Open+Sans:400,600,700" rel='stylesheet' type='text/css'>
                   <link href="bootstrap-3.3.4-dist/css/bootstrap.css" rel="stylesheet">
                   <link href="style.css" rel="stylesheet">
                   <title>Data Spectrum</title>
               </head>
           <body>
               <div id="holder">


               <nav class="navbar navbar-default">
                   <div class="container">
                       <ul class="nav navbar-nav pull-right">
                           <li><a href="home.html"><span class="glyphicon glyphicon-home"></span> Home</a></li>
                           <li><a href="observations.html"><span class="glyphicon glyphicon-list-alt"></span> Observations</a></li>
                           <li class="active"><a href="pivot.html"><span class="glyphicon glyphicon-stats"></span> Pivot Table</a></li>
                            
                       </ul>
                   </div>
               </nav>
               <div id="body">
               <div class="pivot-title"></div>
               <div class = "container-fluid">'''

    #No filter value given
    if fVal == None:
        print '<h3 class="title">Pivot Table for '+rowField+' and '+colField+'</h3>'
    else:
        print '<h3 class="title">Pivot Table for '+rowField+' and '+colField+' if ' +filter+' = '+fVal+'</h3>'
    
    print '    <div class="row"><a href="pivot_graph.html" class="btn btn-default col-md-2 col-sm-offset-5">Visualizer</a></div>'
    print '    <table class="table-borderless center-table">'

    #Read values from csv into list
    #finds max and min
    #and calculates the interval that one colour spans

    values = []
    inList = []
    for row in input_file:
        inList.append(row)
        for colume in row[1:]:
            values.append(float(colume))
    values.sort(reverse=True)

    max = values[0]
    min = values[-1]
    diff = max - min
    interval = diff/len(color)

    #Make headings
    print '<thead>'
    print '<tr>'
    header[0] = ''
    for i in header:
        print'<th>'+i+'</th>'
    print '</tr>'
    print '</thead>'


    #Draw table and assign colors
    #Can only handle numbers
    print '<tbody>'
    for row in inList:
        print '<tr>'
        #row[0] will be the row header
        print '<th>' + row[0] + '</th>'
        for colume in row[1:]:
        
            for i in range(len(color)+1):
                if i == 0 and (float(colume) <= (i * interval + min)):
                    print '<td style = "background-color: '+color[i] + '"''>' + str(colume) + '</td>'
                    break
                elif float(colume) <= (i * interval + min):
                    print '<td style = "background-color: '+color[i-1] + '"''>' + str(colume) + '</td>'
                    break
        print '</tr>'

    print '''        </tbody>
            </table>
        </div>
        
        <sql class="sql">
            <div class="container">
                <div class="row">
                    <div class="well col-sm-12">
                        <p>SQL query:</p>
                        <p>'''+sql_str+'''</p>
            </div></div></div></sql></div>
                    
        <footer class="footer">
            <div class="container">
                <div class="row vcenter">
                    <div class="col-sm-3">
                        <p>Data Spectrum</p>
                    </div>
                    <div class="col-sm-6">
                        <p>by Bikram Bora, Kim Liew and Michael Lumley</p>
                    </div>
                    <div class="col-sm-3">
                        <p>Made for Foundations of Infomatics</p>
                    </div>
                </div>
            </div>
        </footer>
        </div>
    </body>
    </html>'''

#Main code
form = cgi.FieldStorage()
rowField = form.getvalue("row")
colField = form.getvalue("colume")
filter = form.getvalue("filter")
fVal = form.getvalue("fVal")

if(fVal!= None):
    c = conn.cursor()
    stmt2='SELECT Cancer  FROM cancer WHERE '+filter+'="'+str(fVal)+'" COLLATE NOCASE'
    c.execute(stmt2)
    value=c.fetchall()
    
    if(len(value)==0):
    
        print 'Content-Type: text/html\n'
        print '''<html>
               <head>     
                   <link href="http://fonts.googleapis.com/css?family=Open+Sans:400,600,700" rel='stylesheet' type='text/css'>
                   <link href="bootstrap-3.3.4-dist/css/bootstrap.css" rel="stylesheet">
                   <link href="style.css" rel="stylesheet">
                   <title>Data Spectrum</title>
               </head>
           <body>
               <div id="holder">


               <nav class="navbar navbar-default">
                   <div class="container">
                       <ul class="nav navbar-nav pull-right">
                           <li><a href="home.html">Home</a></li>
                           <li><a href="visualisations.html">Observations</a></li>
                           <li class="active"><a href="pivot.html">Pivot Table</a></li>
                            
                       </ul>
                   </div>
               </nav>
               <div id="body">'''
        print '''
        <error class="sql">
            <div class="container">
                <div class="row">
                    <div class="well col-sm-12">
                        <p>Error:</p>
                        <p>Filter value invalid not present in database leave empty for no filter</p>
            </div></div></div></sql></div>
<h1 class="title">Pivot Table</h1>
        
        <form action="pivot.py" method="get">
            
            <div class="row">
                <div class="col-sm-3 col-sm-offset-3">
                    <label class="sel1">Row</label>
                        <select class="form-control" name="row">
                            <option>Cancer</option>
                            <option>Year</option>
                            <option>Sex</option>
                            <option>Nature</option>
                        </select>
                    </div>
                
                <div class="col-sm-3">
                    <label class="sel1">Column</label>
                        <select class="form-control" name="colume">
                            <option>Year</option>
                            <option>Sex</option>
                            <option>Nature</option>
                        </select>
                </div>

                
            </div>

            <div class="row">
                <div class="col-sm-3 col-sm-offset-3">
                    <label class="sel2">Filter</label>
                        <select class="form-control" name="filter">
                            <option>Cancer</option>
                            <option>Year</option>
                            <option>Sex</option>
                            <option>Nature</option>
                        </select>
                        <input class="form-control" placeholder="Filter Value" name="fVal" id="fVal">
                </div>
            </div>
            
            <div class="row">
                <button type="submit" class="btn btn-default col-md-2 col-sm-offset-5">Submit</button> 
            </div>
        </form>
        </div>
         <footer class="footer">
            <div class="container">
                <div class="row vcenter">
                    <div class="col-sm-3">
                        <p>Data Spectrum</p>
                    </div>
                    <div class="col-sm-6">
                        <p>By Bikram Bora, Kim Liew and Michael Lumley</p>
                    </div>
                    <div class="col-sm-3">
                        <p>Made for Foundations of Infomatics</p>
                    </div>
                </div>
            </div>
        </footer>
        </div>
    </body>
    </html>''' 


#Check if input is vaild
if rowField != colField:
    sql_str = sql_query(rowField, colField, filter, fVal)
    pivot_table(sql_str)
else:
    print 'Content-Type: text/html\n'
    print '''<html>
               <head>     
                   <link href="http://fonts.googleapis.com/css?family=Open+Sans:400,600,700" rel='stylesheet' type='text/css'>
                   <link href="bootstrap-3.3.4-dist/css/bootstrap.css" rel="stylesheet">
                   <link href="style.css" rel="stylesheet">
                   <title>Data Spectrum</title>
               </head>
           <body>
               <div id="holder">


               <nav class="navbar navbar-default">
                   <div class="container">
                       <ul class="nav navbar-nav pull-right">
                           <li><a href="home.html">Home</a></li>
                           <li><a href="visualisations.html">Observations</a></li>
                           <li class="active"><a href="pivot.html">Pivot Table</a></li>
                            
                       </ul>
                   </div>
               </nav>
               <div id="body">'''
    print '''
    <error class="sql">
            <div class="container">
                <div class="row">
                    <div class="well col-sm-12">
                        <p>Error:</p>
                        <p>Row and Column can't be the same</p>
            </div></div></div></sql></div>
<h1 class="title">Pivot Table</h1>
        
        <form action="pivot.py" method="get">
            
            <div class="row">
                <div class="col-sm-3 col-sm-offset-3">
                    <label class="sel1">Row</label>
                        <select class="form-control" name="row">
                            <option>Cancer</option>
                            <option>Year</option>
                            <option>Sex</option>
                            <option>Nature</option>
                        </select>
                    </div>
                
                <div class="col-sm-3">
                    <label class="sel1">Column</label>
                        <select class="form-control" name="colume">
                            <option>Year</option>
                            <option>Sex</option>
                            <option>Nature</option>
                        </select>
                </div>

                
            </div>

            <div class="row">
                <div class="col-sm-3 col-sm-offset-3">
                    <label class="sel2">Filter</label>
                        <select class="form-control" name="filter">
                            <option>Cancer</option>
                            <option>Year</option>
                            <option>Sex</option>
                            <option>Nature</option>
                        </select>
                        <input class="form-control" placeholder="Filter Value" name="fVal" id="fVal">
                </div>
            </div>
            
            <div class="row">
                <button type="submit" class="btn btn-default col-md-2 col-sm-offset-5">Submit</button> 
            </div>
        </form>
        </div>
        <footer class="footer">
            <div class="container">
                <div class="row vcenter">
                    <div class="col-sm-3">
                        <p>Data Spectrum</p>
                    </div>
                    <div class="col-sm-6">
                        <p>By Bikram Bora, Kim Liew and Michael Lumley</p>
                    </div>
                    <div class="col-sm-3">
                        <p>Made for Foundations of Infomatics</p>
                    </div>
                </div>
            </div>
        </footer>
        </div>
    </body>
    </html>'''













