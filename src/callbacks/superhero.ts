import {createCallbackData} from "callback-data";

export const superheroData = createCallbackData(
  "3",
  {
    method: String,
    id: String,
    telegramId: String,
  }
);
