import { AxiosInstance } from 'axios';

type OAuthTelegramPayload = {
    telegram_id: number;
    first_name: string;
    username?: string;
    last_name?: string;
    image?: string;
};

export default (client: AxiosInstance) => {
  const telegram = (payload: OAuthTelegramPayload) => client.post('/oauth/telegram', payload);

  return {
    telegram
  };
};
