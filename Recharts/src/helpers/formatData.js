import posts from "../data/sentiment_output";

// - Se anno presente nella stringa
function checkYearPresent(dateStr) {
  // Espressione regolare per cercare un anno nel formato 'YYYY'
  const yearPattern = /\b\d{4}\b/;

  // Cerca un anno nella stringa data
  const match = dateStr.match(yearPattern);

  // Restituisci True se l'anno è presente, False altrimenti
  return match !== null;
}

// - Se anno contiene un giorno della settimana
function containsWeekday(string) {
  const weekDays = [
    "Monday",
    "Tuesday",
    "Wednesday",
    "Thursday",
    "Friday",
    "Saturday",
    "Sunday",
    "monday",
    "tuesday",
    "wednesday",
    "thursday",
    "friday",
    "saturday",
    "sunday",
    "Lunedì",
    "Martedì",
    "Mercoledì",
    "Giovedì",
    "Venerdì",
    "Sabato",
    "Domenica",
    "lunedì",
    "martedì",
    "mercoledì",
    "giovedì",
    "venerdì",
    "sabato",
    "domenica",
  ];

  for (const day of weekDays) {
    if (string.includes(day)) {
      return true;
    }
  }
  return false;
}

// - Aggiunta anno ne non presente
function addYearToDate(data) {
  // 1) VERIFICA SE NELLA STRINGA È PRESENTE L'ANNO =>
  // se ok allora procede con la formattazione
  if (checkYearPresent(data)) {
    try {
      // Prova a convertire la data con il mese scritto per intero
      return new Date(data);
    } catch (error) {
      // Se fallisce, prova con il mese scritto nel formato abbrevviato
      return new Date(data);
    }
  }

  // 2) ANNO NELLA STRINGA NON PRESENTE =>
  // se non presente allora si fa riferimento all'anno corrente
  const currentYear = new Date().getFullYear();
  data = `${data} ${currentYear}`;

  try {
    // Prova a convertire la data con il mese scritto per intero
    return new Date(data);
  } catch (error) {
    // Se fallisce, prova con il mese scritto nel formato abbrevviato
    return new Date(data);
  }
}

// - Format data
function formatData(data) {
  // CASO 1
  // "Yesterday at 10:46"
  // "Today at 12:04"
  // "Ieri alle 06:29"
  // "sabato alle 23:08"
  // "19 hrs"
  // "Date Not Found"
  // "45 minutes ago"
  // !!! Tali date verranno convertite nel formato 2024-05-01 00:00:00
  if (
    data.includes("Yesterday") ||
    data.includes("Today") ||
    data.includes("hrs") ||
    containsWeekday(data) ||
    data.includes("Date Not Found") ||
    data.includes("ago") ||
    data.includes("Ieri")
  ) {
    return new Date("2024-05");
  }

  // CASO 2
  // data contenente "alle" o "alle ore"
  // Esempio:
  // "3 maggio alle ore 01:00"
  if (data.includes("ore") || data.includes("alle")) {
    data = data.replace(" alle ore ", " ").replace(" alle ", " ");
    return addYearToDate(data);
  }

  // CASO 3
  try {
    // data formato "10/6/2022, 15:33"
    return new Date(data);
  } catch (error) {
    try {
      // data formato "24/1/2024"
      return new Date(data);
    } catch (error) {
      try {
        // data formato "5 giu 2023"
        return new Date(data);
      } catch (error) {
        // data formato accettabile (SI SPERA.....)
        return new Date(data);
      }
    }
  }
}

function processPost(post) {
  const platform = post.platform;

  // INSTAGRAM
  if (platform === "IG") {
    const dataPubblicazioneIG = formatData(post.taken_at_date);

    const postSing = {
      platform,
      source: post.source,
      giorno: dataPubblicazioneIG.getDate(),
      mese: dataPubblicazioneIG.getMonth() + 1,
      anno: dataPubblicazioneIG.getFullYear(),
      sentiment_post: post.sentiment,
      nr_like: post.likes_count,
      nr_comment: post.comments_count,
      comments: [],
    };

    for (const commentIG of post.comments || []) {
      if (commentIG.username == "verovolley") {
        continue;
      }
      const dataCommIG = formatData(commentIG.created_at_utc);

      const commIG = {
        author: commentIG.username,
        giorno: dataCommIG.getDate(),
        mese: dataCommIG.getMonth() + 1,
        anno: dataCommIG.getFullYear(),
        sentiment_comment: commentIG.sentiment,
        nr_like: commentIG.like_count,
      };

      postSing.comments.push(commIG);
    }

    return postSing;
  } else if (platform === "FB") {
    const dataPubblicazioneFB = formatData(post.date);

    const postSing = {
      platform,
      source: post.source,
      giorno: dataPubblicazioneFB.getDate(),
      mese: dataPubblicazioneFB.getMonth() + 1,
      anno: dataPubblicazioneFB.getFullYear(),
      sentiment_post: post.sentiment,
      nr_like: post.num_likes,
      nr_comment: post.num_comments,
      comments: [],
    };

    for (const commentFB of post.comments || []) {
      if (commentFB.author == "verovolley") {
        continue;
      }
      const dataCommFB = formatData(commentFB.date);

      const commFB = {
        author: commentFB.author,
        giorno: dataCommFB.getDate(),
        mese: dataCommFB.getMonth() + 1,
        anno: dataCommFB.getFullYear(),
        sentiment_comment: commentFB.sentiment,
        nr_like: commentFB.likes_num,
      };

      postSing.comments.push(commFB);
    }

    return postSing;
  } else if (platform === "Web") {
    const dataPubblicazioneWeb = formatData(post.date);

    const postSing = {
      platform,
      source: post.source,
      giorno: dataPubblicazioneWeb.getDate(),
      mese: dataPubblicazioneWeb.getMonth() + 1,
      anno: dataPubblicazioneWeb.getFullYear(),
      sentiment_post: post.sentiment,
      nr_like: "Not Defined",
      nr_comment: "Not Defined",
      comments: [],
    };

    for (const commentWeb of post.comments || []) {
      if (commentWeb.user == "verovolley") {
        continue;
      }
      const dataCommWeb = formatData(commentWeb.created_at_utc);

      const commWeb = {
        author: commentWeb.user,
        giorno: dataCommWeb.getDate(),
        mese: dataCommWeb.getMonth() + 1,
        anno: dataCommWeb.getFullYear(),
        sentiment_comment: commentWeb.sentiment,
        nr_like: "0",
      };

      postSing.comments.push(commWeb);
    }

    return postSing;
  }
}

export default function getProcessedPosts() {
  const newPosts = [];
  for (const post of posts) {
    newPosts.push(processPost(post));
  }
  return newPosts;
}
