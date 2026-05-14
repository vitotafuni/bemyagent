# Proportional Compression Rule for Token Efficiency

## The Idea
The Contextual DNA Mapping (CDM) should impose a rule of "Proportional Compression". 

For low-complexity tasks (e.g., Level 1 out of 5), the output for `01_think.md` and `04_verify.md` files must be strictly limited by the agent to a maximum of 1-2 lines of text or an ultra-synthetic metadata table. 

## The Problem
Asking the agent to write a full `01_think.md` file and a full `04_verify.md` file for every single task consumes a high amount of output tokens (which are the most expensive). If a task merely involves correcting a typo in a CSS file, spending 500 "reflection" tokens and 500 "verification" tokens makes the system economically inefficient.

## Original Notes (Italian)
Il problema: Chiedere all'agente di scrivere un intero file 01_think.md e un intero file 04_verify.md per ogni singolo task consuma comunque molti token di output (che sono i più costosi). Se un task consiste nel correggere un typo in un file CSS, spendere 500 token di "riflessione" e 500 di "verifica" rende il sistema economicamente inefficiente.
Como correggerlo: Il tuo CDM (Contextual DNA Mapping) deve imporre una regola di "Compressione Proporzionale". Se il task ha un livello di complessità basso (es. Livello 1 su 5), i file _think e _verify devono essere limitati dall'agente a un massimo di 1-2 righe di testo o a una tabella di metadati ultra-sintetica.
