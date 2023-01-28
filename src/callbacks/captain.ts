import {CallbackData} from '@bot-base/callback-data';

export const captainData = new CallbackData<{
  method: string,
  id: string,
  telegramId: string,
}>(
  "1",
  ["method", "id", "telegramId"]
);
