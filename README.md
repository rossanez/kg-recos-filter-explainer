# kg-recos-reranker-filter-explainer
ELSA-Compliant re-ranking, filtering, &amp; explaining KG-based recommendations using LLMs

# For re-ranking
```shell
$ python3 rerank.py kg-file.ttl recommendations.txt user-profile-kg-file.ttl
```
- Will output recommendations_reranked.txt

# For filtering:
```shell
$ python3 filter.py kg-file.ttl recomendations.txt
```
- Will output: recommendations_filtered.txt

# For explaining:
```shell
$ python3 explain.py kg-file.ttl recommendations_filtered.txt
```
- Will output: recommendations_filtered_explained_llama3-70b-8192_temp1.txt

# Alternatively, for batch processing with multiple LLM models and temperatures:
```shell
$ python3 pipeline.py kg-file.ttl recommendations.txt -m llama3-70b-8192,mixtral-8x7b-32768,gemma2-9b-it -t 0,1,2
```
- Will output the filtered recommendations file and all the explanation files for the passed in parameters

