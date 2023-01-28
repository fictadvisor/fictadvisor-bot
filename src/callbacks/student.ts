import {CallbackData} from '@bot-base/callback-data';

export const studentData = new CallbackData<{
  method: string,
  id: string,
  telegramId: string,
}>(
  "2",
  ["method", "id", "telegramId"]
);
