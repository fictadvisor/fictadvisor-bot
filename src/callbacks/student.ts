import { createCallbackData } from 'callback-data';

export const studentData = createCallbackData(
  "2",
  {
    method: String,
    id: String,
    telegramId: String,
  }
);
