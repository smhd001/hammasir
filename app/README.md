Documentation: Indexing, Slot Filling, and Elastic Querying
Overview

This document covers the functionality of three main components used in the project:

    Indexing (index.py): Defines the schema, settings, and processes for indexing data into Elasticsearch.
    Slot Filling (slot_filing.py): Handles natural language processing (NLP) to extract structured data (slots) from unstructured text.
    Elastic Querying (elastic_query.py): Provides functions for querying Elasticsearch, including constructing and executing search queries.

1. Indexing (index.py)
Purpose

The index.py script is responsible for creating and populating an Elasticsearch index with data. It connects to an Elasticsearch instance, sets up the index schema, and indexes documents.
Key Functions

    safe_literal_eval(val):
        Converts strings that represent Python literals into their corresponding Python objects.
        Returns None if evaluation fails.

    create_index(mappings, settings, index_name="doctors", reindex=True):
        Creates an Elasticsearch index with specified mappings and settings.
        Deletes the existing index and synonym sets if reindex=True.

    index(data, mappings=mappings, settings=settings, index_name="doctors", reindex=True):
        Indexes the provided data into Elasticsearch.
        Converts data rows into Elasticsearch documents and indexes them.

    get_data(path):
        Loads and preprocesses data from CSV files.
        Merges datasets and applies transformations.

Settings and Mappings

    Defines Elasticsearch mappings for various fields such as gender, expertise, title, etc.
    Configures custom analyzers for Persian text, including handling synonyms and normalization.

2. Slot Filling (slot_filing.py)
Purpose

The slot_filing.py script extracts structured information (slots) from unstructured text using NLP techniques. It leverages a pre-trained Named Entity Recognition (NER) model.
Key Functions

    slot_filing(text):
        Uses a transformer-based NER model to extract entities from text.
        Returns a dictionary where each key corresponds to a slot type and the values are lists of extracted entities.

Tags List

    Problem: The illness or medical service the user requires.
    Expertise: The specific medical expertise or specialization the user is seeking in a doctor.
    City: The city in which the user wants to find a doctor.
    Gender: The gender of the doctor preferred by the user.
    Neighborhood: The neighborhood where the doctor's clinic is located.
    Online-or-In-Person: The availability of online appointments versus in-person visits.
    Insurance: The types of insurance accepted by the doctor.
    First-Available-Appointment: The earliest possible time for the user to see the doctor.
    Amount-of-Delay: The expected waiting time at the clinic.
    Moral: The doctor’s level of respectfulness and manners.
    User-Score: The rating or score given to the doctor by users.
    Experience: The number of years the doctor has been practicing.

Dependencies

    Transformers: Used for the NER model and tokenizer.
    Optimum ONNX Runtime: For loading and running the NER model efficiently on GPU.

3. Elastic Querying (elastic_query.py)
Purpose

The elastic_query.py script constructs and executes search queries on the Elasticsearch index. It includes query configuration, building, and formatting.
Key Functions

    search(search_params):
        Executes a search query on Elasticsearch using provided parameters.
        Formats and returns the search results.

    configure_query(search_params, default_config):
        Configures query parameters based on input search parameters and default settings.
        Maps search parameters (e.g., gender) to appropriate terms.

    build_query(search_params, config=query_config):
        Constructs a boolean query with various filters and scoring functions.
        Supports advanced search features such as function scoring and query boosting.

    bound_query(*, query=None, function=None, maximum=5):
        Constructs a function score query based on provided query or function.

    build_query_v1(search_params, config=query_config):
        An earlier version of the query builder with different query structure.

    unrestricted_query(search_params, config=query_config):
        Builds a simpler query without restrictions.

    build_minimal_query(search_params, config=query_config):
        Constructs a minimal query focusing on essential parameters.

    dummy_query(text):
        Provides a hardcoded example of query results for testing purposes.

    get_lat_long(result, city):
        Extracts latitude and longitude from search results based on the specified city.

    format_result(result, search_params):
        Formats search results for easier presentation, including extracting title, expertise, and location.