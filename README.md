# fs_dorms
<p>Automate closing the Pisciners accounts who didn't pass initial inspection. (GoogleSheets &amp; 42 APIs)</p>

<b>Last minute</b> README here (i.e. first draft):

*<b> Make sure RA's use the correct spreadsheet shared to RA drive</b>*

*<b> Final column of spreadsheet defining whether account is closed or not currently must be filled out by RA's with
      -- 'n' or 'y' after each inspection before running script.</b>*

1. Inside main.py function - ‘close_request()’ :<br /> 
    <p>In ‘payload’ dictionary:<br /></p> 
      <p><b>Replace ‘closer_id’ int value w/ your closer_id.</b></p> 

2. In your shell’s environment variables, create variables 'FT_SECRET' and 'FT_CLIENT' for your 42 api secret and client id 
   -- created from intra app that gives you roles and access to 42 api. The script will use the os python library to pull those variables from the shell.

3. Your 42 api app must have <b>‘Basic Staff’</b> and <b>'tig’ scope</b> must be set.


