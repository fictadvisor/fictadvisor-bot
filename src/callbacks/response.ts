import {createCallbackData} from "callback-data";

export const responseData = createCallbackData(
  "response",
  {
    method: String,
    id: String,
  }
);
