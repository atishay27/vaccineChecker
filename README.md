# vaccineChecker
Find vaccine availablity(18-43 yrs) in your district using this simple python script with a single click

<h2>PREREQUISITE</h2><br />

Python >= 3.6 <br />
Python Module: requests,datetime,json,pytz,random<br />
Module Installation Instructions<br />
<ul>
	<li>pip install requests</li>
	<li>pip install pytz</li>
	<li>pip install DateTime</li>
</ul>

<h2>Instructions</h2><br />
<ol>
	<li>Go to District-ID Folder</li>
	<li>Open text file of your state Eg: Karnataka.txt</li>
	<li>Find id of your district in the text file</li>
	<li>Open script.py in a text editor</li>
	<li>Edit 'dist_id' (line 86) list according to your district id (note 'dist_id' is a list hence you can use multiple district id's)</li>
	<li>Run the script using python IDLE</li>
</ol>


<h2>Tips</h2><br />
<ul>
	<li>Use dist_id = [294,265,276] for bengaluru</li>
</ul>

<h2>NOTE</h2><br />
<ul>
	<li>District-ID folder will be updated soon for all the states</li>
</ul>

<h3>This project is based on CoWin API</h3>
<h3>The National Health Authority (NHA) has opened up the APIs for vaccine</h3>
<h3>https://apisetu.gov.in/public/api/cowin</h3>