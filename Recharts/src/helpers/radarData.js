import posts from "../data/sentiment_output.json";

function getRadarData() {
  const sentiments = ["positive", "negative", "neutral"];
  const keywords = ["sylla", "orro", "egonu", "danesi", "larson"];
  const data = {};

  for (const keyword of keywords) {
    const subdata = {};
    for (const sentiment of sentiments) {
      subdata[sentiment] = 0;
    }
    data[keyword] = subdata;
  }

  const total_comments = {};

  for (const keyword of keywords) {
    total_comments[keyword] = 0;
  }

  for (const post of posts) {
    for (const keyword of keywords) {
      if (post.keywords.includes(keyword)) {
        for (const comment of post.comments) {
          if (!sentiments.includes(comment.sentiment)) {
            continue;
          }
          data[keyword][comment.sentiment] += 1;
          total_comments[keyword] += 1;
        }
      }
    }
  }

  const final_data = [];

  for (const [keyword, value] of Object.entries(data)) {
    const subdata = { subject: keyword, fullMark: 100 };
    for (const sentiment of sentiments) {
      subdata[sentiment] =
        (data[keyword][sentiment] * 100) / total_comments[keyword];
    }
    final_data.push(subdata);
  }

  //   const inverted_data = [];

  //   for (const sentiment of sentiments) {
  //     const subdata = { subject: sentiment, fullMark: 100 };
  //     for (const keyword of keywords) {
  //       subdata[keyword] =
  //         (data[keyword][sentiment] * 100) / total_comments[keyword];
  //     }
  //     inverted_data.push(subdata);
  //   }

  return final_data;
}

export default getRadarData;
