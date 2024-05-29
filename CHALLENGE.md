# Problem description

As conversation with Kin goes on a lot of information is generated. The information is extracted and added to the knowledge graph the agent have. However not all details are relevant or should be added to the KG.

I'm going to assume the KG is added into the context along with some amount of the previous messages, however adding the messages have some undesired side effects:

* There is a maximum amount of content we can put into the context length.
* The biggest the context length the highest the cost of using chatgpt.

# Proposal: Compaction

Given most of the words and content of messages can be ignored we can create summaries to compact the information, so rather than having 1000 messages we will end up with 1000 messages + compacted summaries and we will be using the summaries rather than the raw messages. A conversation might look like the following:

message 1
message 2
message 3
message 4
message 5

After some amount of time or number of messages we will run the compaction (a model capable of doing summarization). Say we compact every 4 messages, on the context we will send summary 1 and message 5 only.

```
          | message 1
          | message 2
summary 1 | message 3
          | message 4
message 5
```

Overtime might make sense to also summarize the summaries having the following structure:

```
                       | message 1
          |            | message 2
          |  summary 1 | message 3
          |            | message 4
summary 3 |
          |            | message 5
          |            | message 6
          |  summary 2 | message 7
          |            | message 8
message 9
```

In this case the context will only contain summary 3 and message 9.

# Downsides to consider

1) We might be missing information after the compaction happens.
2) We will need to store more information to store the summaries.
