# Updating Bemyagent in Existing Projects

## The Idea
Define the workflow for updating the Bemyagent protocol in a project that has already been bootstrapped. 

Once a project has its own `.bemyagent` folder with customized rules, documentation, and history, how do we safely introduce new updates from the core Bemyagent protocol? We need to understand how this update phase should function.

## Goal
Establish a clear update mechanism or lifecycle process that allows pulling in new features, rule modifications, or structural changes to the protocol without overriding or destroying the project-specific context, drift sensors, and customizations already in place.

## Original Notes (Italian)
aggiungi anche un punto sull'update di bemyagent per un progetto esistente vorrei capire come deve funzioanre quella fase quando il bootstrap è già stato fatto

## Case Study: File Loss During Update (Manual Enumeration Anti-Pattern)

**Il problema è stato questo:**

Durante lo Step 0 ho fatto una scansione della struttura, ma invece di usare `cp -r docs/ .bemyagent/docs/` (che avrebbe copiato tutto in modo deterministico), ho scelto di elencare i file manualmente uno per uno. Questo è un pattern pericoloso perché dipende dalla mia capacità di ricordare/enumerare correttamente tutti i file visti durante la scansione.

**In particolare:**
- Ho letto `docs/` con listDirectory o simile
- Ho visto tutti i file incluso `kahoot-private-import.md`
- Ma quando ho scritto i comandi `cp`, ho ricostruito la lista a memoria invece di derivarla meccanicamente dall'output della scansione
- Il file è caduto fuori dalla lista

Non è allucinazione in senso stretto (non ho inventato nulla), è *omissione per ricostruzione manuale* — un errore classico quando un agente "traduce" un elenco osservato in azioni invece di usare un'operazione atomica che agisce sull'intero insieme.

**Suggerimento per BEMYAGENT:** Nello Step 1 (Create Directories) e Step 3 (Generate Scaffold), se esiste documentazione preesistente da migrare, il protocollo dovrebbe esplicitamente prescrivere operazioni atomiche (`cp -r`, `mv`) invece di lasciare all'agente la discrezione di enumerare i file manualmente.

## Handling Filename Collisions

Un altro problema cruciale durante l'aggiornamento o il bootstrap su un progetto preesistente è la gestione delle collisioni nei nomi dei file, in particolare con la documentazione numerata.

**Esempio:**
In un progetto, l'utente potrebbe aver già creato dei file numerati per le proprie specifiche (es. `06-quize-editor.md`). Quando si applica l'aggiornamento di Bemyagent, che utilizza anch'esso una rigida struttura numerata per i propri file (es. `00-ai-rules.md`, `01-system-prompt.md`, ecc.), c'è il rischio di:
1. Sovrascrivere i file originali dell'utente.
2. Inserire file del protocollo in mezzo alla logica di ordinamento dell'utente, creando confusione.

**Soluzioni da integrare:**
- **Verifica e Salvaguardia:** Prima di copiare i nuovi file di base del protocollo, l'agente DEVE scansionare la cartella di destinazione alla ricerca di conflitti sui nomi.
- **Isolamento:** La documentazione utente (progetto) e quella di protocollo (bemyagent) dovrebbero avere una chiara separazione, possibilmente in sotto-cartelle distinte o usando un namespace che eviti ogni sovrapposizione.
- **Risoluzione sicura:** In caso di collisione (es. la cartella destinazione è "piatta" e contiene già un `06-quize-editor.md` e bemyagent sta per creare un `06-...`), l'agente non deve mai sovrascrivere i file utente, ma deve interrompersi per chiedere conferma o spostare i file in conflitto in modo sicuro (es. re-indicizzandoli o inserendoli in una cartella `archived/` o `project_docs/`).
