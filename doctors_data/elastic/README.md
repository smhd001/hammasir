Indexing and Searching in Elasticsearch

This documentation provides an overview of the indexing and searching processes for doctor data using Elasticsearch, outlining how to set up, configure, and utilize custom analyzers for Persian text processing.
1. Overview

The project involves two main parts:

    Indexing doctor data (index.py): This script loads and processes data about doctors (such as their expertise, experience, and biography) and indexes it into Elasticsearch with custom Persian text analyzers.
    Searching the indexed data (search.ipynb): This script is used to build, execute, and analyze search queries to retrieve relevant doctor profiles based on various criteria.

2. Data Indexing (index.py)
2.1 Elasticsearch Connection

The script connects to a local Elasticsearch instance using the following credentials:

    URL: https://localhost:9200
    Basic Auth: Username: elastic, Password: hammasir
    Certificate Verification: Disabled for local connection.

It verifies the connection by printing cluster information using es.info().
2.2 Mappings and Settings

    Mappings: Defines how each field in the doctor dataset is structured within the Elasticsearch index. The fields include:
        gender: Keyword
        expertise, title, view, insurances, about: Text (used for full-text search)
        star, doctor_encounter, explanation_of_issue, quality_of_treatment, waiting_time: Float
        rates_count, comments_count, number_of_visits: Integer
        experience: Integer
        clinic: Object (contains detailed information about the clinic)
        presence_freeturn: Date (epoch format)
        url and image: Text (indexed but not analyzed)
    Custom Persian Analyzer:
        Handles Persian text normalization, stemming, and stopword removal.
        Index-time Analyzer: Applied when data is indexed. It removes zero-width spaces, normalizes Arabic and Persian characters, and performs stemming.
        Search-time Analyzer: Extends the index analyzer with synonyms and stopwords to improve search accuracy.

2.3 Synonym Handling

    Synonyms: The script loads a list of synonyms from a synonyms.txt file. This file contains common medical and general synonyms in Persian, which help map similar terms (e.g., "تب" (fever) and "لرز" (chills)).

    These synonyms are applied only at search-time, making search queries more flexible and effective.

2.4 Index Creation

    create_index():
        Deletes the existing index if it already exists (if reindexing is enabled).
        Loads synonyms and creates a new index with the specified mappings and settings.
    The function configures Elasticsearch to use the custom Persian analyzers for both indexing and searching.

2.5 Indexing Documents

    After creating the index, the script iterates over the dataset and uploads individual doctor profiles as documents in Elasticsearch.

    Each document contains various fields related to the doctor’s expertise, experience, clinic, ratings, and more. It also includes:
        "About" field: A biography field extracted from the doctor's profile, processed to remove HTML tags and unnecessary characters.

    If any field (like waiting_time or presence_freeturn) is missing, it is replaced with a default value (e.g., 4 for waiting_time).

2.6 Data Loading

    The get_data() function loads two CSV files:
        new_dataset.csv: Contains doctor profile data such as expertise, gender, experience, and ratings.
        about_dataset.csv: Contains additional information, primarily the "about" section (biography) of the doctors.
    The data from both files is merged based on the unique medical_code field, ensuring a complete profile for each doctor.

3. Searching Indexed Data (search.ipynb)
3.1 Elasticsearch Connection

    Similar to index.py, this script connects to the local Elasticsearch instance using the same credentials and setup.

3.2 Search Query Configuration

    The search process begins with defining a set of search parameters. These parameters dictate what the user is looking for in a doctor. For example:
        City: مشهد (Mashhad)
        Gender: زن (Female)
        Expertise: ستون فقرات (Spine Specialist)
        Problem: کمرم (Back Pain)
        Neighborhood: کوهسنگی (Kooh Sangi)

    These search parameters are fed into a query configuration system that:
        Configures the query using predefined settings (query_config).
        Builds the query using the custom analyzers, taking into account Persian-specific text normalization and synonym handling.

3.3 Executing Search Queries

    The configured query is sent to Elasticsearch using the es.search() function.

    Elasticsearch returns a list of results (doctor profiles) matching the search criteria. Each result includes fields like expertise, rating (stars), experience, and biography.

    For each search result, the script prints the doctor’s expertise and star rating, providing the user with an overview of the most relevant doctors for their query.

3.4 Query Explanation

    The es.explain() function is used to explain how the search query matched a specific document (doctor profile). This provides detailed information about how the relevance score was calculated and which fields contributed most to the match.

3.5 Text Analysis

    The script demonstrates the use of es.indices.analyze() to analyze specific text inputs (e.g., چشمام meaning "my eyes"). This ensures that the custom Persian analyzers are working correctly, normalizing and tokenizing the text as expected.

4. Key Functionalities
4.1 Data Indexing (via index.py)

    Custom Persian Analyzers: The index and search analyzers are tailored for Persian text, improving the accuracy and relevance of searches in Persian.
    Synonym Handling: A dynamic synonym set helps improve search flexibility, ensuring that queries can match related terms (e.g., medical synonyms).
    Efficient Indexing: The script indexes large volumes of doctor profiles, with each document structured to allow flexible and powerful search capabilities.

4.2 Searching (via search.ipynb)

    Flexible Query Building: The system allows users to search for doctors based on various criteria, including location, expertise, gender, and symptoms.
    Real-time Search: Search results are retrieved in real-time, providing relevant doctor profiles based on the user’s input.
    Query Debugging and Explanation: The es.explain() function helps users understand how search results are ranked, offering insights into query scoring.

5. Example Use Case

    Indexing: Suppose you have a dataset of doctors in different cities, including their expertise, experience, and biographies. By running index.py, you can index all this information into Elasticsearch, making it searchable.

    Searching: Using search.ipynb, you can search for a female spine specialist in Mashhad with experience in treating back pain. The search query will use the custom Persian analyzers and synonym sets to find the most relevant doctors, returning profiles with expertise, ratings, and other relevant information.

6. Conclusion

This project leverages Elasticsearch to index and search doctor profiles efficiently. With custom Persian analyzers and synonym handling, the system is optimized for Persian-language search queries, providing accurate and relevant results for users.