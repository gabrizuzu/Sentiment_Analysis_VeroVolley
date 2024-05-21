import posts from "../data/sentiment_output.json";
import { AVAILABLE_KEYWORDS } from "./formatData";

export const OFFENSIVE_KEYWORDS = ["VeroVolley", "egonu", "orro", "sylla"];

export function getOffensiveData(season) {
  // Take negatives as offensive TODO: change once we have the specific offensive data
  const offensiveComments = [];
  for (const post of posts) {
    for (const comment of post.comments) {
      if (
        comment.sentiment_comment === "negative" &&
        comment.season === season
      ) {
        comment.keywords = post.keywords;
        offensiveComments.push(comment);
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
    data.push({ subject: keyword, value: count });
  }

  return data;
}
