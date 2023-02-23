import {client} from "./index";

export class ResponseApi {
  static async verifyResponse(id: string, data?: any) {
    await client.post(`/disciplineTeacher/${id}/responses`, data);
  }
}