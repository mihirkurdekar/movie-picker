const API_URL = import.meta.env.VITE_API_URL || '';

export async function fetchMovie({ category, difficulty, exclude = [] }) {
  // Use relative URL when API_URL is empty (production deployment)
  const endpoint = API_URL ? `${API_URL}/movie` : '/movie';

  const response = await fetch(endpoint, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      category,
      difficulty,
      exclude,
    }),
  });

  if (!response.ok) {
    const error = await response.json();
    throw new Error(error.error || 'Failed to fetch movie');
  }

  return response.json();
}