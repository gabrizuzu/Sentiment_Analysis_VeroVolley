import getProcessedPosts from "./formatData";

function getRadarData(seasons, platforms, usePosts) {
  const posts = getProcessedPosts();
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
    if (
      !platforms.includes(post.platform) ||
      (usePosts && !seasons.includes(post.season))
    ) {
      continue;
    }
    for (const keyword of keywords) {
      if (post.keywords.includes(keyword)) {
        if (usePosts) {
          data[keyword][post.sentiment_post] += 1;
          total_comments[keyword] += 1;
        } else {
          for (const comment of post.comments) {
            if (
              !sentiments.includes(comment.sentiment_comment) ||
              !seasons.includes(comment.season)
            ) {
              continue;
            }
            data[keyword][comment.sentiment_comment] += 1;
            total_comments[keyword] += 1;
          }
        }
      }
    }
  }

  const final_data = [];

  for (const [keyword, value] of Object.entries(data)) {
    const subdata = { subject: keyword };
    for (const sentiment of sentiments) {
      subdata[sentiment] = Math.round(
        (data[keyword][sentiment] * 100) / total_comments[keyword]
      );
    }
    subdata.subject = keyword.charAt(0).toUpperCase() + keyword.slice(1);
    final_data.push(subdata);
  }
  return final_data;
}

export default getRadarData;
