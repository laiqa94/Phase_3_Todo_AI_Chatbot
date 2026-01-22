export type User = {
  id: string;
  email: string;
  displayName?: string;
};

export type Session = {
  accessToken: string;
  userId?: number;
  expiresAt?: string;
  user: User;
};
