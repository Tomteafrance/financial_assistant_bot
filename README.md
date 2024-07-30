# financial_assistant_bot
ChatBot for financial news

This is 𝗵𝗼𝘄 you can 𝗶𝗺𝗽𝗹𝗲𝗺𝗲𝗻𝘁 a 𝘀𝘁𝗿𝗲𝗮𝗺𝗶𝗻𝗴 𝗽𝗶𝗽𝗲𝗹𝗶𝗻𝗲 to populate a 𝘃𝗲𝗰𝘁𝗼𝗿 𝗗𝗕 to do 𝗥𝗔𝗚 for a 𝗳𝗶𝗻𝗮𝗻𝗰𝗶𝗮𝗹 𝗮𝘀𝘀𝗶𝘀𝘁𝗮𝗻𝘁 powered by 𝗟𝗟𝗠𝘀.

🐝 All the following steps are wrapped in Bytewax functions and connected in a single streaming pipeline (aka Bytewax flow) ↓

𝗘𝘅𝘁𝗿𝗮𝗰𝘁 𝗳𝗶𝗻𝗮𝗻𝗰𝗶𝗮𝗹 𝗻𝗲𝘄𝘀 𝗳𝗿𝗼𝗺 𝗔𝗹𝗽𝗮𝗰𝗮

You need 2 types of inputs:

1. A WebSocket API to listen to financial news in real time - used to listen 24/7 for new data and ingest it as soon as it is available.

2. A RESTful API to ingest historical data in batch mode. When you deploy a fresh vector DB, you use it to populate it with older data.

You wrap the ingested HTML document and its metadata in a `pydantic` NewsArticle model to validate its schema.

Regardless of the input type, the ingested data is the same. Thus, the following steps are the same for both data inputs ↓

𝗣𝗮𝗿𝘀𝗲 𝘁𝗵𝗲 𝗛𝗧𝗠𝗟 𝗰𝗼𝗻𝘁𝗲𝗻𝘁

As the ingested financial news is in HTML, you must extract the text from particular HTML tags.

`unstructured` makes it as easy as calling `partition_html(document)`, which will recursively return the text within all essential HTML tags.

The parsed NewsArticle model is mapped into another `pydantic` model to validate its new schema:
- the headline
- summary
- full content.

𝗖𝗹𝗲𝗮𝗻 𝘁𝗵𝗲 𝘁𝗲𝘅𝘁

Now we have a bunch of text that has to be cleaned. Again, `unstructured` makes things easy. Calling a few functions we clean:
- the dashes & bullets
- extra whitespace & trailing punctuation
- non ascii chars
- invalid quotes

Finally, we standardize everything to lowercase.

𝗖𝗵𝘂𝗻𝗸 𝘁𝗵𝗲 𝘁𝗲𝘅𝘁

As the text can exceed the context window of the embedding model, we have to chunk it.

Yet again, `unstructured` provides a valuable function that splits the text based on the tokenized text and expected input length of the embedding model.

This strategy is naive, as it doesn't consider the text's structure, such as chapters, paragraphs, etc. As the news is short, this is not an issue, but LangChain provides a `RecursiveCharacterTextSplitter` class that does that if required.

𝗘𝗺𝗯𝗲𝗱 𝘁𝗵𝗲 𝗰𝗵𝘂𝗻𝗸𝘀

You pass all the chunks through an encoder-only model.

We have used `all-MiniLM-L6-v2` from `sentence-transformers`, a small model that can run on a CPU and outputs a 384 embedding.

But based on the size and complexity of your data, you might need more complex and bigger models.

𝗟𝗼𝗮𝗱 𝘁𝗵𝗲 𝗱𝗮𝘁𝗮 𝗶𝗻 𝘁𝗵𝗲 𝗤𝗱𝗿𝗮𝗻𝘁 𝘃𝗲𝗰𝘁𝗼𝗿 𝗗𝗕

Finally, you insert the embedded chunks and their metadata into the Qdrant vector DB.

The metadata contains the embedded text, the source_url and the publish date.