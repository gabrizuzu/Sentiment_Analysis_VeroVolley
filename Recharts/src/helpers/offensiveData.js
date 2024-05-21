import posts from "../data/sentiment_output.json";
import { AVAILABLE_KEYWORDS, AVAILABLE_PLATFORMS } from "./formatData";

export const OFFENSIVE_KEYWORDS = ["VeroVolley", "egonu", "orro", "sylla"];

export function getOffensiveData(season, platforms, percentual = false) {
  // Take negatives as offensive TODO: change once we have the specific offensive data

  const totalCountCommentsPerKeyword = {};
  const offensiveComments = [];
  for (const post of posts) {
    if (!platforms.includes(post.platform)) {
      continue;
    }
    for (const comment of post.comments) {
      if (comment.isToxic && comment.season === season) {
        comment.keywords = post.keywords;
        offensiveComments.push(comment);
      }
      for (const keyword of OFFENSIVE_KEYWORDS) {
        const keywords = AVAILABLE_KEYWORDS[keyword]
          ? AVAILABLE_KEYWORDS[keyword]
          : [keyword];
        if (post.keywords.some((k) => keywords.includes(k))) {
          totalCountCommentsPerKeyword[keyword] = totalCountCommentsPerKeyword[
            keyword
          ]
            ? totalCountCommentsPerKeyword[keyword] + 1
            : 1;
        }
      }
    }
  }

  // Order data as [{subject: "keyword", value: 1}, ...]
  const data = [];
  for (const keyword of OFFENSIVE_KEYWORDS) {
    const keywords = AVAILABLE_KEYWORDS[keyword]
      ? AVAILABLE_KEYWORDS[keyword]
      : [keyword];
    const count = offensiveComments.filter((comment) =>
      keywords.some((k) => comment.keywords.includes(k))
    ).length;

    let value = count;
    if (percentual) {
      value =
        Math.round((count * 10000) / totalCountCommentsPerKeyword[keyword]) /
        100;
      if (isNaN(value)) {
        value = 0;
      }
    }

    data.push({
      subject: keyword.charAt(0).toUpperCase() + keyword.slice(1),
      [`Comments${percentual ? " %" : ""}`]: value,
    });
  }

  return data;
}

export function getOffensiveDistributionData(season, platforms) {
  // For offensive distribution we require the toxicity, severe_toxicity, identity_attack and insult
  const data = [];
  const offensiveComments = [];
  for (const post of posts) {
    if (!platforms.includes(post.platform)) {
      continue;
    }
    for (const comment of post.comments) {
      if (comment.isToxic && comment.season === season) {
        comment.keywords = post.keywords;
        offensiveComments.push(comment);
      }
    }
  }

  for (const keyword of OFFENSIVE_KEYWORDS) {
    const keywords = AVAILABLE_KEYWORDS[keyword]
      ? AVAILABLE_KEYWORDS[keyword]
      : [keyword];
    const attrs = {
      toxicity: "Toxicity",
      severe_toxicity: "Severe_Toxicity",
      identity_attack: "Identity_Attack",
      insult: "Insult",
    };

    const keywordData = {
      subject: keyword.charAt(0).toUpperCase() + keyword.slice(1),
    };
    for (const attr of Object.values(attrs)) {
      keywordData[attr] = 0;
    }

    let count = 0;
    for (const comment of offensiveComments) {
      if (keywords.some((k) => comment.keywords.includes(k))) {
        for (const [attr, name] of Object.entries(attrs)) {
          keywordData[name] += comment[attr];
        }
        count += 1;
      }
    }
    for (const attr of Object.values(attrs)) {
      keywordData[attr] = count ? keywordData[attr] / count : 0;
      keywordData[attr] = Math.round(keywordData[attr] * 100) / 100;
    }

    data.push(keywordData);
  }

  return data;
}
