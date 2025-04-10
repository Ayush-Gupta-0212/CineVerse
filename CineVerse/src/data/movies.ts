
export interface Movie {
  id: string;
  title: string;
  description: string;
  releaseYear: number;
  duration: string;
  rating: number;
  genres: string[];
  moods: string[];
  imageUrl: string;
  trailerUrl: string;
  clipUrl: string;
}

export const genres = [
  'Action',
  'Adventure',
  'Animation',
  'Comedy',
  'Crime',
  'Documentary',
  'Drama',
  'Fantasy',
  'Horror',
  'Mystery',
  'Romance',
  'Sci-Fi',
  'Thriller'
];

export const moods = [
  'Excited',
  'Happy',
  'Relaxed',
  'Thoughtful',
  'Melancholic',
  'Tense',
  'Inspired',
  'Nostalgic'
];