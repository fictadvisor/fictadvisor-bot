import {createCallbackData} from "callback-data";

export const responseData = createCallbackData(
  "1",
  {
    method: String,
    id: String,
  }
);
