import getProcessedPosts, { AVAILABLE_PLATFORMS } from "./formatData";

export function getPieSentimentData(
  seasons,
  platforms,
  sources,
  keywords,
  usePosts
) {
  const posts = getProcessedPosts();
  const sentiments = ["positive", "negative", "neutral"];

  const data = {};
  for (const sentiment of sentiments) {
    data[sentiment] = 0;
  }

  const total_comments = {};
  for (const sentiment of sentiments) {
    total_comments[sentiment] = 0;
  }

  for (const post of posts) {
    if (
      !platforms.includes(post.platform) ||
      !sources.includes(post.source) ||
      !keywords.some((keyword) => post.keywords.includes(keyword))
    ) {
      continue;
    }

    if (usePosts) {
      if (
        !sentiments.includes(post.sentiment_post) ||
        !seasons.includes(post.season)
      ) {
        continue;
      }
      data[post.sentiment_post] += 1;
      total_comments[post.sentiment_post] += 1;
    } else {
      for (const comment of post.comments) {
        if (
          !sentiments.includes(comment.sentiment_comment) ||
          !seasons.includes(comment.season)
        ) {
          continue;
        }
        data[comment.sentiment_comment] += 1;
        total_comments[comment.sentiment_comment] += 1;
      }
    }
  }

  const final_data = [];
  for (const sentiment of Object.keys(data)) {
    const subdata = {
      name: sentiment,
      value: data[sentiment],
    };

    final_data.push(subdata);
  }

  return final_data;
}

export function getPiePlatformDistributionData(
  season,
  sources,
  keywords,
  usePosts
) {
  const posts = getProcessedPosts();
  const platforms = AVAILABLE_PLATFORMS;

  const data = {};
  for (const platform of platforms) {
    data[platform.key] = 0;
  }

  const total_comments = {};
  for (const platform of platforms) {
    total_comments[platform.key] = 0;
  }

  for (const post of posts) {
    if (
      !sources.includes(post.source) ||
      !keywords.some((keyword) => post.keywords.includes(keyword))
    ) {
      continue;
    }

    if (usePosts) {
      if (season !== post.season) {
        continue;
      }
      data[post.platform] += 1;
      total_comments[post.platform] += 1;
    } else {
      for (const comment of post.comments) {
        if (season !== comment.season) {
          continue;
        }
        data[post.platform] += 1;
        total_comments[post.platform] += 1;
      }
    }
  }

  const final_data = [];
  for (const platform of Object.keys(data)) {
    const subdata = {
      name: platforms.find((p) => p.key === platform).name,
      value: data[platform],
    };

    final_data.push(subdata);
  }
  return final_data;
}
