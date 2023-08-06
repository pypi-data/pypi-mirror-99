# European Language Grid Python SDK

The [**European Language Grid**](https://live.european-language-grid.eu/) is the primary platform for Language Technology in Europe. With the ELG Python SDK, you can use LT services and search the catalog inside your Python projects.

## Installation

**Via pip / PyPI**
```bash
pip install elg
```

### Register on the ELG

Please visit the [ELG website](https://live.european-language-grid.eu/catalogue/#/) to create a user account if you haven't got one already.


## Functionalities

### Use LTs

#### Initialize LT service

LT Services can be initialized as `Service` objects using the `service_id` parameter and an integer corresponding to the LT service you want to use.  
In the following code example, `474` corresponds to the [Cogito Discover Named Entity Recognizer](https://live.european-language-grid.eu/catalogue/#/resource/service/tool/474) (notice the ID at the end of the URL). For more LT services, search the catalog via the `Catalog` functionality (see section below) or visit the [list of LT services on the ELG](https://live.european-language-grid.eu/catalogue/#/?resource_type__term=Tool/Service).

```python
from elg import Service

# Init LT service using its ID
lt = Service.from_id(474)
```
This requires you to login to your ELG account via the URL that is printed on your terminal.

![ELG Login](elg-login.png)

After successful login, your tokens are saved as `~/.cache/elg/tokens.json`, so you do not need to log in again for subsequent calls. 

#### Run LT service

You can either pass an input file or a string / raw text.

```python
# Pass an input file that should be processed by the LT service
result = lt("path/to/file")

# You can also directly pass raw text to the LT service in most cases
result = lt("Did Nikola Tesla live in Berlin?")
```

### Use corpus

```python
from elg import Corpus

corpus = Corpus.from_id(913)
corpus.download()
```

### Use the catalog

```python
from elg import Catalog

catalog = Catalog()

# Search and get the result as a list of Entity
results = catalog.search(
    resource = "Tool/Service", # "Corpus", "Lexical/Conceptual resource" or "Language description"
    function = "Machine Translation", # function should be pass only if resource is set to "Tool/Service"
    languages = ["en", "fr"], # string or list if multiple languages
    limit = 100,
)

# search interactively 
catalog.interactive_search(
    search = "keyword1 keyword2 ...",
    resource = "Tool/Service", # "Corpus", "Lexical/Conceptual resource" or "Language description"
    function = "Machine Translation", # function should be pass only if resource is set to "Tool/Service"
    languages = ["en", "fr"], # string or list if multiple languages
)
```

### Create a LT service object from the results

```python
service = Service.from_entity(results[0])
result = service("Did Nikola Tesla live in Berlin?")
```

### Get info of an entity

```python
from elg import Entity

entity = Entity.from_id(476)
print(entity)
```

### Benchmark

You can also run a benchmark that evaluates multiple services receiving the same input:

```python
from elg import Benchmark

ben = Benchmark.from_ids([610, 624])

result = ben(["Bush is the president of the USA and lives in Washington", "My name is Rémi and I live in France"], number_of_runs=4)

df = result.compare()
print("General comparison:\n", df)
df = result.compare_results()
print("Comparison of the results:\n", df)
df = result.compare_response_times()
print("Comparison of the response time:\n", df)
```

You can investigate the results by saving the output from the `bench` call to a variable or by accessing `bench.services`.

### CLI

```bash
elg-cli search *term1* *term2* ... *termN* --lang "" --resource "" --function ""
elg-cli info *id*
elg-cli run *id* --authentication_file path/to/tokens.json --data_file path/to/file
```