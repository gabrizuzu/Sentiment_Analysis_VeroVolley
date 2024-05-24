import getProcessedPosts from "./formatData";

export const RADAR_KEYWORDS = ["Sylla", "Orro", "Egonu", "Danesi", "Larson"];

export function getRadarData(
  seasons,
  platforms,
  usePosts,
  useNeutral = false,
  useOffensive = false
) {
  const posts = getProcessedPosts();
  const sentiments = ["positive", "negative"];
  if (useNeutral) {
    sentiments.push("neutral");
  }
  const data = {};

  for (const keyword of RADAR_KEYWORDS) {
    const subdata = {};
    for (const sentiment of sentiments) {
      subdata[sentiment] = 0;
    }
    if (useOffensive) {
      subdata["offensive"] = 0;
    }
    data[keyword] = subdata;
  }

  const total_comments = {};

  for (const keyword of RADAR_KEYWORDS) {
    total_comments[keyword] = 0;
  }

  for (const post of posts) {
    if (
      !platforms.includes(post.platform) ||
      (usePosts && !seasons.includes(post.season))
    ) {
      continue;
    }
    for (const keyword of RADAR_KEYWORDS) {
      const keywordLower = keyword.toLowerCase();
      if (post.keywords.includes(keywordLower)) {
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
            let sentiment = comment.sentiment_comment;
            if (useOffensive && comment.isToxic) {
              sentiment = "offensive";
            }
            data[keyword][sentiment] += 1;
            total_comments[keyword] += 1;
          }
        }
      }
    }
  }
  if (useOffensive) {
    sentiments.push("offensive");
  }

  const final_data = [];
  const total_comments_sum = Object.values(total_comments).reduce(
    (a, b) => a + b
  );

  for (const sentiment of sentiments) {
    const subdata = { subject: sentiment };
    for (const keyword of RADAR_KEYWORDS) {
      subdata[keyword] = Math.round(
        (data[keyword][sentiment] * 100) / total_comments[keyword]
      );
    }
    final_data.push(subdata);
  }
  const quantity = { subject: "quantity" };
  for (const keyword of RADAR_KEYWORDS) {
    quantity[keyword] = Math.round(
      (total_comments[keyword] * 100) / total_comments_sum
    );
  }
  final_data.push(quantity);

  return final_data;
}

export function getRadarDataSentimentAsCorners(
  seasons,
  platforms,
  usePosts,
  attrs = null
) {
  const data = getRadarData(seasons, platforms, usePosts, true, true);

  return (attrs || RADAR_KEYWORDS).map((key) => {
    const item = {
      subject: key,
    };
    for (const value of data) {
      if (value.subject === "quantity") continue;
      item[value.subject] = value[key];
    }
    return item;
  });
}
