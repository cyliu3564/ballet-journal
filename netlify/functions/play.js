exports.handler = async (event, context) => {
  const songId = event.queryStringParameters?.id;
  if (!songId || !/^\d+$/.test(songId)) {
    return { statusCode: 400, body: JSON.stringify({ error: 'Invalid song ID' }) };
  }

  try {
    // Fetch the outer URL with redirect follow to get the final CDN URL
    const res = await fetch(`https://music.163.com/song/media/outer/url?id=${songId}.mp3`, {
      headers: {
        'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X)',
        'Referer': 'https://music.163.com/',
      },
    });

    // res.url contains the final redirected URL after following all redirects
    const finalUrl = res.url;

    if (!finalUrl || finalUrl.includes('404')) {
      return { statusCode: 404, body: JSON.stringify({ error: 'Song unavailable' }) };
    }

    // Force HTTPS on CDN URL
    const httpsUrl = finalUrl.replace(/^http:\/\//, 'https://');

    return {
      statusCode: 302,
      headers: {
        'Location': httpsUrl,
        'Cache-Control': 'public, max-age=3600',
      },
    };
  } catch (err) {
    return { statusCode: 500, body: JSON.stringify({ error: err.message }) };
  }
};
