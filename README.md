Comptrollers-Checkbook
======================
The Checkbook NYC 2.0 website provides unprecedented access to view and track how New York City government spends its nearly $70 billion annual budget. 
All data present in Checkbook NYC 2.0 is available through the API, except for visualizations. 
The API has 2 required global parameters and 2 optional global parameters in every request. 
Depending on the value used for type of data, there are additional optional parameters that can be sent. 
The XML formats will hopefully be fairly self-explanatory.  
Links are provided for documentation for contracts, spending, and payroll domains.  
The documentation consists of global parameters and domain specific parameters.  
Sample XML requests and responses are included for each domain.

=======================
<h3>Import The Library</h3>
<p><b>To use the included Python Library, you must first import it:</b><p>
<code>import Comptroller</code><br />
<p>If the library fails to import, make sure python is set to search the directory that the file is located in. Then restart python and try again.</p>


<h3> Create an object by entering a valid API ID/Key and choosing a datatype:</h3>
<code>Budget = Comptroller.Budget('API ID' , 'API Key') <br /></code>
<code>Contracts = Comptroller.Contracts('API ID', 'API Key')</code>


<h3>Changing the API Key or ID for a Comptroller object that was already created:</h3>
<code>object.setID('NewID')<br /></code>
<code>object.setKey('NewKey')</code>

<h3>Get the API Key/AID for a Comptroller object:</h3>
<code>object.getID('ID')<br /></code>
<code>object.getKey('Key')</code>


<h3>Setting a Criteria for an object:</h3>
<p>&nbsp;<b>Note:</b> You can add multiple criterias to a single object</p>

<p><b>Value Criterias:</b></p>
<code>object.add_criteria('criteria_name',value)<br /> </code>
<code>Budget.add_critera('max_records',1)</code>
<p><b>Range Criterias:</b></p>
<code>object.add_criteria('criteria_name',start,end)<br /></code>
<code>Budget.add_criteria('adopted',2100,35000)</code>


<h3>Setting a response column for an object:</h3>
<p>&nbsp;<b>Note:</b> You can add multiple response columns to a single object</p>
<code>object.add_response_column('name')<br /></code>
<code>Budget.add_response_column('agency')</code>

<h3>Deleting a response column:</h3>
<code>object.del_response_column('name')<br /></code>
<code>Budget.del_response_column('agency')</code>

<h3>Deleting a criteria:</h3>
<code>object.delete_criteria('name')<br /></code>
<code>Budget.delete_critera('adopted')</code>

<h3>Call to API for results(returned in text format):</h3>
<p>&nbsp;<b>Note:</b> The call depends on the datatype you selected when creating your object</p>
<code>MyBudgetObject.getBudget()</code><br />
<code>MyContractsObject.getContracts()</code><br />


<b>For further documentation and examples, see the integrated help Doc in python:</b><br />
<code>help(Comptroller) </code>





