
## Setting up the environment

The project uses [uv](https://github.com/astral-sh/uv) as a package
manager. Follow the [installation instructions](https://docs.astral.sh/uv/getting-started/installation/) to have uv available on your machine.



```python

```

## Documentation

To build the documentation locally, run the following command:
```
uv run --group docs mkdocs serve
```
The local build is served at port [8000](http://127.0.0.1:8000/).

When you would like to cite a specific part of the AI Act, you can use the 
following format in MarkDown:

```MarkDown
|Art. 6|, |Article 13.3 (ii)|, |Annex II|, |Recital 23|
```

In case there is a wrong format in the citation 
(e.g. missing a whitespace |Art.6|). The console will log a UserWarning

![ai_act_cite_user_warning.png](docs/assets/ai_act_cite_user_warning.png)

and in the local build, you will see something like this

<img src="docs/assets/ai_act_cite_user_warning_build.png" alt="drawing" width="300"/>




