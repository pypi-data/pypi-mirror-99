# High level description

This tool will 
1. Take in a set of provided data, or use input.json in its place
2. Read in a set of available enrichment REST endpoints, with POST or GET structure defined
3. Read in a set of steps to follow, to call multiple enrichment providers in parallel, serial, percentage,
or fallback means
4. Read in mapping XML, which will take the input data (step 1) and convert it into what the various REST endpoints
need (step 2).
5. Read in outbound mapping XML, which will take the data that comes back from the enrichment tools (step 2) and map
it to data that is named what a customer would expect as output
6. Follows the steps defined (step 3), with the input data (step 1).
   - For each step, 
      - For each enrichment called, map the incoming data to what the rest call needs.  Call the rest interface
      - On failure, capture the failure in the results
      - On success, capture the data that comes back. Map it to the variable names as defined in step 5
7. Return back the set of data from each of the enrichment providers, remapped as requested, to the caller

# Requirements
* pip install requests
* python -m pip install --upgrade pip
