import {CallbackData} from '@bot-base/callback-data';

export const superheroData = new CallbackData<{
  method: string,
  id: string,
  telegramId: string,
}>(
  "3",
  ["method", "id", "telegramId"]
);
