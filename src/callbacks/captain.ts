import { createCallbackData } from "callback-data";

export const captainData = createCallbackData(
  "1",
  {
    method: String,
    id: String,
    telegramId: String,
  },
);
