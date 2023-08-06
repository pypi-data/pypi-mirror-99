
.. rdf2vec-begin

What is RDF2Vec?
----------------

RDF2Vec is an unsupervised technique that builds further on
`Word2Vec <https://en.wikipedia.org/wiki/Word2vec>`__, where an
embedding is learned per word, in two ways:

1. **the word based on its context**: Continuous Bag-of-Words (CBOW);
2. **the context based on a word**: Skip-Gram (SG).

To create this embedding, RDF2Vec first creates "sentences" which can be
fed to Word2Vec by extracting walks of a certain depth from a Knowledge
Graph.

This repository contains an implementation of the algorithm in "RDF2Vec:
RDF Graph Embeddings and Their Applications" by Petar Ristoski, Jessica
Rosati, Tommaso Di Noia, Renato De Leone, Heiko Paulheim
(`[paper] <http://semantic-web-journal.net/content/rdf2vec-rdf-graph-embeddings-and-their-applications-0>`__
`[original
code] <http://data.dws.informatik.uni-mannheim.de/rdf2vec/>`__).

.. rdf2vec-end
.. getting-started-begin

Getting Started
---------------

For most uses-cases, here is how ``pyRDF2Vec`` should be used to generate
embeddings and get literals from a given Knowledge Graph (KG) and entities:

.. code:: python

   import pandas as pd

   from pyrdf2vec import RDF2VecTransformer
   from pyrdf2vec.embedders import Word2Vec
   from pyrdf2vec.graphs import KG
   from pyrdf2vec.walkers import RandomWalker

   data = pd.read_csv("samples/countries-cities/entities.tsv", sep="\t")
   entities = [entity for entity in data["location"]]
   print(entities)
   # [
   #    "http://dbpedia.org/resource/Belgium",
   #    "http://dbpedia.org/resource/France",
   #    "http://dbpedia.org/resource/Germany",
   # ]

   transformer = RDF2VecTransformer(
       Word2Vec(iter=10),
       walkers=[RandomWalker(4, 10, n_jobs=2)],
       # verbose=1
   )
   embeddings, literals = transformer.fit_transform(
       KG(
           "https://dbpedia.org/sparql",
           skip_predicates={"www.w3.org/1999/02/22-rdf-syntax-ns#type"},
           literals=[
               [
                   "http://dbpedia.org/ontology/wikiPageWikiLink",
                   "http://www.w3.org/2004/02/skos/core#prefLabel",
               ],
               ["http://dbpedia.org/ontology/humanDevelopmentIndex"],
           ],
       ),
       entities
   )
   print(embeddings)
   # [
   #     array([ 1.5737595e-04,  1.1333118e-03, -2.9838676e-04,  ..., -5.3064007e-04,
   #             4.3192197e-04,  1.4529384e-03], dtype=float32),
   #     array([-5.9027621e-04,  6.1689125e-04, -1.1987977e-03,  ...,  1.1066757e-03,
   #            -1.0603866e-05,  6.6087965e-04], dtype=float32),
   #     array([ 7.9996325e-04,  7.2907173e-04, -1.9482171e-04,  ...,  5.6251377e-04,
   #             4.1435464e-04,  1.4478950e-04], dtype=float32)
   # ]

   print(literals)
   # [
   #     [('1830 establishments in Belgium', 'States and territories established in 1830',
   #       'Western European countries', ..., 'Member states of the Organisation
   #       internationale de la Francophonie', 'Member states of the Union for the
   #       Mediterranean', 'Member states of the United Nations'), 0.919],
   #     [('Group of Eight nations', 'Southwestern European countries', '1792
   #       establishments in Europe', ..., 'Member states of the Union for the
   #       Mediterranean', 'Member states of the United Nations', 'Transcontinental
   #       countries'), 0.891]
   #     [('Germany', 'Group of Eight nations', 'Articles containing video clips', ...,
   #       'Member states of the European Union', 'Member states of the Union for the
   #       Mediterranean', 'Member states of the United Nations'), 0.939]
   #  ]

In a more concrete way, we provide a blog post with a tutorial on how to use
``pyRDF2Vec`` `here
<https://towardsdatascience.com/how-to-create-representations-of-entities-in-a-knowledge-graph-using-pyrdf2vec-82e44dad1a0>`__.

**NOTE:** this blog uses an older version of ``pyRDF2Vec``, some commands need
be to adapted.

If you run the above snippet, you will not necessarily have the same
embeddings, because there is no conservation of the random determinism, however
it remains possible to do it (**SEE:** `FAQ <#faq>`__).

Installation
~~~~~~~~~~~~

``pyRDF2Vec`` can be installed in two ways:

1. from `PyPI <https://pypi.org/project/pyrdf2vec>`__ using ``pip``:

.. code:: bash

   pip install pyRDF2vec

2. from any compatible Python dependency manager (e.g., ``poetry``):

.. code:: bash

   poetry add pyRDF2vec

Introduction
~~~~~~~~~~~~

To create embeddings for a list of entities, there are two steps to do
beforehand:

1. **use a KG**;
2. **define a walking strategy**.

For more elaborate examples, check the `examples
<https://github.com/IBCNServices/pyRDF2Vec/blob/master/examples>`__ folder.

If no sampling strategy is defined, ``UniformSampler`` is used. Similarly for
the embedding techniques, ``Word2Vec`` is used by default.

Use a Knowledge Graph
~~~~~~~~~~~~~~~~~~~~~

To use a KG, you can initialize it in three ways:

1. **From a endpoint server using SPARQL**:

.. code:: python

   from pyrdf2vec.graphs import KG

   # Defined the DBpedia endpoint server, as well as a set of predicates to
   # exclude from this KG and a list of predicate chains to fetch the literals.
   KG(
       "https://dbpedia.org/sparql",
       skip_predicates={"www.w3.org/1999/02/22-rdf-syntax-ns#type"},
       literals=[
           [
               "http://dbpedia.org/ontology/wikiPageWikiLink",
               "http://www.w3.org/2004/02/skos/core#prefLabel",
           ],
           ["http://dbpedia.org/ontology/humanDevelopmentIndex"],
        ],
    ),

2. **From a file using RDFLib**:

.. code:: python

   from pyrdf2vec.graphs import KG

   # Defined the MUTAG KG, as well as a set of predicates to exclude from
   # this KG and a list of predicate chains to get the literals.
   KG(
       "samples/mutag/mutag.owl",
       skip_predicates={"http://dl-learner.org/carcinogenesis#isMutagenic"},
       literals=[
           [
               "http://dl-learner.org/carcinogenesis#hasBond",
               "http://dl-learner.org/carcinogenesis#inBond",
           ],
           [
               "http://dl-learner.org/carcinogenesis#hasAtom",
               "http://dl-learner.org/carcinogenesis#charge",
           ],
       ],
   ),

3. **From scratch**:

.. code:: python

   from pyrdf2vec.graphs import KG, Vertex

    GRAPH = [
        ["Alice", "knows", "Bob"],
        ["Alice", "knows", "Dean"],
        ["Dean", "loves", "Alice"],
    ]
    URL = "http://pyRDF2Vec"
    CUSTOM_KG = KG()

    for row in GRAPH:
        subj = Vertex(f"{URL}#{row[0]}")
        obj = Vertex((f"{URL}#{row[2]}"))
        pred = Vertex((f"{URL}#{row[1]}"), predicate=True, vprev=subj, vnext=obj)
        CUSTOM_KG.add_walk(subj, pred, obj)

Define Walking Strategies With Their Sampling Strategy
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

All supported walking strategies can be found on the
`Wiki
page <https://github.com/IBCNServices/pyRDF2Vec/wiki/Walking-Strategies>`__.

As the number of walks grows exponentially in function of the depth,
exhaustively extracting all walks quickly becomes infeasible for larger
Knowledge Graphs. In order to avoid this issue, `sampling strategies
<http://www.heikopaulheim.com/docs/wims2017.pdf>`__ can be applied. These will
extract a fixed maximum number of walks per entity and sampling the walks
according to a certain metric.

For example, if one wants to extract a maximum of 10 walks of a maximum depth
of 4 for each entity using the random walking strategy and Page Rank sampling
strategy, the following code snippet can be used:

.. code:: python

   from pyrdf2vec.samplers import PageRankSampler
   from pyrdf2vec.walkers import RandomWalker

   walkers = [RandomWalker(4, 10, PageRankSampler())]

.. getting-started-end

Speed up the Extraction of Walks
--------------------------------

The extraction of walks can take hours, days if not more in some cases. That's
why it is important to use certain attributes and optimize ``pyRDF2Vec``
parameters as much as possible according to your use cases.

This section aims to help you to set up these parameters with some advice.

Configure the ``n_jobs`` attribute to use multiple processors
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

By default multiprocessing is disabled (``n_jobs=1``). If your machine allows
it, it is recommended to use multiprocessing by incrementing the number of
processors used for the extraction of walks:

.. code:: python

   from pyrdf2vec.walkers import RandomWalker

   RDF2VecTransformer(walkers=[RandomWalker(4, 10, n_jobs=4)])

In the above snippet, the random walking strategy will use 4 processors to
extract the walks, whether for a local or remote KG.

**WARNING: using a large number of processors may violate the policy of some
SPARQL endpoint servers**. This being that using multiprocessing means that
each processor will send a SPARQL request to one server to fetch the hops of
the entity it is processing. Therefore, since these requests may take place in
a short time, this server could consider them as a Denial-Of-Service attack
(DOS). Of course, these risks are multiplied in the absence of cache and when
the entities to be treated are of a consequent number.

Bundle SPARQL requests
~~~~~~~~~~~~~~~~~~~~~~

By default the SPARQL requests bundling is disabled
(``mul_req=False``). However, if you are using a remote KG and have a large
number of entities, this option can greatly speed up the extraction of walks:

.. code:: python

   import pandas as pd

   from pyrdf2vec import RDF2VecTransformer
   from pyrdf2vec.graphs import KG
   from pyrdf2vec.walkers import RandomWalker

   data = pd.read_csv("samples/countries-cities/entities.tsv", sep="\t")


   RDF2VecTransformer(walkers=[RandomWalker(4, 10)]).fit_transform(
       KG("https://dbpedia.org/sparql", mul_req=True),
       [entity for entity in data["location"]],
   )

In the above snippet, the KG specifies to the internal connector that it uses,
to fetch the hops of the specified entities in an asynchronous way. These hops
will then be stored in cache and be accessed by the walking strategy to
accelerate the extraction of walks for these entities.

**WARNING: bundling SPARQL requests for a number of entities considered too
large can may violate the policy of some SPARQL endpoint servers**. As for the
use of multiprocessing (which can be combined with ``mul_req``), sending a
large number of SPARQL requests simultaneously could be seen by a server as a
DOS. Be aware that the number of entities you have in your file corresponds to
the number of simultaneous requests that will be made and stored in cache.

Modify the Cache Settings
~~~~~~~~~~~~~~~~~~~~~~~~~

By default, ``pyRDF2Vec`` uses a cache that provides a `Least Recently Used
(LRU) <https://www.interviewcake.com/concept/java/lru-cache>`__ policy, with a
size that can hold 1024 entries, and a Time To Live (TTL) of 1200 seconds. For
some use cases, you would probably want to modify the `cache policy
<https://cachetools.readthedocs.io/en/stable/>`__, increase (or decrease) the
cache size and/or change the TTL:

.. code:: python

   import pandas as pd
   from cachetools import MRUCache

   from pyrdf2vec import RDF2VecTransformer
   from pyrdf2vec.graphs import KG
   from pyrdf2vec.walkers import RandomWalker

   data = pd.read_csv("samples/countries-cities/entities.tsv", sep="\t")

   RDF2VecTransformer(walkers=[RandomWalker(4, 10)]).fit_transform(
       KG("https://dbpedia.org/sparql", cache=MRUCache(maxsize=2048),
       [entity for entity in data["location"]],
   )

Modify the Walking Strategy Settings
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

By default, ``pyRDF2Vec`` uses ``[RandomWalker(2, None, UniformSampler())]`` as
walking strategy. Using a greater maximum depth indicates a longer extraction
time for walks. Add to this that using ``max_walks=None``, extracts more walks
and is faster in most cases than when giving a number (**SEE:** `FAQ <#faq>`__).

In some cases, using another sampling strategy can speed up the extraction of
walks by assigning a higher weight to some paths than others:

.. code:: python

   import pandas as pd

   from pyrdf2vec import RDF2VecTransformer
   from pyrdf2vec.graphs import KG
   from pyrdf2vec.samplers import PageRankSampler
   from pyrdf2vec.walkers import RandomWalker

   data = pd.read_csv("samples/countries-cities/entities.tsv", sep="\t")

   RDF2VecTransformer(
       walkers=[RandomWalker(2, None, PageRankSampler())]
   ).fit_transform(
       KG("https://dbpedia.org/sparql"),
       [entity for entity in data["location"]],
   )

Set Up a Local Server
~~~~~~~~~~~~~~~~~~~~~

Loading large RDF files into memory will cause memory issues. Remote KGs serve
as a solution for larger KGs, but **using a public endpoint will be slower**
due to overhead caused by HTTP requests. For that reason, it is better to set
up your own local server and use that for your "Remote" KG.

To set up such a server, a tutorial has been made `on our wiki
<https://github.com/IBCNServices/pyRDF2Vec/wiki/Fast-generation-of-RDF2Vec-embeddings-with-a-SPARQL-endpoint>`__.

Documentation
-------------

For more information on how to use ``pyRDF2Vec``, `visit our online documentation
<https://pyrdf2vec.readthedocs.io/en/latest/>`__ which is automatically updated
with the latest version of the ``master`` branch.

From then on, you will be able to learn more about the use of the
modules as well as their functions available to you.

Contributions
-------------

Your help in the development of ``pyRDF2Vec`` is more than welcome. In order to
better understand how you can help either through pull requests and/or issues,
please take a look at the `CONTRIBUTING
<https://github.com/IBCNServices/pyRDF2Vec/blob/master/CONTRIBUTING.rst>`__
file.

FAQ
---
How to Ensure the Generation of Similar Embeddings?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

``pyRDF2Vec``'s walking strategies, sampling strategies and Word2Vec work with
randomness. To get reproducible embeddings, you firstly need to **use a seed** to
ensure determinism:

.. code:: bash

   PYTHONHASHSEED=42 python foo.py

Added to this, you must **also specify a random state** to the walking strategy
which will implicitly use it for the sampling strategy:

.. code:: python

   from pyrdf2vec.walkers import RandomWalker

   RandomWalker(2, None, random_state=42)

**NOTE:** the ``PYTHONHASHSEED`` (e.g., 42) is to ensure determinism.

Finally, to ensure random determinism for Word2Vec, you must **specify a single
worker**:

.. code:: python

   from pyrdf2vec.embedders import Word2Vec

   Word2Vec(workers=1)

**NOTE:** using the ``n_jobs`` and ``mul_req`` parameters does not affect the
random determinism.

Why the extraction time of walks is faster if ``max_walks=None``?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Currently, **the BFS function** (using the Breadth-first search algorithm) is used
when ``max_walks=None`` which is significantly **faster** than the DFS function
(using the Depth-first search algorithm) **and extract more walks**.

We hope that this algorithmic complexity issue will be solved for the next
release of ``pyRDf2Vec``

Referencing
-----------

If you use ``pyRDF2Vec`` in a scholarly article, we would appreciate a
citation:

.. code:: bibtex

   @inproceedings{pyrdf2vec,
     author       = {Gilles Vandewiele and Bram Steenwinckel and Terencio Agozzino
                     and Michael Weyns and Pieter Bonte and Femke Ongenae
                     and Filip De Turck},
     title        = {{pyRDF2Vec: Python Implementation and Extension of RDF2Vec}},
     organization = {IDLab},
     year         = {2020},
     url          = {https://github.com/IBCNServices/pyRDF2Vec}
   }
