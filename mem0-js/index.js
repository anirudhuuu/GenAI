import "dotenv/config";

import { Memory } from "mem0ai/oss";
import { OpenAI } from "openai";

const client = new OpenAI();

const mem = new Memory({
  version: "v1.1",
  vectorStore: {
    provider: "qdrant",
    config: {
      collectionName: "memories",
      embeddingModelDims: 1536,
      host: "localhost",
      port: 6333,
    },
  },
});

mem.add([{ role: "user", content: "My name is Anirudh" }], {
  userId: "anirudh",
});

async function main(query = "") {
  const response = await client.chat.completions.create({
    model: "gpt-4.1-mini",
    messages: [{ role: "user", content: query }],
  });

  console.log("Bot:", response.choices[0].message.content);
}

main("Hey Agent,You know my name is Anirudh and i am from Lucknow");
